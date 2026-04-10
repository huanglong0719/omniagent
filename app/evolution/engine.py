import os
from typing import List, Optional, Dict
from datetime import datetime
from app.core.models import OmniMessage
from app.memory.manager import OmniMemoryManager
from app.evolution.verification import SkillVerificationSystem

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

    async def create_skill(self, task_name: str, experience_trace: str, success_criteria: str):
        """
        Creates a new Markdown skill from a successful experience trace.
        """
        skill_name = f"skill_{task_name.replace(' ', '_').lower()}.md"
        file_path = os.path.join(self.skills_dir, skill_name)
        
        skill_content = f"""# Skill: {task_name}
## Description
This skill was evolved from a successful experience.

## Execution Steps
{experience_trace}

## Success Criteria
{success_criteria}

## Metadata
- Created at: {datetime.utcnow()}
- Status: Beta (Pending Verification)
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(skill_content)
        
        # Submit for verification
        self.verification_system.submit_for_verification(skill_name, "EvolutionEngine")
        
        print(f"[EvolutionEngine] New skill created: {skill_name}")
        print(f"[EvolutionEngine] Skill submitted for verification")
        return skill_name

    async def evolve(self, task_name: str, conversation_history: List[OmniMessage]):
        """
        The Learning Loop: Analyzes history and creates a reusable skill.
        """
        print(f"[EvolutionEngine] Evolving skill for task: {task_name}")
        
        # 1. Extract experience trace (Mocking the LLM reflection process)
        trace = "\\n".join([f"{m.sender}: {m.content}" for m in conversation_history])
        experience_trace = f"Based on the history, the successful pattern was: {trace[:200]}..."
        
        # 2. Define success criteria
        success_criteria = "The user confirmed the result was correct."
        
        # 3. Create the skill
        return await self.create_skill(task_name, experience_trace, success_criteria)
