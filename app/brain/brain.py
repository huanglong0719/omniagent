from typing import List, Optional, Dict, Any
from app.core.models import OmniMessage, Session, AgentRole
from app.memory.manager import OmniMemoryManager
from app.evolution.engine import EvolutionEngine
from app.core.llm import LLMClient
from langgraph.graph import Graph

class ComplexityEvaluator:
    """
    Evaluates the complexity of a user request to decide the orchestration mode.
    Supports both English and Chinese keywords and uses multiple factors for assessment.
    """
    def __init__(self):
        # Complexity indicators
        self.complex_keywords = [
            # English
            "report", "research", "analyze", "compare", "plan", "build", 
            "develop", "design", "implement", "create", "optimize", "evaluate",
            # Chinese
            "报告", "调研", "分析", "对比", "计划", "构建", "设计",
            "开发", "实现", "创建", "优化", "评估", "研究"
        ]
        
        self.task_type_keywords = {
            "research": ["research", "调研", "研究", "调查"],
            "writing": ["write", "撰写", "写作", "报告"],
            "analysis": ["analyze", "分析", "评估", "评价"],
            "planning": ["plan", "计划", "规划", "安排"]
        }
    
    def evaluate(self, content: str) -> str:
        """
        Evaluate the complexity of a user request based on multiple factors:
        1. Length of the request
        2. Presence of complex keywords
        3. Number of different task types mentioned
        4. Specificity and detail level
        """
        content_lower = content.lower()
        
        # Factor 1: Length-based complexity
        length_score = min(len(content) / 200, 1.0)
        
        # Factor 2: Complex keyword presence
        keyword_score = 0
        for keyword in self.complex_keywords:
            if keyword in content_lower:
                keyword_score += 1
        keyword_score = min(keyword_score / 3, 1.0)
        
        # Factor 3: Task type diversity
        task_types = set()
        for task_type, keywords in self.task_type_keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    task_types.add(task_type)
                    break
        task_diversity_score = min(len(task_types) / 2, 1.0)
        
        # Factor 4: Specificity (presence of details like numbers, dates, specific requirements)
        specificity_score = 0
        if any(char.isdigit() for char in content):
            specificity_score += 0.3
        if any(punct in content for punct in ["!", "?", ":", ";"]):
            specificity_score += 0.2
        if len(content.split()) > 15:
            specificity_score += 0.5
        specificity_score = min(specificity_score, 1.0)
        
        # Calculate total complexity score
        total_score = (length_score * 0.2) + (keyword_score * 0.4) + (task_diversity_score * 0.2) + (specificity_score * 0.2)
        
        print(f"[ComplexityEvaluator] Complexity score: {total_score:.2f}")
        
        # Determine mode based on score
        if total_score > 0.5:
            return "COMPLEX"
        return "SIMPLE"
    
    def get_task_type(self, content: str) -> str:
        """
        Determine the primary task type based on keywords.
        """
        content_lower = content.lower()
        for task_type, keywords in self.task_type_keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    return task_type
        return "general"

