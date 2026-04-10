from typing import Dict, Optional
from datetime import datetime
import os

class SkillGenerator:
    """技能自动生成器"""
    
    def __init__(self, templates_dir: str = "skills/templates"):
        self.templates_dir = templates_dir
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
        self._load_templates()
    
    def _load_templates(self):
        """加载技能模板"""
        self.templates = {}
        for template_file in os.listdir(self.templates_dir):
            if template_file.endswith(".md"):
                template_name = template_file.replace(".md", "")
                with open(os.path.join(self.templates_dir, template_file), "r", encoding="utf-8") as f:
                    self.templates[template_name] = f.read()
    
    def generate_skill(self, skill_name: str, skill_description: str, category: str = "general_task", 
                      execution_steps: Optional[list] = None, success_criteria: Optional[list] = None) -> str:
        """
        生成技能
        
        Args:
            skill_name: 技能名称
            skill_description: 技能描述
            category: 技能类别
            execution_steps: 执行步骤（可选）
            success_criteria: 成功标准（可选）
            
        Returns:
            生成的技能内容
        """
        # 选择模板
        template = self.templates.get(category, self.templates.get("general_task"))
        if not template:
            raise ValueError(f"Template for category '{category}' not found")
        
        # 替换模板变量
        skill_content = template.replace("{{skill_name}}", skill_name)
        skill_content = skill_content.replace("{{skill_description}}", skill_description)
        skill_content = skill_content.replace("{{created_at}}", datetime.utcnow().isoformat())
        skill_content = skill_content.replace("{{status}}", "Beta (Pending Verification)")
        skill_content = skill_content.replace("{{version}}", "1.0")
        
        # 如果提供了自定义步骤，替换默认步骤
        if execution_steps:
            steps_content = "\n".join([f"{i+1}. **{step['title']}**: {step['description']}" for i, step in enumerate(execution_steps)])
            skill_content = skill_content.replace("## Execution Steps\n1. **理解任务**：分析用户的请求，明确任务目标和要求\n2. **收集信息**：收集完成任务所需的相关信息\n3. **执行操作**：根据任务类型执行相应的操作\n4. **验证结果**：检查执行结果是否符合要求\n5. **返回结果**：将执行结果反馈给用户", f"## Execution Steps\n{steps_content}")
        
        # 如果提供了自定义成功标准，替换默认标准
        if success_criteria:
            criteria_content = "\n".join([f"- {criterion}" for criterion in success_criteria])
            skill_content = skill_content.replace("## Success Criteria\n- 任务目标得到明确理解\n- 所有必要的信息都被收集\n- 操作执行正确无误\n- 结果符合用户要求\n- 用户确认任务完成", f"## Success Criteria\n{criteria_content}")
        
        return skill_content
    
    def save_skill(self, skill_content: str, skills_dir: str = "omniagent/skills") -> str:
        """
        保存技能到文件
        
        Args:
            skill_content: 技能内容
            skills_dir: 技能保存目录
            
        Returns:
            保存的文件路径
        """
        if not os.path.exists(skills_dir):
            os.makedirs(skills_dir)
        
        # 从内容中提取技能名称
        lines = skill_content.split('\n')
        skill_name_line = next((line for line in lines if line.startswith("# Skill: ")), "")
        skill_name = skill_name_line.replace("# Skill: ", "").strip()
        
        # 生成文件名
        filename = f"skill_{skill_name.replace(' ', '_').lower()}.md"
        file_path = os.path.join(skills_dir, filename)
        
        # 保存文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(skill_content)
        
        return file_path