#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User Management Class
Responsible for user information storage, validation and management
"""

import json
import os
import hashlib
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

class User:
    """User class"""
    def __init__(self, username: str, email: str, password_hash: str, created_at: Optional[str] = None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_login: Optional[str] = None
        self.is_active = True
    
    def to_dict(self):
        """Convert to dictionary"""
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
        """Create user object from dictionary"""
        user = cls(data["username"], data["email"], data["password_hash"], data["created_at"])
        user.last_login = data.get("last_login")
        user.is_active = data.get("is_active", True)
        return user

class UserManager:
    """User manager"""
    def __init__(self, data_file: Optional[str] = None):
        if data_file is None:
            # Get project root directory data folder path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            self.data_file = os.path.join(project_root, "data", "users.json")
        else:
            self.data_file = data_file
        self.users: Dict[str, User] = {} # Dictionary to store users, key is username, value is User object
        self.current_user: Optional[User] = None
        self.load_users()
    
    def load_users(self):
        """Load user data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for username, user_data in data.items():
                        self.users[username] = User.from_dict(user_data)
            except Exception as e:
                print(f"Failed to load user data: {e}")
                # Create default admin account
                self.create_default_admin()
        else:
            # Create default admin account
            self.create_default_admin()
    
    def save_users(self):
        """Save user data to file"""
        try:
            data = {}
            for username, user in self.users.items():
                data[username] = user.to_dict()
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save user data: {e}")
    
    def create_default_admin(self):
        """Create default admin account"""
        admin_password = self.hash_password("admin123")
        admin_user = User("admin", "admin@company.com", admin_password)
        self.users["admin"] = admin_user
        self.save_users()
    
    def hash_password(self, password: str) -> str:
        """Password hashing"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        if len(password) > 20:
            return False, "Password cannot exceed 20 characters"
        if not re.search(r'[a-zA-Z]', password):
            return False, "Password must contain letters"
        if not re.search(r'\d', password):
            return False, "Password must contain numbers"
        return True, "Password strength meets requirements"
    
    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """Register user"""
        # Validate username
        if not username or len(username.strip()) < 3:
            return False, "Username must be at least 3 characters long"
        
        username = username.strip()
        if username in self.users:
            return False, "Username already exists"
        
        # Validate email
        if not self.validate_email(email):
            return False, "Invalid email format"
        
        # Check if email is already used
        for user in self.users.values():
            if user.email == email:
                return False, "Email already registered"
        
        # Validate password
        is_valid, msg = self.validate_password(password)
        if not is_valid:
            return False, msg
        
        # Create user
        password_hash = self.hash_password(password)
        new_user = User(username, email, password_hash)
        self.users[username] = new_user
        self.save_users()
        
        return True, "Registration successful"
    
    def login_user(self, account: str, password: str) -> Tuple[bool, str]:
        """User login"""
        if account not in self.users:
            for user in self.users.values():
                if user.email == account:
                    flag=1 #Email login
                    break
            else:
                return False, "User does not exist"
        else:
            flag=0 #Username login
            user=self.users[account]
        
        if not user.is_active:
                return False, "Account has been disabled"

        password_hash = self.hash_password(password)
        if user.password_hash != password_hash:
            return False, "Incorrect password"
        
        # Update login time
        user.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.current_user = user
        self.save_users()
        
        return True, "Login successful"
    
    def guest_login(self) -> Tuple[bool, str]:
        """Guest login"""
        guest_user = User("Guest", "guest@temp.com", "")
        guest_user.username = f"Guest_{datetime.now().strftime('%H%M%S')}"
        self.current_user = guest_user
        return True, "Guest login successful"
    
    def logout(self):
        """User logout"""
        self.current_user = None

    def reset_password(self, email: str, password: str) -> Tuple[bool, str]:
        """Reset password"""
        for user in self.users.values():
            if user.email == email:
                if not self.validate_email(email):
                    return False, "Invalid email format"
                elif not (result := self.validate_password(password)[1]):
                    return False, result
                # Update password
                user.password_hash = self.hash_password(password)
                self.save_users()
                return True, "Password reset successful!\n"
        
        return False, "Email does not exist"
    
    def change_password(self, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change password"""
        if not self.current_user:
            return False, "Please log in first"
        
        # Validate old password
        old_hash = self.hash_password(old_password)
        if self.current_user.password_hash != old_hash:
            return False, "Original password is incorrect"
        
        # Validate new password
        is_valid, msg = self.validate_password(new_password)
        if not is_valid:
            return False, msg
        
        # Update password
        self.current_user.password_hash = self.hash_password(new_password)
        self.users[self.current_user.username] = self.current_user
        self.save_users()
        
        return True, "Password changed successfully"
    
    def get_user_info(self) -> dict:
        """Get current user information"""
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
        """Check if username exists"""
        return username.strip() in self.users
    
    def email_exists(self, email: str) -> bool:
        """Check if email exists"""
        for user in self.users.values():
            if user.email == email:
                return True
        return False
    
    def reset_password_by_email(self, email: str, new_password: str) -> bool:
        """Reset password by email"""
        success, message = self.reset_password(email, new_password)
        return success