class LangGraphMultiAgent:
    """
    Multi-agent collaboration using LangGraph for complex workflows and state management.
    Dynamically adjusts workflow based on task type.
    """
    def __init__(self, task_content: str, llm: LLMClient):
        self.task_content = task_content
        self.llm = llm
        self.evaluator = ComplexityEvaluator()
        self.task_type = self.evaluator.get_task_type(task_content)
        self.graph = self._build_graph()

    def _build_graph(self) -> Graph:
        """Build the LangGraph workflow based on task type."""
        graph = Graph()
        
        # Common nodes
        graph.add_node("finalize", self._finalize_node)
        
        # Build workflow based on task type
        if self.task_type == "research":
            # Research-focused workflow
            graph.add_node("researcher", self._researcher_node)
            graph.add_node("analyzer", self._analyzer_node)
            graph.add_edge("researcher", "analyzer")
            graph.add_edge("analyzer", "finalize")
            graph.set_entry_point("researcher")
        elif self.task_type == "writing":
            # Writing-focused workflow
            graph.add_node("writer", self._writer_node)
            graph.add_node("editor", self._editor_node)
            graph.add_edge("writer", "editor")
            graph.add_edge("editor", "finalize")
            graph.set_entry_point("writer")
        elif self.task_type == "analysis":
            # Analysis-focused workflow
            graph.add_node("data_collector", self._data_collector_node)
            graph.add_node("analyzer", self._analyzer_node)
            graph.add_node("visualizer", self._visualizer_node)
            graph.add_edge("data_collector", "analyzer")
            graph.add_edge("analyzer", "visualizer")
            graph.add_edge("visualizer", "finalize")
            graph.set_entry_point("data_collector")
        elif self.task_type == "planning":
            # Planning-focused workflow
            graph.add_node("planner", self._planner_node)
            graph.add_node("reviewer", self._reviewer_node)
            graph.add_edge("planner", "reviewer")
            graph.add_edge("reviewer", "finalize")
            graph.set_entry_point("planner")
        else:
            # General workflow
            graph.add_node("researcher", self._researcher_node)
            graph.add_node("writer", self._writer_node)
            graph.add_node("critic", self._critic_node)
            graph.add_edge("researcher", "writer")
            graph.add_edge("writer", "critic")
            graph.add_edge("critic", "finalize")
            graph.set_entry_point("researcher")
        
        return graph

    async def _researcher_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Researcher agent node."""
        print("[LangGraph] Running Researcher node")
        prompt = f"You are a Researcher. Gather key data about: {self.task_content}. Provide a concise summary."
        research_res = await self.llm.generate([{"role": "user", "content": prompt}])
        return {"research": research_res, "state": "research_completed"}

    async def _writer_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Writer agent node."""
        print("[LangGraph] Running Writer node")
        research_res = state.get("research", "")
        prompt = f"You are a Writer. Based on this research: {research_res}, write a professional report."
        writer_res = await self.llm.generate([{"role": "user", "content": prompt}])
        return {"report": writer_res, "state": "writing_completed"}

    async def _critic_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Critic agent node."""
        print("[LangGraph] Running Critic node")
        report = state.get("report", "")
        prompt = f"You are a Critic. Review this report: {report}. Provide a final polished version."
        critic_res = await self.llm.generate([{"role": "user", "content": prompt}])
        return {"final_report": critic_res, "state": "review_completed"}

    async def _analyzer_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzer agent node."""
        print("[LangGraph] Running Analyzer node")
        research_res = state.get("research", "")
        prompt = f"You are an Analyst. Analyze this research: {research_res}. Provide insights and recommendations."
        analysis_res = await self.llm.generate([{"role": "user", "content": prompt}])
        return {"analysis": analysis_res, "state": "analysis_completed"}

    async def _data_collector_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Data collector agent node."""
        print("[LangGraph] Running Data Collector node")
        prompt = f"You are a Data Collector. Collect relevant data for: {self.task_content}. Organize it clearly."
        data_res = await self.llm.generate([{"role": "user", "content": prompt}])
        return {"data": data_res, "state": "data_collected"}

    async def _visualizer_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Visualizer agent node."""
        print("[LangGraph] Running Visualizer node")
        analysis_res = state.get("analysis", "")
        prompt = f"You are a Visualizer. Based on this analysis: {analysis_res}, suggest visual representations and key insights."
        visual_res = await self.llm.generate([{"role": "user", "content": prompt}])
        return {"visualization": visual_res, "state": "visualization_completed"}

    async def _planner_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Planner agent node."""
        print("[LangGraph] Running Planner node")
        prompt = f"You are a Planner. Create a detailed plan for: {self.task_content}. Include steps, timeline, and resources."
        plan_res = await self.llm.generate([{"role": "user", "content": prompt}])
        return {"plan": plan_res, "state": "plan_created"}

    async def _reviewer_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Reviewer agent node."""
        print("[LangGraph] Running Reviewer node")
        plan_res = state.get("plan", "")
        prompt = f"You are a Reviewer. Review this plan: {plan_res}. Provide feedback and improvements."
        review_res = await self.llm.generate([{"role": "user", "content": prompt}])
        return {"review": review_res, "state": "plan_reviewed"}

    async def _editor_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Editor agent node."""
        print("[LangGraph] Running Editor node")
        report = state.get("report", self.task_content)
        prompt = f"You are an Editor. Edit and polish this content: {report}. Improve clarity, flow, and style."
        edit_res = await self.llm.generate([{"role": "user", "content": prompt}])
        return {"edited_content": edit_res, "state": "content_edited"}

    async def _finalize_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Finalize node."""
        print("[LangGraph] Running Finalize node")
        # Get the most relevant result based on task type
        if self.task_type == "research":
            final_result = state.get("analysis", "") or state.get("research", "")
        elif self.task_type == "writing":
            final_result = state.get("edited_content", "") or state.get("report", "")
        elif self.task_type == "analysis":
            final_result = state.get("visualization", "") or state.get("analysis", "")
        elif self.task_type == "planning":
            final_result = state.get("review", "") or state.get("plan", "")
        else:
            final_result = state.get("final_report", "") or state.get("report", "") or state.get("research", "")
        
        return {"final_result": final_result, "state": "completed"}

    async def execute(self) -> str:
        """Execute the LangGraph workflow."""
        print(f"[LangGraph] Starting collaboration for: {self.task_content}")
        print(f"[LangGraph] Task type: {self.task_type}")
        
        # Run the graph
        result = await self.graph.run({"task": self.task_content, "task_type": self.task_type})
        
        # Return the final result
        return result.get("final_result", "")

