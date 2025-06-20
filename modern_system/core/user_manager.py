#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户管理类
负责用户信息的存储、验证和管理
"""

import json
import os
import hashlib
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

class User:
    """用户类"""
    def __init__(self, username: str, email: str, password_hash: str, created_at: Optional[str] = None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_login: Optional[str] = None
        self.is_active = True
    
    def to_dict(self):
        """转换为字典"""
        return {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建用户对象"""
        user = cls(data["username"], data["email"], data["password_hash"], data["created_at"])
        user.last_login = data.get("last_login")
        user.is_active = data.get("is_active", True)
        return user

class UserManager:
    """用户管理器"""
    def __init__(self, data_file: Optional[str] = None):
        if data_file is None:
            # 获取项目根目录的data文件夹路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            self.data_file = os.path.join(project_root, "data", "users.json")
        else:
            self.data_file = data_file
        self.users: Dict[str, User] = {} # 存储用户的字典，键为用户名，值为User对象
        self.current_user: Optional[User] = None
        self.load_users()
    
    def load_users(self):
        """从文件加载用户数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for username, user_data in data.items():
                        self.users[username] = User.from_dict(user_data)
            except Exception as e:
                print(f"加载用户数据失败: {e}")
                # 创建默认管理员账户
                self.create_default_admin()
        else:
            # 创建默认管理员账户
            self.create_default_admin()
    
    def save_users(self):
        """保存用户数据到文件"""
        try:
            data = {}
            for username, user in self.users.items():
                data[username] = user.to_dict()
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存用户数据失败: {e}")
    
    def create_default_admin(self):
        """创建默认管理员账户"""
        admin_password = self.hash_password("admin123")
        admin_user = User("admin", "admin@company.com", admin_password)
        self.users["admin"] = admin_user
        self.save_users()
    
    def hash_password(self, password: str) -> str:
        """密码哈希"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def validate_email(self, email: str) -> bool:
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """验证密码强度"""
        if len(password) < 6:
            return False, "密码长度至少6位"
        if len(password) > 20:
            return False, "密码长度不能超过20位"
        if not re.search(r'[a-zA-Z]', password):
            return False, "密码必须包含字母"
        if not re.search(r'\d', password):
            return False, "密码必须包含数字"
        return True, "密码强度符合要求"
    
    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """注册用户"""
        # 验证用户名
        if not username or len(username.strip()) < 3:
            return False, "用户名长度至少3位"
        
        username = username.strip()
        if username in self.users:
            return False, "用户名已存在"
        
        # 验证邮箱
        if not self.validate_email(email):
            return False, "邮箱格式不正确"
        
        # 检查邮箱是否已被使用
        for user in self.users.values():
            if user.email == email:
                return False, "邮箱已被注册"
        
        # 验证密码
        is_valid, msg = self.validate_password(password)
        if not is_valid:
            return False, msg
        
        # 创建用户
        password_hash = self.hash_password(password)
        new_user = User(username, email, password_hash)
        self.users[username] = new_user
        self.save_users()
        
        return True, "注册成功"
    
    def login_user(self, account: str, password: str) -> Tuple[bool, str]:
        """用户登录"""
        if account not in self.users:
            for user in self.users.values():
                if user.email == account:
                    flag=1 #邮箱登录
                    break
            else:
                return False, "用户不存在"
        else:
            flag=0 #用户名登录
            user=self.users[account]
        
        if not user.is_active:
                return False, "账户已被禁用"

        password_hash = self.hash_password(password)
        if user.password_hash != password_hash:
            return False, "密码错误"
        
        # 更新登录时间
        user.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.current_user = user
        self.save_users()
        
        return True, "登录成功"
    
    def guest_login(self) -> Tuple[bool, str]:
        """游客登录"""
        guest_user = User("游客", "guest@temp.com", "")
        guest_user.username = f"游客_{datetime.now().strftime('%H%M%S')}"
        self.current_user = guest_user
        return True, "游客登录成功"
    
    def logout(self):
        """用户登出"""
        self.current_user = None

    def reset_password(self, email: str, password: str) -> Tuple[bool, str]:
        """重置密码"""
        for user in self.users.values():
            if user.email == email:
                if not self.validate_email(email):
                    return False, "邮箱格式不正确"
                elif not (result := self.validate_password(password)[1]):
                    return False, result
                # 更新密码
                user.password_hash = self.hash_password(password)
                self.save_users()
                return True, "密码重置成功！\n"
        
        return False, "邮箱不存在"
    
    def change_password(self, old_password: str, new_password: str) -> Tuple[bool, str]:
        """修改密码"""
        if not self.current_user:
            return False, "请先登录"
        
        # 验证旧密码
        old_hash = self.hash_password(old_password)
        if self.current_user.password_hash != old_hash:
            return False, "原密码错误"
        
        # 验证新密码
        is_valid, msg = self.validate_password(new_password)
        if not is_valid:
            return False, msg
        
        # 更新密码
        self.current_user.password_hash = self.hash_password(new_password)
        self.users[self.current_user.username] = self.current_user
        self.save_users()
        
        return True, "密码修改成功"
    
    def get_user_info(self) -> dict:
        """获取当前用户信息"""
        if not self.current_user:
            return {}
        
        return {
            "username": self.current_user.username,
            "email": self.current_user.email,
            "created_at": self.current_user.created_at,
            "last_login": self.current_user.last_login,
            "is_active": self.current_user.is_active
        }
    
    def user_exists(self, username: str) -> bool:
        """检查用户名是否存在"""
        return username.strip() in self.users
    
    def email_exists(self, email: str) -> bool:
        """检查邮箱是否存在"""
        for user in self.users.values():
            if user.email == email:
                return True
        return False
    
    def reset_password_by_email(self, email: str, new_password: str) -> bool:
        """通过邮箱重置密码"""
        success, message = self.reset_password(email, new_password)
        return success
