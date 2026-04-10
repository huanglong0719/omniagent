from typing import Optional, Dict, List
from datetime import datetime
import os

class SkillVerificationSystem:
    """Skill verification system with HITL (Human-In-The-Loop)审核机制."""
    
    def __init__(self, skills_dir: str = "omniagent/skills"):
        self.skills_dir = skills_dir
        self.verification_status: Dict[str, str] = {}
        self.review_history: Dict[str, List[Dict]] = {}
        self._load_skill_status()
    
    def _load_skill_status(self):
        """Load skill verification status from files."""
        if not os.path.exists(self.skills_dir):
            return
        
        for skill_file in os.listdir(self.skills_dir):
            if skill_file.endswith(".md"):
                file_path = os.path.join(self.skills_dir, skill_file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Extract status from metadata
                    if "Status: " in content:
                        status_line = [line for line in content.split('\n') if "Status: " in line][0]
                        status = status_line.split("Status: ")[1].strip()
                        self.verification_status[skill_file] = status
    
    def get_skill_status(self, skill_name: str) -> str:
        """Get the verification status of a skill."""
        return self.verification_status.get(skill_name, "Unknown")
    
    def submit_for_verification(self, skill_name: str, submitter: str) -> bool:
        """Submit a skill for verification."""
        if skill_name not in self.verification_status:
            return False
        
        # Update status to Pending Review
        self.verification_status[skill_name] = "Pending Review"
        
        # Update skill file
        self._update_skill_status(skill_name, "Pending Review")
        
        # Add to review history
        if skill_name not in self.review_history:
            self.review_history[skill_name] = []
        
        self.review_history[skill_name].append({
            "action": "Submitted for review",
            "by": submitter,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        print(f"[Verification] Skill {skill_name} submitted for verification by {submitter}")
        return True
    
    def review_skill(self, skill_name: str, reviewer: str, approved: bool, comments: str = "") -> bool:
        """Review a skill (HITL审核)."""
        if skill_name not in self.verification_status:
            return False
        
        # Update status based on review
        status = "Verified" if approved else "Rejected"
        self.verification_status[skill_name] = status
        
        # Update skill file
        self._update_skill_status(skill_name, status)
        
        # Add to review history
        if skill_name not in self.review_history:
            self.review_history[skill_name] = []
        
        self.review_history[skill_name].append({
            "action": f"{'Approved' if approved else 'Rejected'}",
            "by": reviewer,
            "comments": comments,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        print(f"[Verification] Skill {skill_name} {'approved' if approved else 'rejected'} by {reviewer}")
        return True
    
    def _update_skill_status(self, skill_name: str, status: str):
        """Update the status in the skill file."""
        file_path = os.path.join(self.skills_dir, skill_name)
        if not os.path.exists(file_path):
            return
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace status line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "Status: " in line:
                lines[i] = f"- Status: {status}"
                break
        
        updated_content = '\n'.join(lines)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
    
    def get_pending_skills(self) -> List[str]:
        """Get list of skills pending review."""
        return [skill for skill, status in self.verification_status.items() if status == "Pending Review"]
    
    def get_skill_review_history(self, skill_name: str) -> List[Dict]:
        """Get review history for a skill."""
        return self.review_history.get(skill_name, [])
