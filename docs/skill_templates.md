# 通用技能模板

## 1. 模板说明

本目录包含 OmniAgent 系统的通用技能模板，用于快速创建各种类型的技能。这些模板提供了标准化的结构，确保技能的一致性和可维护性。

## 2. 技能模板列表

### 2.1 通用任务模板 (general_task.md)

```markdown
# Skill: {{skill_name}}
## Description
{{skill_description}}

## Execution Steps
1. **理解任务**：分析用户的请求，明确任务目标和要求
2. **收集信息**：收集完成任务所需的相关信息
3. **执行操作**：根据任务类型执行相应的操作
4. **验证结果**：检查执行结果是否符合要求
5. **返回结果**：将执行结果反馈给用户

## Success Criteria
- 任务目标得到明确理解
- 所有必要的信息都被收集
- 操作执行正确无误
- 结果符合用户要求
- 用户确认任务完成

## Metadata
- Created at: {{created_at}}
- Status: {{status}}
- Version: {{version}}
- Category: General
```

### 2.2 研究任务模板 (research.md)

```markdown
# Skill: {{skill_name}}
## Description
{{skill_description}}

## Execution Steps
1. **明确研究目标**：确定研究的具体问题和范围
2. **收集资料**：搜索和收集相关的资料和信息
3. **分析资料**：对收集到的资料进行分析和整理
4. **得出结论**：基于分析结果得出合理的结论
5. **呈现结果**：以清晰的方式呈现研究结果

## Success Criteria
- 研究目标明确具体
- 收集的资料全面准确
- 分析方法科学合理
- 结论有充分的依据
- 结果呈现清晰易懂

## Metadata
- Created at: {{created_at}}
- Status: {{status}}
- Version: {{version}}
- Category: Research
```

### 2.3 写作任务模板 (writing.md)

```markdown
# Skill: {{skill_name}}
## Description
{{skill_description}}

## Execution Steps
1. **理解写作要求**：明确写作的目的、风格和格式要求
2. **构思内容**：规划文章的结构和主要内容
3. **撰写初稿**：按照规划撰写文章初稿
4. **修改完善**：对初稿进行修改和完善
5. **最终审查**：检查文章的质量和准确性

## Success Criteria
- 符合写作要求和规范
- 内容结构清晰合理
- 语言表达流畅准确
- 逻辑连贯有条理
- 满足用户的具体需求

## Metadata
- Created at: {{created_at}}
- Status: {{status}}
- Version: {{version}}
- Category: Writing
```

### 2.4 分析任务模板 (analysis.md)

```markdown
# Skill: {{skill_name}}
## Description
{{skill_description}}

## Execution Steps
1. **明确分析目标**：确定分析的具体问题和目标
2. **收集数据**：收集分析所需的数据和信息
3. **处理数据**：对数据进行清洗和预处理
4. **分析数据**：使用适当的方法进行数据分析
5. **生成报告**：基于分析结果生成详细的报告

## Success Criteria
- 分析目标明确具体
- 数据收集全面准确
- 分析方法科学合理
- 结果解释清晰易懂
- 报告内容完整详细

## Metadata
- Created at: {{created_at}}
- Status: {{status}}
- Version: {{version}}
- Category: Analysis
```

### 2.5 规划任务模板 (planning.md)

```markdown
# Skill: {{skill_name}}
## Description
{{skill_description}}

## Execution Steps
1. **明确目标**：确定规划的具体目标和范围
2. **分析现状**：分析当前的情况和资源
3. **制定方案**：基于分析结果制定详细的规划方案
4. **评估方案**：评估方案的可行性和效果
5. **实施计划**：制定具体的实施步骤和时间表

## Success Criteria
- 目标明确具体
- 现状分析全面准确
- 方案科学合理
- 评估方法客观公正
- 实施计划详细可行

## Metadata
- Created at: {{created_at}}
- Status: {{status}}
- Version: {{version}}
- Category: Planning
```

## 3. 技能自动生成功能

### 3.1 技能生成器

```python
# app/evolution/generator.py
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
```

### 3.2 技能市场机制

```python
# app/evolution/marketplace.py
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
```

## 4. 使用示例

### 4.1 生成技能

```python
from app.evolution.generator import SkillGenerator

# 初始化技能生成器
generator = SkillGenerator()

# 生成技能
skill_content = generator.generate_skill(
    skill_name="市场调研",
    skill_description="执行市场调研任务，收集和分析市场数据",
    category="research",
    execution_steps=[
        {"title": "确定调研目标", "description": "明确调研的具体问题和范围"},
        {"title": "设计调研方案", "description": "制定详细的调研计划和方法"},
        {"title": "收集数据", "description": "通过各种渠道收集市场数据"},
        {"title": "分析数据", "description": "对收集到的数据进行分析和整理"},
        {"title": "生成报告", "description": "基于分析结果生成详细的调研报告"}
    ],
    success_criteria=[
        "调研目标明确具体",
        "数据收集全面准确",
        "分析方法科学合理",
        "报告内容详细完整",
        "满足用户的具体需求"
    ]
)

# 保存技能
file_path = generator.save_skill(skill_content)
print(f"技能已保存到: {file_path}")
```

### 4.2 使用技能市场

```python
from app.evolution.marketplace import SkillMarketplace

# 初始化技能市场
marketplace = SkillMarketplace()

# 添加技能到市场
marketplace.add_skill(
    skill_name="市场调研",
    skill_file="omniagent/skills/skill_market_research.md",
    category="research",
    description="执行市场调研任务，收集和分析市场数据"
)

# 获取技能列表
skills = marketplace.get_skills(category="research")
print("研究类技能:")
for skill in skills:
    print(f"- {skill['name']} (评分: {skill['rating']})")

# 评价技能
marketplace.rate_skill(
    skill_id="skill_1",
    rating=4.5,
    user_id="user_1",
    comment="非常好用的技能，帮助我完成了市场调研任务"
)

# 下载技能
file_path = marketplace.download_skill(skill_id="skill_1")
print(f"技能已下载到: {file_path}")
```

## 5. 目录结构

```
skills/
├── templates/              # 技能模板目录
│   ├── general_task.md     # 通用任务模板
│   ├── research.md         # 研究任务模板
│   ├── writing.md          # 写作任务模板
│   ├── analysis.md         # 分析任务模板
│   └── planning.md         # 规划任务模板
├── marketplace.json         # 技能市场数据
└── skill_*.md              # 生成的技能文件
```

## 6. 总结

通用技能模板和技能自动生成功能为 OmniAgent 系统提供了以下优势：

1. **标准化**：提供统一的技能结构，确保技能的一致性和可维护性
2. **效率**：通过模板快速生成技能，减少手动编写的工作量
3. **质量**：模板包含最佳实践和标准流程，提高技能质量
4. **扩展性**：支持自定义执行步骤和成功标准，适应不同任务需求
5. **市场机制**：通过技能市场促进技能的共享和评价，提高技能的可用性

这些功能将显著提升 OmniAgent 系统的技能管理能力，使系统能够更有效地处理各种类型的任务。
