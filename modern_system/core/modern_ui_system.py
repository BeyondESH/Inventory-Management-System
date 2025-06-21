#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Food Service Management System Interface
A graphical interface management system with a modern design style
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import datetime
from typing import Dict, List, Any
import json

# Import various modules
try:
    from ..modules.modern_sales_module import ModernSalesModule
    from ..modules.modern_inventory_module import ModernInventoryModule
    from ..modules.modern_meal_module import ModernMealModule
    from ..modules.modern_order_module import ModernOrderModule
    from ..modules.modern_customer_module import ModernCustomerModule
    from ..modules.modern_finance_module import ModernFinanceModule
    from ..modules.modern_employee_module import ModernEmployeeModule
    from ..ui.meituan_charts_module import ModernChartsModule
    from ..utils.data_manager import data_manager
except ImportError:
    import sys
    import os
    # Add module path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    modules_dir = os.path.join(os.path.dirname(current_dir), 'modules')
    ui_dir = os.path.join(os.path.dirname(current_dir), 'ui')
    utils_dir = os.path.join(os.path.dirname(current_dir), 'utils')
    sys.path.insert(0, modules_dir)
    sys.path.insert(0, ui_dir)
    sys.path.insert(0, utils_dir)
    
    try:
        from modern_sales_module import ModernSalesModule
        from modern_inventory_module import ModernInventoryModule
        from modern_meal_module import ModernMealModule
        from modern_order_module import ModernOrderModule
        from modern_customer_module import ModernCustomerModule
        from modern_finance_module import ModernFinanceModule
        from modern_employee_module import ModernEmployeeModule
        from meituan_charts_module import ModernChartsModule
        from data_manager import data_manager
    except ImportError as e:
        print(f"Failed to import modules: {e}")
        # Create simple mock classes
        class MockModule:
            def __init__(self, *args, **kwargs):
                pass
            def show(self):
                pass
        
        ModernSalesModule = MockModule
        ModernInventoryModule = MockModule
        ModernMealModule = MockModule
        ModernOrderModule = MockModule
        ModernCustomerModule = MockModule
        ModernFinanceModule = MockModule
        ModernEmployeeModule = MockModule
        ModernChartsModule = MockModule
        
        class MockDataManager:
            def get_dashboard_stats(self):
                return {
                    'today_sales': 12580,
                    'order_count': 156,
                    'inventory_alerts': 8,
                    'customer_count': 2340
                }
        data_manager = MockDataManager()

class ModernFoodServiceSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Restaurant Management System")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f8f9fa")
        self.root.resizable(True, True)
        
        # Modern color theme
        self.colors = {
            'primary': '#FF6B35',      # Main color - Orange Red
            'secondary': '#F7931E',    # Secondary color - Orange
            'accent': '#FFD23F',       # Accent color - Yellow
            'background': '#F8F9FA',   # Background color
            'surface': '#FFFFFF',      # Card background
            'text_primary': '#2D3436', # Primary text
            'text_secondary': '#636E72', # Secondary text
            'success': '#00B894',      # Success color
            'warning': '#FDCB6E',      # Warning color
            'error': '#E84393',        # Error color
            'border': '#E0E0E0',       # Border color
            'sidebar': '#2D3436',      # Sidebar background
            'nav_hover': '#636E72'     # Navigation hover
        }
        # Font configuration
        self.fonts = {
            'title': ('Segoe UI', 18, 'bold'),
            'heading': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 12),
            'small': ('Segoe UI', 10),
            'nav': ('Segoe UI', 13, 'bold'),
            'breadcrumb': ('Segoe UI', 11)
        }
        
        # Current module
        self.current_module = "sales"
        
        # Module definitions (dashboard removed)
        self.modules = {
            "sales": {"text": "Sales", "icon": "💰"},
            "inventory": {"text": "Inventory", "icon": "📦"},
            "meal": {"text": "Meals", "icon": "🍽️"},
            "order": {"text": "Orders", "icon": "📋"},
            "customer": {"text": "Customers", "icon": "👥"},
            "employee": {"text": "Employees", "icon": "👤"},
            "finance": {"text": "Finance", "icon": "💼"},
            "charts": {"text": "Dashboard", "icon": "📈"}
        }
        
        # Initialize UI
        self.setup_window()
        self.create_modern_layout()
        self.create_modern_widgets()
        self.init_modules()
        self.update_content_area()
        
    def setup_window(self):
        """Set window properties"""
        # Set icon
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            icon_path = os.path.join(project_root, "image", "icon", "main.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
    
    def create_modern_layout(self):
        """Create modern layout"""
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.colors['background'])
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Top navigation bar
        self.top_nav = tk.Frame(self.main_container, bg=self.colors['surface'], height=70)
        self.top_nav.pack(fill="x", side="top")
        self.top_nav.pack_propagate(False)
        
        # Main content area
        self.content_container = tk.Frame(self.main_container, bg=self.colors['background'])
        self.content_container.pack(fill="both", expand=True)
        
        # Left navigation panel
        self.sidebar = tk.Frame(self.content_container, bg=self.colors['sidebar'], width=280)
        self.sidebar.pack(side="left", fill="y", padx=(0, 0))
        self.sidebar.pack_propagate(False)
        
        # Right content area
        self.main_content = tk.Frame(self.content_container, bg=self.colors['background'])
        self.main_content.pack(side="right", fill="both", expand=True, padx=(20, 20), pady=(20, 20))
        
    def create_modern_widgets(self):
        """Create modern UI elements"""
        self.create_top_navigation()
        self.create_sidebar_navigation()
        self.create_content_area()
        
    def create_top_navigation(self):
        """Create top navigation bar"""
        # Left logo and title
        logo_frame = tk.Frame(self.top_nav, bg=self.colors['surface'])
        logo_frame.pack(side="left", fill="y", padx=20)
        
        # System icon
        icon_label = tk.Label(logo_frame, text="🍽️", font=('Segoe UI Emoji', 24), 
                             bg=self.colors['surface'], fg=self.colors['primary'])
        icon_label.pack(side="left", padx=(0, 10), pady=15)
        
        # System title
        title_label = tk.Label(logo_frame, text="Foodie POS", font=self.fonts['title'], 
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(side="left", pady=15)
        
        # Right user info
        user_frame = tk.Frame(self.top_nav, bg=self.colors['surface'])
        user_frame.pack(side="right", fill="y", padx=20)
        
        # Current time
        time_label = tk.Label(user_frame, text=datetime.datetime.now().strftime("%H:%M"),
                             font=self.fonts['body'], bg=self.colors['surface'], 
                             fg=self.colors['text_secondary'])
        time_label.pack(side="right", padx=(10, 0), pady=15)
        
        # User info
        user_label = tk.Label(user_frame, text="👤 Admin", font=self.fonts['body'],
                             bg=self.colors['surface'], fg=self.colors['text_secondary'])
        user_label.pack(side="right", pady=15)

    def create_sidebar_navigation(self):
        """Create sidebar navigation"""
        # Navigation title
        nav_title = tk.Label(self.sidebar, text="System Navigation", font=self.fonts['heading'],
                           bg=self.colors['sidebar'], fg='white', pady=20)
        nav_title.pack(fill="x")
        
        # Navigation button container
        self.nav_buttons = {}
        
        for module_id, module_info in self.modules.items():
            btn_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'])
            btn_frame.pack(fill="x", padx=10, pady=2)
            
            # Create navigation button
            btn = tk.Button(btn_frame, 
                          text=f"{module_info['icon']} {module_info['text']}",
                          font=self.fonts['nav'],
                          bg=self.colors['sidebar'] if module_id != self.current_module else self.colors['primary'],
                          fg='white',
                          bd=0,
                          pady=12,
                          cursor="hand2",
                          anchor="center",
                          command=lambda mid=module_id: self.switch_module(mid))
            btn.pack(fill="x")
            
            # Hover effect
            def on_enter(e, button=btn, mid=module_id):
                if mid != self.current_module:
                    button.configure(bg=self.colors['nav_hover'])
            
            def on_leave(e, button=btn, mid=module_id):
                if mid != self.current_module:
                    button.configure(bg=self.colors['sidebar'])
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            
            self.nav_buttons[module_id] = btn

    def create_content_area(self):
        """Create content area structure"""
        # Title bar for breadcrumb and module-specific actions
        self.title_frame = tk.Frame(self.main_content, bg=self.colors['background'])
        self.title_frame.pack(fill="x", pady=(0, 15))
        
        # Main content frame for module content
        self.content_frame = tk.Frame(self.main_content, bg=self.colors['background'])
        self.content_frame.pack(fill="both", expand=True)

    def switch_module(self, module_id):
        """Switch to a different module"""
        if module_id == self.current_module:
            return  # Do nothing if already on the same module
            
        print(f"Switching to module: {module_id}")
        self.current_module = module_id
        
        # Update navigation button styles
        for mid, btn in self.nav_buttons.items():
            if mid == module_id:
                btn.configure(bg=self.colors['primary'])
            else:
                btn.configure(bg=self.colors['sidebar'])
        
        self.update_content_area()

    def update_breadcrumb(self):
        """Update breadcrumb navigation. This is now handled by each module."""
        pass # The breadcrumb is part of the title_frame, which is now managed by modules.

    def init_modules(self):
        """Initialize all modules"""
        self.module_instances = {}
        
        # Pass both content_frame and title_frame to each module
        self.module_instances["sales"] = ModernSalesModule(self.content_frame, self.title_frame)
        self.module_instances["inventory"] = ModernInventoryModule(self.content_frame, self.title_frame)
        self.module_instances["meal"] = ModernMealModule(self.content_frame, self.title_frame)
        self.module_instances["order"] = ModernOrderModule(self.content_frame, self.title_frame)
        self.module_instances["customer"] = ModernCustomerModule(self.content_frame, self.title_frame)
        self.module_instances["employee"] = ModernEmployeeModule(self.content_frame, self.title_frame)
        self.module_instances["finance"] = ModernFinanceModule(self.content_frame, self.title_frame)
        self.module_instances["charts"] = ModernChartsModule(self.content_frame, self.title_frame)
        
        print("All modules initialized.")

    def update_content_area(self):
        """Update the main content area based on the current module"""
        # The modules themselves will now handle clearing and drawing their content
        # in the frames provided to them.
        try:
            module_to_show = self.module_instances[self.current_module]
            module_to_show.show()
        except Exception as e:
            messagebox.showerror("Module Error", f"Failed to load module: {self.current_module}\n\nError: {e}")
            print(f"Error showing module {self.current_module}: {e}")

    def run(self):
        """Start the main application loop"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Runtime Error", f"An unexpected error occurred: {e}")
            print(f"Runtime error: {e}")

def main():
    """Main function to run the application"""
    try:
        app = ModernFoodServiceSystem()
        app.run()
    except Exception as e:
        messagebox.showerror("Startup Error", f"Failed to start main system: {e}")
        print(f"Failed to start main system: {e}")

if __name__ == '__main__':
    main()
