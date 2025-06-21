#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Food Service Company Management System Launcher
"""

import tkinter as tk

# Support two import methods: package import and direct run
try:
    from ..modules.modern_login_module import ModernLoginModule
    from .modern_ui_system import ModernFoodServiceSystem
except ImportError:
    import sys
    import os
    # Add module path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    modules_dir = os.path.join(os.path.dirname(current_dir), 'modules')
    sys.path.insert(0, modules_dir)
    sys.path.insert(0, current_dir)
    from modern_login_module import ModernLoginModule
    from modern_ui_system import ModernFoodServiceSystem

class SystemLauncher:
    def __init__(self):
        pass
        
    def start_main_system(self, user_info):
        """Start main management system"""
        app = ModernFoodServiceSystem()
        # Pass user information to main system
        if hasattr(app, 'set_user_info'):
            app.set_user_info(user_info)
        app.run()
        
    def run(self):
        """Run system launcher"""
        # Create login module, pass callback function for successful login
        login = ModernLoginModule(on_login_success=self.start_main_system)
        login.run()

if __name__ == "__main__":
    launcher = SystemLauncher()
    launcher.run()
