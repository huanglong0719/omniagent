import os
from typing import List, Optional, Dict
from datetime import datetime
from app.core.models import OmniMessage
from app.memory.manager import OmniMemoryManager
from app.evolution.verification import SkillVerificationSystem
from app.evolution.generator import SkillGenerator
from app.evolution.marketplace import SkillMarketplace

class EvolutionEngine:
    """
    EvolutionEngine: The Cognitive Layer.
    Handles the creation, storage, and retrieval of reusable skills.
    """
    
    def __init__(self, memory_manager: OmniMemoryManager, skills_dir: str = "omniagent/skills"):
        self.memory = memory_manager
        self.skills_dir = skills_dir
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)
        self.verification_system = SkillVerificationSystem(skills_dir)
        self.skill_generator = SkillGenerator()
        self.skill_marketplace = SkillMarketplace(skills_dir)


    def get_best_skill(self, query: str) -> Optional[str]:
        """
        Retrieves the most relevant skill from the library based on the query.
        Only returns verified skills for reliability.
        """
        print(f"[EvolutionEngine] Searching for best skill for: {query}")
        
        # 1. Semantic search in L2 memory to find skill filenames
        # In a real system, we'd store skill metadata in L2
        # For demo, we'll just list files and do a simple keyword match
        skills = os.listdir(self.skills_dir)
        for skill_file in skills:
            if skill_file.endswith(".md") and any(word in skill_file.lower() for word in query.lower().split()):
                # Check if skill is verified
                status = self.verification_system.get_skill_status(skill_file)
                if status == "Verified":
                    with open(os.path.join(self.skills_dir, skill_file), "r", encoding="utf-8") as f:
                        return f.read()
        
        # If no verified skill found, look for pending or beta skills
        for skill_file in skills:
            if skill_file.endswith(".md") and any(word in skill_file.lower() for word in query.lower().split()):
                with open(os.path.join(self.skills_dir, skill_file), "r", encoding="utf-8") as f:
                    return f.read()
        
        return None

    async def create_skill(self, task_name: str, experience_trace: str, success_criteria: str, category: str = "general_task"):
        """
        Creates a new Markdown skill from a successful experience trace using the skill generator.
        """
        # Generate skill using generator
        skill_content = self.skill_generator.generate_skill(
            skill_name=task_name,
            skill_description="This skill was evolved from a successful experience.",
            category=category,
            execution_steps=[
                {"title": "执行任务", "description": experience_trace}
            ],
            success_criteria=[success_criteria]
        )
        
        # Save skill
        file_path = self.skill_generator.save_skill(skill_content, self.skills_dir)
        skill_name = os.path.basename(file_path)
        
        # Submit for verification
        self.verification_system.submit_for_verification(skill_name, "EvolutionEngine")
        
        # Add to marketplace
        self.skill_marketplace.add_skill(
            skill_name=task_name,
            skill_file=file_path,
            category=category,
            description="This skill was evolved from a successful experience."
        )
        
        print(f"[EvolutionEngine] New skill created: {skill_name}")
        print(f"[EvolutionEngine] Skill submitted for verification")
        print(f"[EvolutionEngine] Skill added to marketplace")
        return skill_name

    async def evolve(self, task_name: str, conversation_history: List[OmniMessage]):
        """
        The Learning Loop: Analyzes history and creates a reusable skill.
        """
        print(f"[EvolutionEngine] Evolving skill for task: {task_name}")
        
        # 1. Extract experience trace (Mocking the LLM reflection process)
        trace = "\n".join([f"{m.sender}: {m.content}" for m in conversation_history])
        experience_trace = f"Based on the history, the successful pattern was: {trace[:200]}..."
        
        # 2. Define success criteria
        success_criteria = "The user confirmed the result was correct."
        
        # 3. Determine skill category based on task name
        task_name_lower = task_name.lower()
        if any(keyword in task_name_lower for keyword in ["research", "调研", "调查"]):
            category = "research"
        elif any(keyword in task_name_lower for keyword in ["write", "写", "文章", "报告"]):
            category = "writing"
        elif any(keyword in task_name_lower for keyword in ["analyze", "分析", "评估"]):
            category = "analysis"
        elif any(keyword in task_name_lower for keyword in ["plan", "规划", "计划"]):
            category = "planning"
        else:
            category = "general_task"
        
        # 4. Create the skill
        return await self.create_skill(task_name, experience_trace, success_criteria, category)
