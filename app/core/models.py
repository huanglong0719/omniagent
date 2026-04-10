from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class MemoryTier(str, Enum):
    CORE = "L1"        # High priority, always in context
    RECALL = "L2"      # Semantic search, paged in
    ARCHIVAL = "L3"    # Full history, cold storage

class AgentRole(str, Enum):
    MANAGER = "manager"
    RESEARCHER = "researcher"
    WRITER = "writer"
    CRITIC = "critic"
    GENERAL = "general"

class OmniMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    sender: str  # 'user' or 'agent' or 'system'
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    channel: str  # 'telegram', 'whatsapp', 'web', etc.
    metadata: Dict[str, Any] = {}
    tier: MemoryTier = MemoryTier.ARCHIVAL # Default storage tier

class Session(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    current_context: List[OmniMessage] = []
    metadata: Dict[str, Any] = {}
