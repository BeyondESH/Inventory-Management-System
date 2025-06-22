#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Smart Restaurant Management System startup file
Directly starts the modern login interface
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk

# 获取项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
modern_system_dir = os.path.join(current_dir, 'modern_system')

# 添加路径到系统路径
sys.path.insert(0, current_dir)
sys.path.insert(0, modern_system_dir)
sys.path.insert(0, os.path.join(modern_system_dir, 'modules'))
sys.path.insert(0, os.path.join(modern_system_dir, 'core'))

def show_startup_splash():
    """Display startup splash screen"""
    splash = tk.Tk()
    splash.title("Smart Restaurant Management System")
    splash.geometry("400x300")
    splash.configure(bg="#FF6B35")
    splash.resizable(False, False)
    
    # Center the window
    splash.eval('tk::PlaceWindow . center')
    
    # Icon and title
    title_frame = tk.Frame(splash, bg="#FF6B35")
    title_frame.pack(expand=True, fill="both")
    
    # System icon
    icon_label = tk.Label(title_frame, text="🍽️", font=('Segoe UI Emoji', 48), 
                         bg="#FF6B35", fg="white")
    icon_label.pack(pady=(60, 20))
    
    # System title
    title_label = tk.Label(title_frame, text="Smart Restaurant System", 
                          font=('Segoe UI', 20, 'bold'),
                          bg="#FF6B35", fg="white")
    title_label.pack(pady=(0, 10))
    
    # Version info
    version_label = tk.Label(title_frame, text="Modern Version v2.0", 
                            font=('Segoe UI', 12),
                            bg="#FF6B35", fg="white")
    version_label.pack(pady=(0, 30))
    
    # Progress bar
    progress_frame = tk.Frame(title_frame, bg="#FF6B35")
    progress_frame.pack(fill="x", padx=50)
    
    progress = ttk.Progressbar(progress_frame, mode='indeterminate', length=300)
    progress.pack()
    progress.start()
    
    # Status label
    status_label = tk.Label(title_frame, text="Loading system components...", 
                           font=('Segoe UI', 10),
                           bg="#FF6B35", fg="white")
    status_label.pack(pady=(20, 0))
    
    # Auto-close with safe progress bar handling
    def safe_close():
        try:
            progress.stop()
        except tk.TclError:
            pass  # Progress bar already destroyed
        splash.destroy()
    
    splash.after(3000, safe_close)
    splash.mainloop()

def main():
    """Main startup function"""
    try:
        print("=" * 50)
        print("Starting Smart Restaurant Management System...")
        print("=" * 50)
        
        # Define login success callback
        def on_login_success(user_info, login_window):
            print(f"User login successful: {user_info['name']}")
            try:
                # Close login window if it exists
                if login_window:
                    login_window.destroy()
                
                # Import main UI system
                try:
                    from modern_system.core.modern_ui_system import ModernFoodServiceSystem
                    print("✓ Main system imported successfully")
                except ImportError as e:
                    print(f"✗ Failed to import main system: {e}")
                    try:
                        # Fallback import
                        sys.path.append(os.path.join(modern_system_dir, 'core'))
                        from modern_ui_system import ModernFoodServiceSystem
                        print("✓ Imported main system using fallback path")
                    except ImportError as e2:
                        print(f"✗ Fallback import of main system also failed: {e2}")
                        messagebox.showerror("Import Error", f"Cannot import main system: {e2}")
                        return
                
                # Create and run the main system
                main_app = ModernFoodServiceSystem()
                print("✓ Main system created, starting...")
                main_app.run()
            except Exception as e:
                print(f"✗ Failed to start main system: {e}")
                messagebox.showerror("Startup Error", f"Failed to start main system: {e}")
        
        # Show simplified login interface
        def show_simple_login():
            login_root = tk.Tk()
            login_root.title("Smart Restaurant System - Login")
            login_root.geometry("500x400")
            login_root.configure(bg="#FF6B35")
            login_root.resizable(False, False)
            
            # Center the window
            login_root.eval('tk::PlaceWindow . center')
            
            # Title area
            title_frame = tk.Frame(login_root, bg="#FF6B35")
            title_frame.pack(expand=True, fill="both", padx=40, pady=40)
            
            # System icon
            tk.Label(title_frame, text="🍽️", font=('Segoe UI Emoji', 64), 
                    bg="#FF6B35", fg="white").pack(pady=(20, 10))
            
            # System title
            tk.Label(title_frame, text="Smart Restaurant System", 
                    font=('Segoe UI', 24, 'bold'),
                    bg="#FF6B35", fg="white").pack(pady=(0, 10))
            
            # Version info
            tk.Label(title_frame, text="Modern Version v2.0", 
                    font=('Segoe UI', 14),
                    bg="#FF6B35", fg="white").pack(pady=(0, 30))
            
            # Login button
            def guest_login():
                login_root.destroy()
                on_login_success({'name': 'Guest User', 'type': 'guest'}, None)
            
            login_btn = tk.Button(title_frame, text="🚀 Launch System", 
                                font=('Segoe UI', 16, 'bold'),
                                bg="white", fg="#FF6B35",
                                padx=30, pady=15, bd=0,
                                cursor="hand2",
                                command=guest_login)
            login_btn.pack(pady=20)
            
            # Explanatory text
            tk.Label(title_frame, text="Click the button above to enter the main interface", 
                    font=('Segoe UI', 12),
                    bg="#FF6B35", fg="white").pack(pady=(10, 0))
            
            login_root.mainloop()
        
        # Try to import and use the full login module
        print("Loading login module...")
        try:
            from modern_system.modules.modern_login_module import ModernLoginModule
            print("✓ Login module imported successfully")
            app = ModernLoginModule(on_login_success)
            app.run()
        except Exception as e:
            print(f"⚠️ Full login module unavailable, using simplified login: {e}")
            show_simple_login()
        
    except Exception as e:
        error_msg = f"An error occurred during system startup: {e}"
        print(f"✗ {error_msg}")
        messagebox.showerror("System Error", error_msg)

if __name__ == "__main__":
    main()
