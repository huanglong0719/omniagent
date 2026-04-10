from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# 配置
SECRET_KEY = "your-secret-key-here"  # 在生产环境中应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 密码加密上下文
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# 模拟用户数据库
users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": pwd_context.hash("admin123"),
        "disabled": False,
        "role": "admin"
    },
    "user": {
        "username": "user",
        "full_name": "Regular User",
        "email": "user@example.com",
        "hashed_password": pwd_context.hash("user123"),
        "disabled": False,
        "role": "user"
    }
}

# 数据模型
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: Optional[str] = None

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# 密码验证
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 获取用户
def get_user(db: Dict[str, Any], username: str) -> Optional[UserInDB]:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

# 验证用户
def authenticate_user(db: Dict[str, Any], username: str, password: str) -> Optional[UserInDB]:
    user = get_user(db, username)
    if not user:
        return None
    # 检查密码长度，bcrypt 限制密码长度不超过 72 字节
    if len(password) > 72:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# 创建访问令牌
def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 验证令牌
def verify_token(token: str, credentials_exception) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception

# 获取当前用户
def get_current_user(token: str) -> User:
    credentials_exception = Exception("Could not validate credentials")
    token_data = verify_token(token, credentials_exception)
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    if user.disabled:
        raise Exception("Inactive user")
    return user

# 获取当前活跃用户
def get_current_active_user(current_user: User) -> User:
    if current_user.disabled:
        raise Exception("Inactive user")
    return current_user

# 检查用户权限
def check_user_permission(current_user: User, required_role: str) -> bool:
    if required_role == "admin" and current_user.role != "admin":
        return False
    return True