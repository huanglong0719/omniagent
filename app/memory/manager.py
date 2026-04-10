import sqlite3
import json
import math
import time
from typing import List, Optional, Dict, Any, Tuple, Deque
from collections import deque
from datetime import datetime, timedelta
from app.core.models import OmniMessage, MemoryTier, Session
from app.security.encryption import get_encryption_util
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct

class OmniMemoryManager:
    """
    OmniMemory Manager (Production-Ready Prototype)
    Implements a tiered storage system:
    L1: In-memory cache (Redis-like)
    L2: Vector storage for semantic retrieval (Local Vector Index)
    L3: Persistent SQL storage (SQLite)
    """
    
    def __init__(self, db_path: str = "omniagent.db", vector_db_url: str = "http://localhost:6333"):
        self.db_path = db_path
        self._init_db()
        self.encryption_util = get_encryption_util()
        
        # L1 Cache: {session_id: [OmniMessage, ...]}
        self._l1_cache: Dict[str, List[OmniMessage]] = {}
        self.L1_MAX_SIZE = 20
        
        # L2 Vector Storage
        self.vector_db_url = vector_db_url
        self._use_qdrant = False
        self._qdrant_client = None
        self._collection_name = "omniagent_messages"
        
        # Fallback to local vector index
        self._l2_index: Dict[str, Tuple[List[float], OmniMessage]] = {}
        
        # Try to initialize Qdrant
        try:
            self._qdrant_client = QdrantClient(url=self.vector_db_url)
            self._init_vector_db()
            self._use_qdrant = True
            print("[Memory] Qdrant vector database initialized successfully")
        except Exception as e:
            print(f"[Memory] Qdrant initialization failed: {e}")
            print("[Memory] Falling back to local vector index")
            self._use_qdrant = False
        
        # Access frequency tracking: {message_id: access_count}
        self._access_frequency: Dict[str, int] = {}
        
        # Recently Used queue: {session_id: deque(message_id)}
        self._recently_used: Dict[str, Deque[str]] = {}
        
        # Paging configuration
        self.PAGE_SIZE = 5
        self.PREFETCH_LIMIT = 3
        
        # Prediction model (simple frequency-based for now)
        self._topic_frequency: Dict[str, int] = {}
        self._session_topics: Dict[str, List[str]] = {}
        
        # Batch processing for L3 storage
        self._batch_insert: List[OmniMessage] = []
        self._batch_size = 50  # 增加批处理大小
        self._batch_interval = 0.5  # 增加批处理间隔
        self._last_batch_time = time.time()
        
        # Database connection pool (simple implementation)
        self._db_conn = None
        
        # Memory cleanup timer
        self._cleanup_interval = 3600  # 1 hour
        self._last_cleanup = time.time()
        
        # Session timeout
        self._session_timeout = 3600  # 1 hour
        self._session_last_access = {}
        


    def _init_db(self):
        """Initialize SQLite tables for L3 storage."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    message_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    sender TEXT,
                    content TEXT,
                    timestamp TEXT,
                    channel TEXT,
                    tier TEXT
                )
            ''')
            # Skills table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skills (
                    skill_id TEXT PRIMARY KEY,
                    name TEXT,
                    content TEXT,
                    version INTEGER,
                    status TEXT,
                    created_at TEXT
                )
            ''')
            conn.commit()

    def _init_vector_db(self):
        """Initialize Qdrant vector database."""
        # Check if collection exists
        collections = self._qdrant_client.get_collections()
        collection_names = [col.name for col in collections.collections]
        
        if self._collection_name not in collection_names:
            # Create collection with 768-dimensional vectors (BERT embeddings)
            self._qdrant_client.create_collection(
                collection_name=self._collection_name,
                vectors_config=VectorParams(size=768, distance="Cosine")
            )

    async def add_message(self, message: OmniMessage, session: Session):
        """
        Adds a message to the memory system with batch processing.
        """
        # Update session access time and trigger cleanup
        await self.update_session_access(session.session_id)
        
        # 1. Add to L1 (Active Context)
        await self._add_to_l1(session.session_id, message)
        
        # 2. Index in L2 (Semantic Vector)
        await self._index_in_l2(message)
        
        # 3. Add to batch for L3 storage
        self._batch_insert.append(message)
        
        # Check if batch processing is needed
        current_time = time.time()
        if len(self._batch_insert) >= self._batch_size or current_time - self._last_batch_time >= self._batch_interval:
            await self._process_batch()
            self._last_batch_time = current_time

    async def _add_to_l1(self, session_id: str, message: OmniMessage):
        if session_id not in self._l1_cache:
            self._l1_cache[session_id] = []
        if session_id not in self._recently_used:
            self._recently_used[session_id] = deque(maxlen=self.L1_MAX_SIZE)
        
        # Check if message is already in L1
        existing_index = None
        for i, msg in enumerate(self._l1_cache[session_id]):
            if msg.message_id == message.message_id:
                existing_index = i
                break
        
        if existing_index is not None:
            # Move to end if already exists (most recently used)
            self._l1_cache[session_id].pop(existing_index)
        
        # Add to L1 and update recently used queue
        self._l1_cache[session_id].append(message)
        self._recently_used[session_id].append(message.message_id)
        
        # Update access frequency
        self._access_frequency[message.message_id] = self._access_frequency.get(message.message_id, 0) + 1
        
        # Maintain L1 size limit (LRU based on recently used)
        if len(self._l1_cache[session_id]) > self.L1_MAX_SIZE:
            # Remove least recently used message
            lru_message_id = self._recently_used[session_id].popleft()
            self._l1_cache[session_id] = [m for m in self._l1_cache[session_id] if m.message_id != lru_message_id]

    def _get_db_conn(self):
        """Get database connection."""
        if not hasattr(self, '_db_conn') or self._db_conn is None:
            self._db_conn = sqlite3.connect(self.db_path)
        return self._db_conn

    def _close_db_conn(self):
        """Close database connection."""
        if hasattr(self, '_db_conn') and self._db_conn:
            self._db_conn.close()
            self._db_conn = None

    async def _process_batch(self):
        """Process batch insertion to L3."""
        if not self._batch_insert:
            return
        
        batch = self._batch_insert.copy()
        self._batch_insert = []
        
        conn = self._get_db_conn()
        cursor = conn.cursor()
        
        # Begin transaction
        conn.execute('BEGIN TRANSACTION')
        try:
            for message in batch:
                # Encrypt sensitive content before storage
                encrypted_content = self.encryption_util.encrypt(message.content)
                cursor.execute('''
                    INSERT OR REPLACE INTO messages 
                    (message_id, session_id, sender, content, timestamp, channel, tier)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    message.message_id, 
                    message.session_id, 
                    message.sender, 
                    encrypted_content, 
                    message.timestamp.isoformat() if message.timestamp else datetime.now().isoformat(), 
                    message.channel, 
                    message.tier.value if hasattr(message, 'tier') else 'L3'
                ))
            # Commit transaction
            conn.commit()
        except Exception as e:
            # Rollback on error
            conn.rollback()
            print(f"Error processing batch: {e}")

    async def _store_in_l3(self, message: OmniMessage):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Encrypt sensitive content before storage
            encrypted_content = self.encryption_util.encrypt(message.content)
            cursor.execute('''
                INSERT OR REPLACE INTO messages 
                (message_id, session_id, sender, content, timestamp, channel, tier)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                message.message_id, 
                message.session_id, 
                message.sender, 
                encrypted_content, 
                message.timestamp.isoformat(), 
                message.channel, 
                message.tier.value
            ))
            conn.commit()

    async def _index_in_l2(self, message: OmniMessage):
        # Mock embedding generation (In real system, use OpenAI/HuggingFace embeddings)
        # We'll use a simple hash-based mock embedding for the prototype
        embedding = [float(hash(word) % 100 / 100.0) for word in message.content.split()]
        
        if self._use_qdrant:
            # Pad embedding to 768 dimensions to match Qdrant collection
            while len(embedding) < 768:
                embedding.append(0.0)
            if len(embedding) > 768:
                embedding = embedding[:768]
            
            # Store in Qdrant
            point = PointStruct(
                id=message.message_id,
                vector=embedding,
                payload={
                    "session_id": message.session_id,
                    "sender": message.sender,
                    "content": message.content,
                    "timestamp": message.timestamp.isoformat() if message.timestamp else datetime.now().isoformat(),
                    "channel": message.channel
                }
            )
            
            # Upsert point to Qdrant
            try:
                self._qdrant_client.upsert(
                    collection_name=self._collection_name,
                    points=[point]
                )
            except Exception as e:
                print(f"[Memory] Qdrant upsert failed: {e}")
                print("[Memory] Falling back to local vector index")
                self._l2_index[message.message_id] = (embedding, message)
        else:
            # Use local vector index as fallback
            self._l2_index[message.message_id] = (embedding, message)
            # Limit L2 size
            if len(self._l2_index) > 1000:
                # Remove oldest message
                oldest_id = next(iter(self._l2_index))
                del self._l2_index[oldest_id]

    async def get_context(self, session_id: str) -> List[OmniMessage]:
        """Retrieves the current L1 context."""
        # Update session access time and trigger cleanup
        await self.update_session_access(session_id)
        return self._l1_cache.get(session_id, [])

    async def page_in(self, session_id: str, query: str, limit: int = 5):
        """
        Paging In: Retrieves relevant memories from L2 and promotes them to L1.
        Implements smart paging with priority-based selection.
        """
        # Update session access time and trigger cleanup
        await self.update_session_access(session_id)
        
        print(f"[Paging] Paging IN relevant memories for query: {query}")
        
        # Get relevant memories
        relevant_memories = await self.semantic_search(query, session_id, limit * 2)  # Get more candidates
        
        # Sort by access frequency (prioritize frequently accessed)
        sorted_memories = sorted(
            relevant_memories,
            key=lambda msg: self._access_frequency.get(msg.message_id, 0),
            reverse=True
        )[:limit]
        
        # Page in the selected memories
        paged_in_memories = []
        for msg in sorted_memories:
            await self._add_to_l1(session_id, msg)
            paged_in_memories.append(msg)
        
        # Update topic frequency for prediction
        self._update_topic_frequency(query)
        if session_id not in self._session_topics:
            self._session_topics[session_id] = []
        self._session_topics[session_id].append(query)
        if len(self._session_topics[session_id]) > 10:
            self._session_topics[session_id] = self._session_topics[session_id][-10:]
        
        return paged_in_memories

    async def page_out(self, session_id: str, message_id: str):
        """Paging Out: Removes a specific message from L1."""
        if session_id in self._l1_cache:
            self._l1_cache[session_id] = [m for m in self._l1_cache[session_id] if m.message_id != message_id]

    async def semantic_search(self, query: str, session_id: str, limit: int = 5) -> List[OmniMessage]:
        """
        L2 Semantic Search using Qdrant vector database or local fallback.
        """
        print(f"[L2 Search] Searching for: {query}")
        
        # Generate query embedding
        query_emb = [float(hash(word) % 100 / 100.0) for word in query.split()]
        
        if self._use_qdrant:
            # Pad embedding to 768 dimensions
            while len(query_emb) < 768:
                query_emb.append(0.0)
            if len(query_emb) > 768:
                query_emb = query_emb[:768]
            
            # Search in Qdrant
            try:
                search_result = self._qdrant_client.search(
                    collection_name=self._collection_name,
                    query_vector=query_emb,
                    limit=limit,
                    filter={
                        "must": [
                            {
                                "key": "session_id",
                                "match": {
                                    "value": session_id
                                }
                            }
                        ]
                    }
                )
                
                # Convert search results to OmniMessage objects
                results = []
                for hit in search_result:
                    payload = hit.payload
                    message = OmniMessage(
                        message_id=hit.id,
                        session_id=payload.get("session_id"),
                        sender=payload.get("sender"),
                        content=payload.get("content"),
                        timestamp=datetime.fromisoformat(payload.get("timestamp")),
                        channel=payload.get("channel")
                    )
                    results.append(message)
                
                return results
            except Exception as e:
                print(f"[Memory] Qdrant search failed: {e}")
                print("[Memory] Falling back to local vector index")
                # Fall through to local vector index
        
        # Use local vector index as fallback
        # Simple cosine similarity mock
        results = []
        for mid, (emb, msg) in self._l2_index.items():
            if msg.session_id == session_id:
                # Mock similarity score
                score = sum(a*b for a, b in zip(query_emb, emb)) if len(query_emb) == len(emb) else 0
                results.append((score, msg))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [msg for score, msg in results[:limit]]

    def _update_topic_frequency(self, query: str):
        """Update topic frequency based on query."""
        # Simple topic extraction (split by spaces and take keywords)
        keywords = query.lower().split()
        for keyword in keywords:
            if len(keyword) > 3:  # Only track meaningful keywords
                self._topic_frequency[keyword] = self._topic_frequency.get(keyword, 0) + 1

    async def predictive_prefetch(self, session_id: str, current_query: str):
        """
        Predicts related memories and loads them into L1 asynchronously.
        Uses frequency-based prediction and session context.
        """
        print(f"[Prefetch] Predicting related memories for: {current_query}")
        
        # Extract keywords from current query
        current_keywords = current_query.lower().split()
        
        # Get top related topics based on frequency
        related_topics = []
        for keyword in current_keywords:
            if len(keyword) > 3:
                # Find related topics based on co-occurrence
                for topic, freq in self._topic_frequency.items():
                    if topic != keyword and freq > 1:
                        related_topics.append((freq, topic))
        
        # Sort by frequency
        related_topics.sort(reverse=True)
        predicted_keywords = [topic for _, topic in related_topics[:self.PREFETCH_LIMIT]]
        
        # Also consider recent topics from the same session
        if session_id in self._session_topics:
            recent_topics = self._session_topics[session_id][-5:]
            for topic in recent_topics:
                if topic not in predicted_keywords:
                    predicted_keywords.append(topic)
                    if len(predicted_keywords) >= self.PREFETCH_LIMIT:
                        break
        
        # If no predictions, use a fallback
        if not predicted_keywords:
            predicted_keywords = [f"related to {current_query}"]
        
        # Limit to prefetch limit
        predicted_keywords = predicted_keywords[:self.PREFETCH_LIMIT]
        
        # Prefetch related memories
        for kw in predicted_keywords:
            await self.page_in(session_id, kw, limit=2)

    async def get_from_l3(self, message_id: str) -> Optional[OmniMessage]:
        """Retrieves a message from L3 storage with decryption."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT message_id, session_id, sender, content, timestamp, channel, tier
                FROM messages
                WHERE message_id = ?
            ''', (message_id,))
            row = cursor.fetchone()
            if row:
                # Decrypt content
                decrypted_content = self.encryption_util.decrypt(row[3])
                return OmniMessage(
                    message_id=row[0],
                    session_id=row[1],
                    sender=row[2],
                    content=decrypted_content,
                    timestamp=datetime.fromisoformat(row[4]),
                    channel=row[5],
                    tier=MemoryTier(row[6])
                )
            return None
    
    async def cleanup_memory(self):
        """Cleanup memory by removing inactive sessions and old data."""
        current_time = time.time()
        
        # Check if cleanup is needed
        if current_time - self._last_cleanup < self._cleanup_interval:
            return
        
        print("[Memory] Performing memory cleanup...")
        
        # Remove inactive sessions
        inactive_sessions = []
        for session_id, last_access in self._session_last_access.items():
            if current_time - last_access > self._session_timeout:
                inactive_sessions.append(session_id)
        
        for session_id in inactive_sessions:
            if session_id in self._l1_cache:
                del self._l1_cache[session_id]
            if session_id in self._recently_used:
                del self._recently_used[session_id]
            if session_id in self._session_topics:
                del self._session_topics[session_id]
            if session_id in self._session_last_access:
                del self._session_last_access[session_id]
        
        # Limit L2 index size
        if len(self._l2_index) > 5000:
            # Keep most recent 5000 entries
            recent_keys = list(self._l2_index.keys())[-5000:]
            self._l2_index = {key: self._l2_index[key] for key in recent_keys}
        
        # Limit access frequency tracking
        if len(self._access_frequency) > 10000:
            # Keep top 10000 most accessed
            sorted_freq = sorted(self._access_frequency.items(), key=lambda x: x[1], reverse=True)[:10000]
            self._access_frequency = dict(sorted_freq)
        
        # Limit topic frequency tracking
        if len(self._topic_frequency) > 1000:
            # Keep top 1000 most frequent topics
            sorted_topics = sorted(self._topic_frequency.items(), key=lambda x: x[1], reverse=True)[:1000]
            self._topic_frequency = dict(sorted_topics)
        
        # Close database connection if idle
        self._close_db_conn()
        
        self._last_cleanup = current_time
        print(f"[Memory] Cleanup completed. Removed {len(inactive_sessions)} inactive sessions.")
    
    async def update_session_access(self, session_id: str):
        """Update session last access time."""
        self._session_last_access[session_id] = time.time()
        # Trigger cleanup if needed
        await self.cleanup_memory()
