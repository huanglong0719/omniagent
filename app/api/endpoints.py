from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random
from app.security.auth import (
    authenticate_user, create_access_token, get_current_user, get_current_active_user,
    check_user_permission, users_db, User, UserCreate, Token, UserLogin
)

app = FastAPI()

# OAuth2 密码承载令牌
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟数据
skills = [
    {"id": 1, "name": "市场调研", "category": "research", "status": "Verified", "rating": 4.5},
    {"id": 2, "name": "文章写作", "category": "writing", "status": "Verified", "rating": 4.0},
    {"id": 3, "name": "数据分析", "category": "analysis", "status": "Verified", "rating": 4.2},
    {"id": 4, "name": "项目规划", "category": "planning", "status": "Pending Review", "rating": 3.8},
    {"id": 5, "name": "客户服务", "category": "general_task", "status": "Beta (Pending Verification)", "rating": 3.5}
]

activities = [
    {"time": datetime.now().isoformat(), "activity": "技能 \"市场调研\" 被创建", "status": "success"},
    {"time": (datetime.now().timestamp() - 3600).__str__(), "activity": "系统启动", "status": "success"},
    {"time": (datetime.now().timestamp() - 7200).__str__(), "activity": "技能 \"数据分析\" 被验证", "status": "success"},
    {"time": (datetime.now().timestamp() - 10800).__str__(), "activity": "用户登录", "status": "success"},
    {"time": (datetime.now().timestamp() - 14400).__str__(), "activity": "技能 \"项目规划\" 被更新", "status": "success"}
]

logs = [
    {"time": datetime.now().isoformat(), "level": "INFO", "message": "系统启动成功"},
    {"time": (datetime.now().timestamp() - 3600).__str__(), "level": "INFO", "message": "技能 \"市场调研\" 被创建"},
    {"time": (datetime.now().timestamp() - 7200).__str__(), "level": "INFO", "message": "技能 \"数据分析\" 被验证"},
    {"time": (datetime.now().timestamp() - 10800).__str__(), "level": "WARN", "message": "内存使用接近阈值"},
    {"time": (datetime.now().timestamp() - 14400).__str__(), "level": "INFO", "message": "用户登录成功"}
]

# 系统状态接口
@app.get("/system/status")
async def get_system_status():
    return {
        "health": "healthy",
        "cpu_usage": random.uniform(10, 20),
        "memory_usage": random.uniform(40, 50),
        "skill_count": len(skills),
        "active_sessions": random.randint(1, 10)
    }

# 技能列表接口
@app.get("/skills")
async def get_skills():
    return skills

# 创建技能接口
@app.post("/skills")
async def create_skill(skill: Dict):
    new_skill = {
        "id": len(skills) + 1,
        "name": skill.get("name"),
        "category": skill.get("category", "general_task"),
        "status": "Beta (Pending Verification)",
        "rating": 0,
        "description": skill.get("description", ""),
        "steps": skill.get("steps", ""),
        "criteria": skill.get("criteria", "")
    }
    skills.append(new_skill)
    return new_skill

# 更新技能接口
@app.put("/skills/{skill_id}")
async def update_skill(skill_id: int, skill: Dict):
    for s in skills:
        if s["id"] == skill_id:
            s.update(skill)
            return s
    raise HTTPException(status_code=404, detail="Skill not found")

# 删除技能接口
@app.delete("/skills/{skill_id}")
async def delete_skill(skill_id: int):
    for i, s in enumerate(skills):
        if s["id"] == skill_id:
            skills.pop(i)
            return {"message": "Skill deleted successfully"}
    raise HTTPException(status_code=404, detail="Skill not found")

# 验证技能接口
@app.put("/skills/{skill_id}/verify")
async def verify_skill(skill_id: int):
    for s in skills:
        if s["id"] == skill_id:
            s["status"] = "Verified"
            return s
    raise HTTPException(status_code=404, detail="Skill not found")

# 最近活动接口
@app.get("/activities")
async def get_activities():
    return activities

# 系统日志接口
@app.get("/logs")
async def get_logs():
    return logs

# 监控数据接口
@app.get("/monitoring")
async def get_monitoring_data(token: str = Depends(oauth2_scheme)):
    current_user = get_current_active_user(get_current_user(token))
    return {
        "response_time": [random.uniform(100, 300) for _ in range(6)],
        "request_count": [random.randint(100, 300) for _ in range(6)],
        "skill_usage": [random.randint(40, 120) for _ in range(5)]
    }

# 令牌获取接口
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 用户注册接口
@app.post("/register")
async def register(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    # 检查密码长度，bcrypt 限制密码长度不超过 72 字节
    if len(user.password) > 72:
        raise HTTPException(status_code=400, detail="Password cannot be longer than 72 characters")
    hashed_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # 模拟加密
    users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": hashed_password,
        "disabled": False,
        "role": user.role
    }
    return {"message": "User registered successfully"}

# 获取当前用户信息接口
@app.get("/users/me", response_model=User)
async def get_current_user_info(token: str = Depends(oauth2_scheme)):
    current_user = get_current_active_user(get_current_user(token))
    return current_user

# 需要管理员权限的接口
@app.get("/admin")
async def admin_only(token: str = Depends(oauth2_scheme)):
    current_user = get_current_active_user(get_current_user(token))
    if not check_user_permission(current_user, "admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return {"message": "Admin access granted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)