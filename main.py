import tkinter as tk
from tkinter import ttk, messagebox
from auth_functions import AuthManager 
from dashboard import start_dashboard

class ModernLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Citizen Help Portal")
        self.root.geometry("1000x850")
        self.root.configure(bg='#ffffff')
        self.root.resizable(False, False)
        
        self.COLORS = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'light_bg': '#ecf0f1',
            'white': '#ffffff',
            'text_dark': '#2c3e50',
            'text_light': '#7f8c8d'
        }
        
        self.FONTS = {
            'title': ('Arial', 24, 'bold'),
            'header': ('Arial', 16, 'bold'),
            'body': ('Arial', 10),
            'small': ('Arial', 9),
            'button': ('Arial', 11, 'bold')
        }
        
        self.auth = AuthManager()
        self.current_user = None
        
        self.setup_ui()

    def setup_ui(self):
        self.create_login_screen()
        self.create_register_screen()
        self.show_frame('login')

    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root, bg=self.COLORS['white'])
        
        main_container = tk.Frame(self.login_frame, bg=self.COLORS['light_bg'], relief='raised', bd=1)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        container = tk.Frame(main_container, bg=self.COLORS['light_bg'])
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left side
        left_frame = tk.Frame(container, bg=self.COLORS['primary'])
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        branding_frame = tk.Frame(left_frame, bg=self.COLORS['primary'])
        branding_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(branding_frame, text="🏛️", font=('Arial', 48), bg=self.COLORS['primary'], fg='white').pack(pady=10)
        tk.Label(branding_frame, text="Smart Citizen Portal", font=self.FONTS['title'], bg=self.COLORS['primary'], fg='white').pack(pady=5)
        tk.Label(branding_frame, text="Digital Government Services", font=self.FONTS['body'], bg=self.COLORS['primary'], fg=self.COLORS['light_bg']).pack(pady=5)
        
        # Right side
        right_frame = tk.Frame(container, bg=self.COLORS['white'])
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        form_container = tk.Frame(right_frame, bg=self.COLORS['white'])
        form_container.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(form_container, text="Welcome Back", font=self.FONTS['header'], bg=self.COLORS['white'], fg=self.COLORS['primary']).pack(pady=20)
        tk.Label(form_container, text="Sign in to your account", font=self.FONTS['body'], bg=self.COLORS['white'], fg=self.COLORS['text_light']).pack(pady=5)
        
        input_frame = tk.Frame(form_container, bg=self.COLORS['white'])
        input_frame.pack(pady=30)
        
        # Username
        username_frame = tk.Frame(input_frame, bg=self.COLORS['white'])
        username_frame.pack(fill='x', pady=10)
        tk.Label(username_frame, text="USERNAME", font=self.FONTS['small'], bg=self.COLORS['white'], fg=self.COLORS['text_light'], anchor='w').pack(anchor='w')
        self.login_username = tk.Entry(username_frame, width=25, font=self.FONTS['body'], relief='solid', bd=1, bg=self.COLORS['light_bg'])
        self.login_username.pack(fill='x', pady=5, ipady=8)
        self.login_username.bind('<Return>', lambda e: self.handle_login())
        
        # Password
        password_frame = tk.Frame(input_frame, bg=self.COLORS['white'])
        password_frame.pack(fill='x', pady=15)
        tk.Label(password_frame, text="PASSWORD", font=self.FONTS['small'], bg=self.COLORS['white'], fg=self.COLORS['text_light'], anchor='w').pack(anchor='w')
        self.login_password = tk.Entry(password_frame, show='*', width=25, font=self.FONTS['body'], relief='solid', bd=1, bg=self.COLORS['light_bg'])
        self.login_password.pack(fill='x', pady=5, ipady=8)
        self.login_password.bind('<Return>', lambda e: self.handle_login())
        
        # Login button
        tk.Button(input_frame, text="SIGN IN", font=self.FONTS['button'], bg=self.COLORS['secondary'], fg='white', relief='raised', bd=0, cursor='hand2', command=self.handle_login).pack(fill='x', pady=20, ipady=10)
        
        # Register link
        register_frame = tk.Frame(input_frame, bg=self.COLORS['white'])
        register_frame.pack(fill='x', pady=10)
        tk.Label(register_frame, text="Don't have an account?", font=self.FONTS['small'], bg=self.COLORS['white'], fg=self.COLORS['text_light']).pack(side='left')
        tk.Button(register_frame, text="Create Account", font=self.FONTS['small'], bg=self.COLORS['white'], fg=self.COLORS['secondary'], relief='flat', cursor='hand2', command=lambda: self.show_frame('register')).pack(side='left', padx=5)
        
        # Footer
        footer_frame = tk.Frame(right_frame, bg=self.COLORS['white'])
        footer_frame.pack(side='bottom', fill='x', pady=20)
        tk.Label(footer_frame, text="Default Admin: admin / admin123", font=self.FONTS['small'], bg=self.COLORS['white'], fg=self.COLORS['text_light']).pack()

    def create_register_screen(self):
        self.register_frame = tk.Frame(self.root, bg=self.COLORS['white'])
        
        main_container = tk.Frame(self.register_frame, bg=self.COLORS['light_bg'], relief='raised', bd=1)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.COLORS['light_bg'])
        header_frame.pack(fill='x', pady=10)
        tk.Button(header_frame, text="← Back to Login", font=self.FONTS['body'], bg=self.COLORS['light_bg'], fg=self.COLORS['secondary'], relief='flat', cursor='hand2', command=lambda: self.show_frame('login')).pack(side='left', padx=20)
        
        # Title
        title_frame = tk.Frame(main_container, bg=self.COLORS['light_bg'])
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Create New Account", font=self.FONTS['header'], bg=self.COLORS['light_bg'], fg=self.COLORS['primary']).pack()
        tk.Label(title_frame, text="Join our government service portal", font=self.FONTS['body'], bg=self.COLORS['light_bg'], fg=self.COLORS['text_light']).pack(pady=5)
        
        # Form container
        form_container = tk.Frame(main_container, bg=self.COLORS['white'])
        form_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollable frame
        canvas = tk.Canvas(form_container, bg=self.COLORS['white'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.COLORS['white'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Personal Information
        personal_frame = tk.LabelFrame(scrollable_frame, text=" Personal Information ", font=self.FONTS['body'], bg=self.COLORS['white'], fg=self.COLORS['primary'], relief='solid', bd=1)
        personal_frame.pack(fill='x', pady=10, padx=10)
        
        personal_fields = [
            ("Full Name", "text", True),
            ("Email Address", "text", False),
            ("Phone Number", "text", True),
            ("NID Number", "text", True),
            ("Date of Birth (YYYY-MM-DD)", "text", True),
            ("Address", "text", True)
        ]
        
        self.reg_entries = {}
        
        for label, field_type, required in personal_fields:
            row_frame = tk.Frame(personal_frame, bg=self.COLORS['white'])
            row_frame.pack(fill='x', pady=8, padx=10)
            label_text = f"{label}{' *' if required else ''}"
            tk.Label(row_frame, text=label_text, font=self.FONTS['body'], bg=self.COLORS['white'], fg=self.COLORS['text_dark'], width=20, anchor='w').pack(side='left')
            entry = tk.Entry(row_frame, width=30, font=self.FONTS['body'], relief='solid', bd=1)
            entry.pack(side='left', fill='x', expand=True, padx=(10, 0), ipady=4)
            self.reg_entries[label] = entry
        
        # Account Information
        account_frame = tk.LabelFrame(scrollable_frame, text=" Account Information ", font=self.FONTS['body'], bg=self.COLORS['white'], fg=self.COLORS['primary'], relief='solid', bd=1)
        account_frame.pack(fill='x', pady=10, padx=10)
        
        # Username
        user_frame = tk.Frame(account_frame, bg=self.COLORS['white'])
        user_frame.pack(fill='x', pady=8, padx=10)
        tk.Label(user_frame, text="Username *", font=self.FONTS['body'], bg=self.COLORS['white'], fg=self.COLORS['text_dark'], width=20, anchor='w').pack(side='left')
        self.reg_entries['Username'] = tk.Entry(user_frame, width=30, font=self.FONTS['body'], relief='solid', bd=1)
        self.reg_entries['Username'].pack(side='left', fill='x', expand=True, padx=(10, 0), ipady=4)
        
        # Password
        pass_frame = tk.Frame(account_frame, bg=self.COLORS['white'])
        pass_frame.pack(fill='x', pady=8, padx=10)
        tk.Label(pass_frame, text="Password *", font=self.FONTS['body'], bg=self.COLORS['white'], fg=self.COLORS['text_dark'], width=20, anchor='w').pack(side='left')
        self.reg_entries['Password'] = tk.Entry(pass_frame, show='*', width=30, font=self.FONTS['body'], relief='solid', bd=1)
        self.reg_entries['Password'].pack(side='left', fill='x', expand=True, padx=(10, 0), ipady=4)
        
        # Confirm Password
        confirm_frame = tk.Frame(account_frame, bg=self.COLORS['white'])
        confirm_frame.pack(fill='x', pady=8, padx=10)
        tk.Label(confirm_frame, text="Confirm Password *", font=self.FONTS['body'], bg=self.COLORS['white'], fg=self.COLORS['text_dark'], width=20, anchor='w').pack(side='left')
        self.reg_entries['Confirm Password'] = tk.Entry(confirm_frame, show='*', width=30, font=self.FONTS['body'], relief='solid', bd=1)
        self.reg_entries['Confirm Password'].pack(side='left', fill='x', expand=True, padx=(10, 0), ipady=4)
        
        # Role Selection
        role_frame = tk.Frame(account_frame, bg=self.COLORS['white'])
        role_frame.pack(fill='x', pady=8, padx=10)
        tk.Label(role_frame, text="Account Type *", font=self.FONTS['body'], bg=self.COLORS['white'], fg=self.COLORS['text_dark'], width=20, anchor='w').pack(side='left')
        self.role_var = tk.StringVar(value="Citizen")
        role_combo = ttk.Combobox(role_frame, textvariable=self.role_var, values=["Citizen", "Government Officer", "Administrator"], state="readonly", width=28, font=self.FONTS['body'])
        role_combo.pack(side='left', fill='x', expand=True, padx=(10, 0), ipady=4)
        
        # Department (for officers)
        self.dept_frame = tk.Frame(account_frame, bg=self.COLORS['white'])
        self.dept_frame.pack(fill='x', pady=8, padx=10)
        tk.Label(self.dept_frame, text="Department", font=self.FONTS['body'], bg=self.COLORS['white'], fg=self.COLORS['text_dark'], width=20, anchor='w').pack(side='left')
        self.dept_var = tk.StringVar()
        dept_combo = ttk.Combobox(self.dept_frame, textvariable=self.dept_var, 
                                 values=["City Corporation", "Health Department", "Water Supply", "Electricity", "Education", "Environment"], 
                                 state="readonly", width=28, font=self.FONTS['body'])
        dept_combo.pack(side='left', fill='x', expand=True, padx=(10, 0), ipady=4)
        
        # Show department only for officers
        def on_role_change(*args):
            if self.role_var.get() == "Government Officer":
                self.dept_frame.pack(fill='x', pady=8, padx=10)
            else:
                self.dept_frame.pack_forget()

        self.role_var.trace_add('write', on_role_change)
        on_role_change()  # Initial call
        
        # Terms
        terms_frame = tk.Frame(scrollable_frame, bg=self.COLORS['white'])
        terms_frame.pack(fill='x', pady=20, padx=10)
        self.terms_var = tk.BooleanVar()
        ttk.Checkbutton(terms_frame, text="I agree to the Terms and Conditions", variable=self.terms_var).pack()
        
        # Register button
        button_frame = tk.Frame(scrollable_frame, bg=self.COLORS['white'])
        button_frame.pack(fill='x', pady=20)
        tk.Button(button_frame, text="CREATE ACCOUNT", font=self.FONTS['button'], bg=self.COLORS['success'], fg='white', relief='raised', bd=0, cursor='hand2', command=self.handle_register).pack(ipady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def show_frame(self, frame_name):
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        
        if frame_name == 'login':
            self.login_frame.pack(fill='both', expand=True)
        elif frame_name == 'register':
            self.register_frame.pack(fill='both', expand=True)

    def handle_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        
        success, result = self.auth.login_user(username, password)
        if success:
            self.current_user = result
            messagebox.showinfo("Success", f"Welcome {result['name']}!\nRole: {result['role']}")
            self.clear_login_form()
            # Launch dashboard
            self.root.destroy()
            start_dashboard(result)
        else:
            messagebox.showerror("Error", result)

    def handle_register(self):
        data = {
            'full_name': self.reg_entries['Full Name'].get().strip(),
            'email': self.reg_entries['Email Address'].get().strip(),
            'phone': self.reg_entries['Phone Number'].get().strip(),
            'nid': self.reg_entries['NID Number'].get().strip(),
            'date_of_birth': self.reg_entries['Date of Birth (YYYY-MM-DD)'].get().strip(),
            'address': self.reg_entries['Address'].get().strip(),
            'username': self.reg_entries['Username'].get().strip(),
            'password': self.reg_entries['Password'].get().strip(),
            'role': self.role_var.get(),
            'department': self.dept_var.get() if self.role_var.get() == "Government Officer" else None
        }
        
        if data['password'] != self.reg_entries['Confirm Password'].get().strip():
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        if not self.terms_var.get():
            messagebox.showwarning("Warning", "Please agree to the Terms and Conditions")
            return
        
        success, result = self.auth.register_user(data)
        if success:
            messagebox.showinfo("Success", "Account created successfully!\nYou can now login.")
            self.clear_register_form()
            self.show_frame('login')
        else:
            messagebox.showerror("Error", result)

    def clear_login_form(self):
        self.login_username.delete(0, tk.END)
        self.login_password.delete(0, tk.END)

    def clear_register_form(self):
        for entry in self.reg_entries.values():
            entry.delete(0, tk.END)
        self.role_var.set("Citizen")
        self.dept_var.set("")
        self.terms_var.set(False)

def start_application():
    """Start the main application"""
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    app = ModernLoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_application()