class OmniBrain:
    """
    OmniBrain: The Orchestration Layer.
    Manages the agentic loop, memory interaction, and skill application.
    """
    
    def __init__(self, memory_manager: OmniMemoryManager):
        self.memory = memory_manager
        self.llm = LLMClient()
        self.evolution = EvolutionEngine(memory_manager=memory_manager)
        self.evaluator = ComplexityEvaluator()
        
    async def process_message(self, message: OmniMessage, session: Session) -> str:
        """
        The core agentic loop with dynamic orchestration.
        """
        print(f"[OmniBrain] Processing message: {message.content}")
        
        # 1. Memory Retrieval & Prefetching
        context = await self.memory.get_context(session.session_id)
        await self.memory.predictive_prefetch(session.session_id, message.content)
        
        # 2. Skill Retrieval
        skill = self.evolution.get_best_skill(message.content)
        skill_prompt = f"\\n\\n[Applied Skill]:\\n{skill}" if skill else ""
        
        # 3. Dynamic Orchestration (Task 9)
        complexity = self.evaluator.evaluate(message.content)
        if complexity == "COMPLEX":
            print(f"[OmniBrain] Complexity: COMPLEX. Switching to LangGraph Multi-Agent mode.")
            agent = LangGraphMultiAgent(message.content, self.llm)
            response = await agent.execute()
        else:
            print(f"[OmniBrain] Complexity: SIMPLE. Using Single-Agent mode.")
            # Use LLM for the response instead of mock string
            prompt = f"User message: {message.content}. {skill_prompt} Please respond concisely."
            response = await self.llm.generate([{"role": "user", "content": prompt}])
        
        # 4. Store the interaction in memory
        await self.memory.add_message(message, session)
        
        # Store AI response as well
        ai_msg = OmniMessage(
            session_id=session.session_id,
            sender="agent",
            content=response,
            channel=message.channel
        )
        await self.memory.add_message(ai_msg, session)
        
        # 5. Self-Evolution Trigger (Task 8)
        if any(word in message.content.lower() for word in ["thanks", "correct", "谢谢", "正确", "赞", "太棒了"]):
            task_name = "General Task" 
            await self.evolution.evolve(task_name, context + [message, ai_msg])
        
        return response
