from typing import List, Dict, Optional
import os
import json
from datetime import datetime

class SkillMarketplace:
    """技能市场机制"""
    
    def __init__(self, skills_dir: str = "omniagent/skills", marketplace_file: str = "skills/marketplace.json"):
        self.skills_dir = skills_dir
        self.marketplace_file = marketplace_file
        self._load_marketplace()
    
    def _load_marketplace(self):
        """加载技能市场数据"""
        if not os.path.exists(self.marketplace_file):
            self.marketplace = {
                "skills": [],
                "categories": [],
                "ratings": {}
            }
            self._save_marketplace()
        else:
            with open(self.marketplace_file, "r", encoding="utf-8") as f:
                self.marketplace = json.load(f)
    
    def _save_marketplace(self):
        """保存技能市场数据"""
        if not os.path.exists(os.path.dirname(self.marketplace_file)):
            os.makedirs(os.path.dirname(self.marketplace_file))
        with open(self.marketplace_file, "w", encoding="utf-8") as f:
            json.dump(self.marketplace, f, indent=2, ensure_ascii=False)
    
    def add_skill(self, skill_name: str, skill_file: str, category: str, description: str) -> bool:
        """
        添加技能到市场
        
        Args:
            skill_name: 技能名称
            skill_file: 技能文件路径
            category: 技能类别
            description: 技能描述
            
        Returns:
            是否添加成功
        """
        # 检查技能是否已存在
        for skill in self.marketplace["skills"]:
            if skill["name"] == skill_name:
                return False
        
        # 添加技能
        skill_id = f"skill_{len(self.marketplace['skills']) + 1}"
        self.marketplace["skills"].append({
            "id": skill_id,
            "name": skill_name,
            "file": skill_file,
            "category": category,
            "description": description,
            "created_at": datetime.utcnow().isoformat(),
            "version": "1.0",
            "downloads": 0,
            "rating": 0.0
        })
        
        # 添加类别（如果不存在）
        if category not in self.marketplace["categories"]:
            self.marketplace["categories"].append(category)
        
        self._save_marketplace()
        return True
    
    def get_skills(self, category: Optional[str] = None) -> List[Dict]:
        """
        获取技能列表
        
        Args:
            category: 技能类别（可选）
            
        Returns:
            技能列表
        """
        if category:
            return [skill for skill in self.marketplace["skills"] if skill["category"] == category]
        return self.marketplace["skills"]
    
    def rate_skill(self, skill_id: str, rating: float, user_id: str, comment: str = "") -> bool:
        """
        评价技能
        
        Args:
            skill_id: 技能ID
            rating: 评分（1-5）
            user_id: 用户ID
            comment: 评价内容
            
        Returns:
            是否评价成功
        """
        # 检查技能是否存在
        skill = next((s for s in self.marketplace["skills"] if s["id"] == skill_id), None)
        if not skill:
            return False
        
        # 添加评价
        if skill_id not in self.marketplace["ratings"]:
            self.marketplace["ratings"][skill_id] = []
        
        self.marketplace["ratings"][skill_id].append({
            "user_id": user_id,
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # 更新技能评分
        ratings = [r["rating"] for r in self.marketplace["ratings"][skill_id]]
        skill["rating"] = sum(ratings) / len(ratings) if ratings else 0.0
        
        self._save_marketplace()
        return True
    
    def download_skill(self, skill_id: str) -> Optional[str]:
        """
        下载技能
        
        Args:
            skill_id: 技能ID
            
        Returns:
            技能文件路径
        """
        # 检查技能是否存在
        skill = next((s for s in self.marketplace["skills"] if s["id"] == skill_id), None)
        if not skill:
            return None
        
        # 增加下载次数
        skill["downloads"] += 1
        self._save_marketplace()
        
        return skill["file"]
    
    def get_categories(self) -> List[str]:
        """
        获取技能类别列表
        
        Returns:
            类别列表
        """
        return self.marketplace["categories"]