import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from auth_functions import AuthManager

class AdminOfficerDashboard:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.auth = AuthManager()
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title(f"{self.user_data['role'].title()} Dashboard - {self.user_data['name']}")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2c3e50')
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg='#2c3e50')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.create_header()
        
        # Content area
        self.create_content_area()
        
        # Show dashboard home by default
        self.show_dashboard_home()
    
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg='#34495e', height=80)
        header_frame.pack(fill=tk.X, pady=(0,10))
        header_frame.pack_propagate(False)
        
        # Welcome message
        welcome_label = tk.Label(header_frame, 
                               text=f"{self.user_data['role'].title()} Dashboard - Welcome, {self.user_data['name']}", 
                               font=('Arial', 16, 'bold'), 
                               fg='white', bg='#34495e')
        welcome_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        if self.user_data.get('department'):
            dept_label = tk.Label(header_frame, 
                                text=f"Department: {self.user_data['department']}", 
                                font=('Arial', 12), 
                                fg='#ecf0f1', bg='#34495e')
            dept_label.pack(side=tk.LEFT, padx=10, pady=20)
        
        # Logout button
        logout_btn = tk.Button(header_frame, text="Logout", 
                              font=('Arial', 12, 'bold'), 
                              bg='#e74c3c', fg='white', 
                              relief='flat', padx=20,
                              command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=20)
    
    def create_content_area(self):
        # Sidebar
        self.create_sidebar()
        
        # Main content
        self.content_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def create_sidebar(self):
        sidebar_frame = tk.Frame(self.main_frame, bg='#34495e', width=280)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))
        sidebar_frame.pack_propagate(False)
        
        # Navigation sections
        sections = []
        
        if self.user_data['role'] == 'admin':
            sections = [
                ("👥 USER MANAGEMENT", [
                    ("👑 Admin View", lambda: self.show_user_group('admin')),
                    ("👮 Officer View", lambda: self.show_user_group('officer')),
                    ("👤 Citizen Veiw", lambda: self.show_user_group('citizen')),
                    ("🔄 User Management", self.show_user_management)
                ]),
                ("🛠️ SERVICES", [
                    ("⚙️ Services Management", self.show_services_management)
                ]),
                ("📋 APPLICATIONS", [
                    ("📄 Application Management", self.show_applications_management)
                ]),
                ("📊 REPORTS", [
                    ("📈 Report Management", self.show_reports_management)
                ])
            ]
        else:  # Officer
            sections = [
                ("👥 USER VIEW", [
                    ("👑 Admins", lambda: self.show_user_group('admin')),
                    ("👮 Colleagues", lambda: self.show_user_group('officer')),
                    ("👤 Citizens", lambda: self.show_user_group('citizen'))
                ]),
                ("📋 MY ASSIGNMENTS", [
                    ("📄 Assigned Applications", self.show_applications_management),
                    ("📊 Assigned Reports", self.show_reports_management)
                ]),
                ("🛠️ SERVICES", [
                    ("📋 Services Catalog", self.show_services_management)
                ])
            ]
        
        # Dashboard Home button at top
        home_btn = tk.Button(sidebar_frame, text="🏠 Dashboard Home", 
                           font=('Arial', 12, 'bold'), 
                           bg='#3498db', fg='white', relief='flat', anchor='w',
                           command=self.show_dashboard_home, padx=20, pady=15)
        home_btn.pack(fill=tk.X, pady=(0,10))
        home_btn.bind("<Enter>", lambda e, b=home_btn: b.configure(bg='#2980b9'))
        home_btn.bind("<Leave>", lambda e, b=home_btn: b.configure(bg='#3498db'))
        
        for section_title, buttons in sections:
            # Section title
            section_label = tk.Label(sidebar_frame, text=section_title, 
                                   font=('Arial', 11, 'bold'), bg='#2c3e50', 
                                   fg='#ecf0f1', padx=10, pady=8, anchor='w')
            section_label.pack(fill=tk.X, pady=(10,5))
            
            # Section buttons
            for text, command in buttons:
                btn = tk.Button(sidebar_frame, text=text, font=('Arial', 10), 
                               bg='#34495e', fg='white', relief='flat', anchor='w',
                               command=command, padx=20, pady=10)
                btn.pack(fill=tk.X)
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg='#3498db'))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg='#34495e'))
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard_home(self):
        self.clear_content()
        
        # Welcome section
        welcome_frame = tk.Frame(self.content_frame, bg='white', relief='raised', bd=1)
        welcome_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(welcome_frame, text=f"Welcome to {self.user_data['role'].title()} Dashboard", 
                font=('Arial', 24, 'bold'), bg='white', fg='#2c3e50').pack(pady=30)
        
        tk.Label(welcome_frame, text=f"Hello {self.user_data['name']}, welcome back!", 
                font=('Arial', 16), bg='white', fg='#7f8c8d').pack(pady=10)
        
        # Stats section
        stats_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Get statistics
        users = self.auth.get_all_users()
        services = self.auth.get_all_services()
        applications = self.auth.get_all_applications(self.user_data['role'], self.user_data['id'])
        reports = self.auth.get_all_reports(self.user_data['role'], self.user_data['id'])
        
        stats = [
            ("Total Users", len(users), '#3498db'),
            ("Total Services", len(services), '#27ae60'),
            ("Pending Applications", len([a for a in applications if a['status'] == 'pending']), '#f39c12'),
            ("Active Reports", len([r for r in reports if r['status'] in ['submitted', 'under_review']]), '#e74c3c')
        ]
        
        # Create stat cards
        stats_container = tk.Frame(stats_frame, bg='#ecf0f1')
        stats_container.pack(fill=tk.X, pady=20)
        
        for i, (title, count, color) in enumerate(stats):
            card = tk.Frame(stats_container, bg=color, relief='raised', bd=1)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, ipadx=20, ipady=30)
            
            tk.Label(card, text=str(count), font=('Arial', 24, 'bold'), 
                    bg=color, fg='white').pack(pady=5)
            tk.Label(card, text=title, font=('Arial', 12), 
                    bg=color, fg='white').pack()
        
        # Quick actions
        actions_frame = tk.Frame(self.content_frame, bg='white', relief='raised', bd=1)
        actions_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(actions_frame, text="Quick Actions", 
                font=('Arial', 18, 'bold'), bg='white', fg='#2c3e50').pack(pady=20)
        
        # Action buttons based on role
        if self.user_data['role'] == 'admin':
            actions = [
                ("👥 Manage Users", self.show_user_management),
                ("🛠️ Manage Services", self.show_services_management),
                ("📋 View Applications", self.show_applications_management),
                ("📊 Manage Reports", self.show_reports_management)
            ]
        else:
            actions = [
                ("📋 My Applications", self.show_applications_management),
                ("📊 My Reports", self.show_reports_management),
                ("🛠️ Services Catalog", self.show_services_management),
                ("👥 View Citizens", lambda: self.show_user_group('citizen'))
            ]
        
        action_container = tk.Frame(actions_frame, bg='white')
        action_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        row, col = 0, 0
        for text, command in actions:
            btn = tk.Button(action_container, text=text, font=('Arial', 12, 'bold'),
                          bg='#3498db', fg='white', padx=20, pady=15,
                          command=command)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(2):
            action_container.columnconfigure(i, weight=1)
        for i in range(2):
            action_container.rowconfigure(i, weight=1)
    
    def show_user_group(self, role):
        self.clear_content()
        
        role_display = {
            'admin': 'Administrators',
            'officer': 'Government Officers', 
            'citizen': 'Citizens'
        }
        
        title_label = tk.Label(self.content_frame, text=f"{role_display.get(role, role.title())} - Group View", 
                              font=('Arial', 18, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(pady=20)
        
        # Treeview for users
        tree_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Username', 'Full Name', 'Email', 'Phone', 'Department', 'Status', 'Last Login'), show='headings')
        
        # Configure columns
        columns = [
            ('ID', 50), ('Username', 100), ('Full Name', 150), ('Email', 150), 
            ('Phone', 100), ('Department', 120), ('Status', 80), ('Last Login', 120)
        ]
        
        for col, width in columns:
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load users by role
        users = self.auth.get_all_users(role)
        
        for user in users:
            last_login = user['last_login'].strftime('%Y-%m-%d %H:%M') if user['last_login'] else 'Never'
            tree.insert('', 'end', values=(
                user['id'],
                user['username'],
                user['full_name'] or 'N/A',
                user['email'] or 'N/A',
                user['phone'] or 'N/A',
                user['department'] or 'N/A',
                user['status'].title(),
                last_login
            ))
    
    def show_user_management(self):
        if self.user_data['role'] != 'admin':
            messagebox.showinfo("Access Denied", "Only administrators can access user management.")
            return
            
        self.clear_content()
        
        # Header with search
        header_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        header_frame.pack(fill=tk.X, pady=20, padx=20)
        
        title_label = tk.Label(header_frame, text="User Management", 
                              font=('Arial', 18, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(side=tk.LEFT)
        
        # Action buttons frame
        action_frame = tk.Frame(header_frame, bg='#ecf0f1')
        action_frame.pack(side=tk.RIGHT)
        
        refresh_btn = tk.Button(action_frame, text="🔄 Refresh", font=('Arial', 10),
                               bg='#3498db', fg='white', command=self.load_users)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = tk.Frame(header_frame, bg='#ecf0f1')
        search_frame.pack(side=tk.RIGHT, padx=20)
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.insert(0, "Search users...")
        
        search_btn = tk.Button(search_frame, text="Search", font=('Arial', 10),
                              bg='#27ae60', fg='white', command=self.search_users)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Users treeview
        tree_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.users_tree = ttk.Treeview(tree_frame, columns=('ID', 'Username', 'Full Name', 'Email', 'Role', 'Status', 'Department', 'Created'), show='headings')
        
        # Configure columns
        columns = [
            ('ID', 50), ('Username', 100), ('Full Name', 150), ('Email', 150), 
            ('Role', 80), ('Status', 80), ('Department', 120), ('Created', 120)
        ]
        
        for col, width in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=width)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # User actions frame
        actions_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        action_buttons = [
            ("Activate User", '#27ae60', self.activate_user),
            ("Suspend User", '#f39c12', self.suspend_user),
            ("Delete User", '#e74c3c', self.delete_user),
            ("Update Role", '#3498db', self.update_user_role),
            ("Edit User", '#9b59b6', self.edit_user)
        ]
        
        for text, color, command in action_buttons:
            btn = tk.Button(actions_frame, text=text, font=('Arial', 10),
                           bg=color, fg='white', command=command)
            btn.pack(side=tk.LEFT, padx=5)
        
        # Load users
        self.load_users()
    
    def load_users(self):
        users = self.auth.get_all_users()
        self.display_users(users)
    
    def display_users(self, users):
        # Clear existing data
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Add users to treeview
        for user in users:
            self.users_tree.insert('', 'end', values=(
                user['id'],
                user['username'],
                user['full_name'] or 'N/A',
                user['email'] or 'N/A',
                user['role'].title(),
                user['status'].title(),
                user['department'] or 'N/A',
                user['created_at'].strftime('%Y-%m-%d')
            ))
    
    def search_users(self):
        search_term = self.search_entry.get()
        if search_term and search_term != "":
            users = self.auth.search_users(search_term)
            self.display_users(users)
        else:
            self.load_users()
    
    def get_selected_user_id(self):
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user first")
            return None
        
        item = self.users_tree.item(selection[0])
        return item['values'][0]  # Return user ID
    
    def activate_user(self):
        user_id = self.get_selected_user_id()
        if user_id and messagebox.askyesno("Confirm", "Activate this user?"):
            if self.auth.update_user_status(user_id, 'active'):
                messagebox.showinfo("Success", "User activated successfully")
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to activate user")
    
    def suspend_user(self):
        user_id = self.get_selected_user_id()
        if user_id and messagebox.askyesno("Confirm", "Suspend this user?"):
            if self.auth.update_user_status(user_id, 'suspended'):
                messagebox.showinfo("Success", "User suspended successfully")
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to suspend user")
    
    def delete_user(self):
        user_id = self.get_selected_user_id()
        if user_id and messagebox.askyesno("Confirm", "Delete this user? This action cannot be undone."):
            if self.auth.delete_user(user_id):
                messagebox.showinfo("Success", "User deleted successfully")
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to delete user")

    def update_user_role(self):
        user_id = self.get_selected_user_id()
        if user_id:
            # Create a dialog window for role selection
            role_dialog = tk.Toplevel(self.root)
            role_dialog.title("Update User Role")
            role_dialog.geometry("300x150")
            role_dialog.configure(bg='#ecf0f1')
            role_dialog.transient(self.root)
            role_dialog.grab_set()

            tk.Label(role_dialog, text="Select New Role:",
                     font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(pady=20)

            # Role selection combo box
            role_var = tk.StringVar(value="citizen")
            role_combo = ttk.Combobox(role_dialog, textvariable=role_var,
                                      values=["admin", "officer", "citizen"],
                                      state="readonly", font=('Arial', 12), width=15)
            role_combo.pack(pady=10)

            def confirm_role_update():
                new_role = role_var.get()
                if new_role:
                    if self.auth.update_user_role(user_id, new_role.lower()):
                        messagebox.showinfo("Success", "User role updated successfully")
                        role_dialog.destroy()
                        self.load_users()
                    else:
                        messagebox.showerror("Error", "Failed to update user role")

            # Buttons
            button_frame = tk.Frame(role_dialog, bg='#ecf0f1')
            button_frame.pack(pady=20)

            confirm_btn = tk.Button(button_frame, text="Confirm", font=('Arial', 10),
                                    bg='#27ae60', fg='white', padx=15,
                                    command=confirm_role_update)
            confirm_btn.pack(side=tk.LEFT, padx=10)

            cancel_btn = tk.Button(button_frame, text="Cancel", font=('Arial', 10),
                                   bg='#95a5a6', fg='white', padx=15,
                                   command=role_dialog.destroy)
            cancel_btn.pack(side=tk.LEFT, padx=10)

    def edit_user(self):
        user_id = self.get_selected_user_id()
        if user_id:
            messagebox.showinfo("Info", "Edit user feature would open a detailed form here")
    
    def show_services_management(self):
        self.clear_content()
        
        # Header with actions
        header_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        header_frame.pack(fill=tk.X, pady=20, padx=20)
        
        title_label = tk.Label(header_frame, text="Services Management", 
                              font=('Arial', 18, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(side=tk.LEFT)
        
        action_frame = tk.Frame(header_frame, bg='#ecf0f1')
        action_frame.pack(side=tk.RIGHT)
        
        if self.user_data['role'] == 'admin':
            add_btn = tk.Button(action_frame, text="Add Service", font=('Arial', 10),
                               bg='#27ae60', fg='white', command=self.add_service_dialog)
            add_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(action_frame, text="Refresh", font=('Arial', 10),
                               bg='#3498db', fg='white', command=self.load_services)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Services treeview
        tree_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.services_tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Description', 'Category', 'Fee', 'Status', 'Created By'), show='headings')
        
        columns = [
            ('ID', 50), ('Name', 150), ('Description', 250), ('Category', 100),
            ('Fee', 80), ('Status', 80), ('Created By', 100)
        ]
        
        for col, width in columns:
            self.services_tree.heading(col, text=col)
            self.services_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.services_tree.yview)
        self.services_tree.configure(yscrollcommand=scrollbar.set)
        
        self.services_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Service actions (only for admin)
        if self.user_data['role'] == 'admin':
            actions_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
            actions_frame.pack(fill=tk.X, padx=20, pady=10)
            
            edit_btn = tk.Button(actions_frame, text="Edit Service", font=('Arial', 10),
                               bg='#3498db', fg='white', command=self.edit_service)
            edit_btn.pack(side=tk.LEFT, padx=5)
            
            delete_btn = tk.Button(actions_frame, text="Delete Service", font=('Arial', 10),
                                 bg='#e74c3c', fg='white', command=self.delete_service)
            delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Load services
        self.load_services()
    
    def load_services(self):
        services = self.auth.get_all_services()
        self.display_services(services)
    
    def display_services(self, services):
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)
        
        for service in services:
            self.services_tree.insert('', 'end', values=(
                service['id'],
                service['name'],
                service['description'] or 'No description',
                service['category'] or 'General',
                f"${service['fee']}" if service['fee'] else 'Free',
                service['status'].title(),
                service['created_by_name'] or 'System'
            ))
    
    def add_service_dialog(self):
        if self.user_data['role'] != 'admin':
            messagebox.showinfo("Access Denied", "Only administrators can add services.")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Service")
        dialog.geometry("500x500")
        dialog.configure(bg='#ecf0f1')
        
        tk.Label(dialog, text="Add New Service", font=('Arial', 16, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').pack(pady=20)
        
        form_frame = tk.Frame(dialog, bg='#ecf0f1')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30)
        
        fields = [
            ("Service Name", "entry"),
            ("Description", "text"),
            ("Category", "combo", ["Certificates", "Licenses", "Tax", "Utilities", "Travel", "Other"]),
            ("Requirements", "text"),
            ("Processing Time", "entry"),
            ("Fee", "entry")
        ]
        
        entries = {}
        
        for i, field_info in enumerate(fields):
            field_name = field_info[0]
            field_type = field_info[1]
            
            tk.Label(form_frame, text=field_name, font=('Arial', 10, 'bold'), 
                    bg='#ecf0f1', fg='#2c3e50').grid(row=i, column=0, sticky='w', pady=5)
            
            if field_type == "entry":
                entry = tk.Entry(form_frame, font=('Arial', 10), width=40)
                entry.grid(row=i, column=1, pady=5, padx=10, sticky='ew')
                entries[field_name] = entry
            elif field_type == "text":
                text = tk.Text(form_frame, font=('Arial', 10), height=3, width=40)
                text.grid(row=i, column=1, pady=5, padx=10, sticky='ew')
                entries[field_name] = text
            elif field_type == "combo":
                var = tk.StringVar()
                combo = ttk.Combobox(form_frame, textvariable=var, values=field_info[2], state="readonly")
                combo.grid(row=i, column=1, pady=5, padx=10, sticky='ew')
                entries[field_name] = var
        
        form_frame.columnconfigure(1, weight=1)
        
        def save_service():
            service_data = {}
            for field_name, widget in entries.items():
                if isinstance(widget, tk.Entry):
                    service_data[field_name.lower().replace(' ', '_')] = widget.get()
                elif isinstance(widget, tk.Text):
                    service_data[field_name.lower().replace(' ', '_')] = widget.get("1.0", tk.END).strip()
                elif isinstance(widget, tk.StringVar):
                    service_data[field_name.lower().replace(' ', '_')] = widget.get()
            
            if not service_data.get('service_name'):
                messagebox.showwarning("Warning", "Service name is required")
                return
            
            success, result = self.auth.add_service(service_data, self.user_data['id'])
            if success:
                messagebox.showinfo("Success", "Service added successfully")
                dialog.destroy()
                self.load_services()
            else:
                messagebox.showerror("Error", result)
        
        tk.Button(dialog, text="Save Service", font=('Arial', 12, 'bold'),
                 bg='#27ae60', fg='white', command=save_service).pack(pady=20)

    def edit_service(self):
        if self.user_data['role'] != 'admin':
            messagebox.showinfo("Access Denied", "Only administrators can edit services.")
            return

        selection = self.services_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a service first")
            return

        item = self.services_tree.item(selection[0])
        service_id = item['values'][0]

        # Get service details from database
        service = self.auth.get_service_by_id(service_id)
        if not service:
            messagebox.showerror("Error", "Could not load service details")
            return

        # Create edit service dialog
        edit_dialog = tk.Toplevel(self.root)
        edit_dialog.title("Edit Service")
        edit_dialog.geometry("500x500")
        edit_dialog.configure(bg='#ecf0f1')
        edit_dialog.transient(self.root)
        edit_dialog.grab_set()

        tk.Label(edit_dialog, text="Edit Service", font=('Arial', 16, 'bold'),
                 bg='#ecf0f1', fg='#2c3e50').pack(pady=20)

        form_frame = tk.Frame(edit_dialog, bg='#ecf0f1')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30)

        fields = [
            ("Service Name", "entry", service['name']),
            ("Description", "text", service.get('description', '')),
            ("Category", "combo", ["Certificates", "Licenses", "Tax", "Utilities", "Travel", "Other"],
             service.get('category', 'General')),
            ("Requirements", "text", service.get('requirements', '')),
            ("Processing Time", "entry", service.get('processing_time', '')),
            ("Fee", "entry", str(service.get('fee', 0)) if service.get('fee') else "0"),
            ("Status", "combo", ["active", "inactive"], service.get('status', 'active'))
        ]

        entries = {}

        for i, field_info in enumerate(fields):
            field_name = field_info[0]
            field_type = field_info[1]
            field_value = field_info[3] if len(field_info) > 3 else field_info[2]

            tk.Label(form_frame, text=field_name, font=('Arial', 10, 'bold'),
                     bg='#ecf0f1', fg='#2c3e50').grid(row=i, column=0, sticky='w', pady=8)

            if field_type == "entry":
                entry = tk.Entry(form_frame, font=('Arial', 10), width=40)
                entry.insert(0, field_value)
                entry.grid(row=i, column=1, pady=8, padx=10, sticky='ew')
                entries[field_name] = entry
            elif field_type == "text":
                text = tk.Text(form_frame, font=('Arial', 10), height=3, width=40)
                text.insert('1.0', field_value)
                text.grid(row=i, column=1, pady=8, padx=10, sticky='ew')
                entries[field_name] = text
            elif field_type == "combo":
                var = tk.StringVar(value=field_value)
                combo = ttk.Combobox(form_frame, textvariable=var, values=field_info[2], state="readonly")
                combo.grid(row=i, column=1, pady=8, padx=10, sticky='ew')
                entries[field_name] = var

        form_frame.columnconfigure(1, weight=1)

        def update_service():
            service_data = {}
            for field_name, widget in entries.items():
                if isinstance(widget, tk.Entry):
                    service_data[field_name.lower().replace(' ', '_')] = widget.get()
                elif isinstance(widget, tk.Text):
                    service_data[field_name.lower().replace(' ', '_')] = widget.get("1.0", tk.END).strip()
                elif isinstance(widget, tk.StringVar):
                    service_data[field_name.lower().replace(' ', '_')] = widget.get()

            if not service_data.get('service_name'):
                messagebox.showwarning("Warning", "Service name is required")
                return

            # Convert fee to float
            try:
                service_data['fee'] = float(service_data.get('fee', 0))
            except ValueError:
                messagebox.showwarning("Warning", "Fee must be a valid number")
                return

            # Update service in database
            if self.auth.update_service(service_id, service_data):
                messagebox.showinfo("Success", "Service updated successfully")
                edit_dialog.destroy()
                self.load_services()
            else:
                messagebox.showerror("Error", "Failed to update service")

        # Button frame
        button_frame = tk.Frame(edit_dialog, bg='#ecf0f1')
        button_frame.pack(fill=tk.X, pady=20)

        update_btn = tk.Button(button_frame, text="Update Service", font=('Arial', 12, 'bold'),
                               bg='#27ae60', fg='white', command=update_service)
        update_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(button_frame, text="Cancel", font=('Arial', 12),
                               bg='#95a5a6', fg='white', command=edit_dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)

        # Add delete button
        delete_btn = tk.Button(button_frame, text="Delete Service", font=('Arial', 12),
                               bg='#e74c3c', fg='white',
                               command=lambda: self.delete_service_from_edit(service_id, edit_dialog))
        delete_btn.pack(side=tk.RIGHT, padx=10)

    def delete_service_from_edit(self, service_id, parent_window):
        """Delete service from the edit dialog"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this service?"):
            if self.auth.delete_service(service_id):
                messagebox.showinfo("Success", "Service deleted successfully")
                parent_window.destroy()
                self.load_services()
            else:
                messagebox.showerror("Error", "Failed to delete service")
    
    def delete_service(self):
        if self.user_data['role'] != 'admin':
            messagebox.showinfo("Access Denied", "Only administrators can delete services.")
            return
            
        selection = self.services_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a service first")
            return
        
        item = self.services_tree.item(selection[0])
        service_id = item['values'][0]
        
        if messagebox.askyesno("Confirm", "Delete this service?"):
            if self.auth.delete_service(service_id):
                messagebox.showinfo("Success", "Service deleted successfully")
                self.load_services()
            else:
                messagebox.showerror("Error", "Failed to delete service")
    
    def show_applications_management(self):
        self.clear_content()
        
        # Header with title
        header_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        header_frame.pack(fill=tk.X, pady=20, padx=20)
        
        title_text = "Applications Management" if self.user_data['role'] == 'admin' else "My Assigned Applications"
        title_label = tk.Label(header_frame, text=title_text, 
                              font=('Arial', 18, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(side=tk.LEFT)
        
        # Applications treeview
        tree_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.applications_tree = ttk.Treeview(tree_frame, columns=('ID', 'User', 'Service', 'Status', 'Officer', 'Applied Date'), show='headings')
        
        columns = [
            ('ID', 50), ('User', 150), ('Service', 200), ('Status', 100),
            ('Officer', 120), ('Applied Date', 150)
        ]
        
        for col, width in columns:
            self.applications_tree.heading(col, text=col)
            self.applications_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.applications_tree.yview)
        self.applications_tree.configure(yscrollcommand=scrollbar.set)
        
        self.applications_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Application actions
        actions_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        if self.user_data['role'] == 'admin':
            action_buttons = [
                ("Update Status", '#3498db', self.update_application_status),
                ("Assign Officer", '#9b59b6', self.assign_application_officer),
                ("Delete", '#e74c3c', self.delete_application)
            ]
        else:
            action_buttons = [
                ("Update Status", '#3498db', self.update_application_status),
                ("View Details", '#27ae60', self.view_application_details)
            ]
        
        for text, color, command in action_buttons:
            btn = tk.Button(actions_frame, text=text, font=('Arial', 10),
                           bg=color, fg='white', command=command)
            btn.pack(side=tk.LEFT, padx=5)
        
        # Load applications
        self.load_applications()
    
    def load_applications(self):
        applications = self.auth.get_all_applications(self.user_data['role'], self.user_data['id'])
        self.display_applications(applications)
    
    def display_applications(self, applications):
        for item in self.applications_tree.get_children():
            self.applications_tree.delete(item)
        
        for app in applications:
            self.applications_tree.insert('', 'end', values=(
                app['id'],
                app['user_full_name'] or app['user_name'],
                app['service_name'],
                app['status'].replace('_', ' ').title(),
                app['officer_name'] or 'Not assigned',
                app['applied_date'].strftime('%Y-%m-%d %H:%M')
            ))

    def update_application_status(self):
        selection = self.applications_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application first")
            return

        item = self.applications_tree.item(selection[0])
        app_id = item['values'][0]

        # Create a dialog window for status selection
        status_dialog = tk.Toplevel(self.root)
        status_dialog.title("Update Application Status")
        status_dialog.geometry("350x200")
        status_dialog.configure(bg='#ecf0f1')
        status_dialog.transient(self.root)
        status_dialog.grab_set()

        tk.Label(status_dialog, text="Select New Status:",
                 font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(pady=20)

        # Status selection combo box
        status_var = tk.StringVar(value="pending")
        status_combo = ttk.Combobox(status_dialog, textvariable=status_var,
                                    values=["pending", "under_review", "approved", "rejected", "completed"],
                                    state="readonly", font=('Arial', 12), width=20)
        status_combo.pack(pady=10)

        # Notes field
        tk.Label(status_dialog, text="Notes (optional):",
                 font=('Arial', 10), bg='#ecf0f1').pack(pady=(10, 5))

        notes_entry = tk.Entry(status_dialog, font=('Arial', 10), width=30)
        notes_entry.pack(pady=5)

        def confirm_status_update():
            new_status = status_var.get()
            notes = notes_entry.get().strip()

            if self.auth.update_application_status(app_id, new_status, notes):
                messagebox.showinfo("Success", "Application status updated successfully")
                status_dialog.destroy()
                self.load_applications()
            else:
                messagebox.showerror("Error", "Failed to update application status")

        # Buttons
        button_frame = tk.Frame(status_dialog, bg='#ecf0f1')
        button_frame.pack(pady=20)

        confirm_btn = tk.Button(button_frame, text="Confirm", font=('Arial', 10),
                                bg='#27ae60', fg='white', padx=15,
                                command=confirm_status_update)
        confirm_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(button_frame, text="Cancel", font=('Arial', 10),
                               bg='#95a5a6', fg='white', padx=15,
                               command=status_dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def assign_application_officer(self):
        if self.user_data['role'] != 'admin':
            messagebox.showinfo("Access Denied", "Only administrators can assign officers.")
            return

        selection = self.applications_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application first")
            return

        item = self.applications_tree.item(selection[0])
        app_id = item['values'][0]

        officers = self.auth.get_officers()
        if not officers:
            messagebox.showwarning("Warning", "No officers available")
            return

        # Create a dialog window for officer selection
        officer_dialog = tk.Toplevel(self.root)
        officer_dialog.title("Assign Officer to Application")
        officer_dialog.geometry("400x200")
        officer_dialog.configure(bg='#ecf0f1')
        officer_dialog.transient(self.root)
        officer_dialog.grab_set()

        tk.Label(officer_dialog, text="Select Officer to Assign:",
                 font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(pady=20)

        # Officer selection combo box
        officer_var = tk.StringVar()
        officer_combo = ttk.Combobox(officer_dialog, textvariable=officer_var,
                                     state="readonly", font=('Arial', 12), width=30)

        # Format officer names for display
        officer_options = [f"{officer['username']} - {officer['full_name']} ({officer['department']})"
                           for officer in officers]
        officer_combo['values'] = officer_options
        officer_combo.pack(pady=10)

        def confirm_officer_assignment():
            selected_officer = officer_var.get()
            if not selected_officer:
                messagebox.showwarning("Warning", "Please select an officer")
                return

            # Extract username from the selected option
            officer_username = selected_officer.split(' - ')[0]
            officer = next((o for o in officers if o['username'] == officer_username), None)

            if officer:
                if self.auth.update_application_status(app_id, 'under_review', None, officer['id']):
                    messagebox.showinfo("Success", "Officer assigned successfully")
                    officer_dialog.destroy()
                    self.load_applications()
                else:
                    messagebox.showerror("Error", "Failed to assign officer")

        # Buttons
        button_frame = tk.Frame(officer_dialog, bg='#ecf0f1')
        button_frame.pack(pady=20)

        confirm_btn = tk.Button(button_frame, text="Assign Officer", font=('Arial', 10),
                                bg='#27ae60', fg='white', padx=15,
                                command=confirm_officer_assignment)
        confirm_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(button_frame, text="Cancel", font=('Arial', 10),
                               bg='#95a5a6', fg='white', padx=15,
                               command=officer_dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def delete_application(self):
        if self.user_data['role'] != 'admin':
            messagebox.showinfo("Access Denied", "Only administrators can delete applications.")
            return
            
        selection = self.applications_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application first")
            return
        
        item = self.applications_tree.item(selection[0])
        app_id = item['values'][0]
        
        if messagebox.askyesno("Confirm", "Delete this application?"):
            if self.auth.delete_application(app_id):
                messagebox.showinfo("Success", "Application deleted successfully")
                self.load_applications()
            else:
                messagebox.showerror("Error", "Failed to delete application")
    
    def view_application_details(self):
        selection = self.applications_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application first")
            return
        
        item = self.applications_tree.item(selection[0])
        app_id = item['values'][0]
        
        messagebox.showinfo("Application Details", f"Detailed view for application ID: {app_id}")
    
    def show_reports_management(self):
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        header_frame.pack(fill=tk.X, pady=20, padx=20)
        
        title_text = "Report Management" if self.user_data['role'] == 'admin' else "My Assigned Reports"
        title_label = tk.Label(header_frame, text=title_text, 
                              font=('Arial', 18, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(side=tk.LEFT)
        
        # Reports treeview
        tree_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.reports_tree = ttk.Treeview(tree_frame, columns=('ID', 'Title', 'User', 'Officer', 'Status', 'Priority', 'Submitted Date'), show='headings')
        
        columns = [
            ('ID', 50), ('Title', 200), ('User', 120), ('Officer', 120),
            ('Status', 100), ('Priority', 80), ('Submitted Date', 150)
        ]
        
        for col, width in columns:
            self.reports_tree.heading(col, text=col)
            self.reports_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.reports_tree.yview)
        self.reports_tree.configure(yscrollcommand=scrollbar.set)
        
        self.reports_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Report actions
        actions_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        action_buttons = [
            ("View Details", '#3498db', self.view_report_details),
            ("Update Status", '#f39c12', self.update_report_status),
        ]
        
        if self.user_data['role'] == 'admin':
            action_buttons.append(("Assign Officer", '#9b59b6', self.assign_report_officer))
            action_buttons.append(("Delete Report", '#e74c3c', self.delete_report))
        
        for text, color, command in action_buttons:
            btn = tk.Button(actions_frame, text=text, font=('Arial', 10),
                           bg=color, fg='white', command=command)
            btn.pack(side=tk.LEFT, padx=5)
        
        # Load reports
        self.load_reports()
    
    def load_reports(self):
        reports = self.auth.get_all_reports(self.user_data['role'], self.user_data['id'])
        self.display_reports(reports)
    
    def display_reports(self, reports):
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)
        
        for report in reports:
            self.reports_tree.insert('', 'end', values=(
                report['id'],
                report['title'],
                report['user_full_name'] or report['user_name'],
                report['officer_full_name'] or report['officer_name'] or 'Not assigned',
                report['status'].replace('_', ' ').title(),
                report['priority'].title(),
                report['submitted_date'].strftime('%Y-%m-%d %H:%M')
            ))
    
    def view_report_details(self):
        selection = self.reports_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report first")
            return
        
        item = self.reports_tree.item(selection[0])
        report_id = item['values'][0]
        
        # In a real application, this would open a detailed view window
        messagebox.showinfo("Report Details", f"Detailed view for report ID: {report_id}")

    def update_report_status(self):
        selection = self.reports_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report first")
            return

        item = self.reports_tree.item(selection[0])
        report_id = item['values'][0]

        # Create a dialog window for status selection
        status_dialog = tk.Toplevel(self.root)
        status_dialog.title("Update Report Status")
        status_dialog.geometry("600x400")
        status_dialog.configure(bg='#ecf0f1')
        status_dialog.transient(self.root)
        status_dialog.grab_set()

        tk.Label(status_dialog, text="Select New Status:",
                 font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(pady=20)

        # Status selection combo box
        status_var = tk.StringVar(value="submitted")
        status_combo = ttk.Combobox(status_dialog, textvariable=status_var,
                                    values=["submitted", "under_review", "resolved", "rejected", "closed"],
                                    state="readonly", font=('Arial', 12), width=20)
        status_combo.pack(pady=10)

        # Resolution notes field
        tk.Label(status_dialog, text="Resolution Notes (optional):",
                 font=('Arial', 10), bg='#ecf0f1').pack(pady=(10, 5))

        notes_entry = tk.Entry(status_dialog, font=('Arial', 10), width=30)
        notes_entry.pack(pady=5)

        def confirm_status_update():
            new_status = status_var.get()
            resolution_notes = notes_entry.get().strip()

            if self.auth.update_report_status(report_id, new_status, resolution_notes):
                messagebox.showinfo("Success", "Report status updated successfully")
                status_dialog.destroy()
                self.load_reports()
            else:
                messagebox.showerror("Error", "Failed to update report status")

        # Buttons
        button_frame = tk.Frame(status_dialog, bg='#ecf0f1')
        button_frame.pack(pady=20)

        confirm_btn = tk.Button(button_frame, text="Confirm", font=('Arial', 10),
                                bg='#27ae60', fg='white', padx=15,
                                command=confirm_status_update)
        confirm_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(button_frame, text="Cancel", font=('Arial', 10),
                               bg='#95a5a6', fg='white', padx=15,
                               command=status_dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def assign_report_officer(self):
        if self.user_data['role'] != 'admin':
            messagebox.showinfo("Access Denied", "Only administrators can assign officers.")
            return

        selection = self.reports_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report first")
            return

        item = self.reports_tree.item(selection[0])
        report_id = item['values'][0]

        officers = self.auth.get_officers()
        if not officers:
            messagebox.showwarning("Warning", "No officers available")
            return

        # Create a dialog window for officer selection
        officer_dialog = tk.Toplevel(self.root)
        officer_dialog.title("Assign Officer to Report")
        officer_dialog.geometry("400x200")
        officer_dialog.configure(bg='#ecf0f1')
        officer_dialog.transient(self.root)
        officer_dialog.grab_set()

        tk.Label(officer_dialog, text="Select Officer to Assign:",
                 font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(pady=20)

        # Officer selection combo box
        officer_var = tk.StringVar()
        officer_combo = ttk.Combobox(officer_dialog, textvariable=officer_var,
                                     state="readonly", font=('Arial', 12), width=30)

        # Format officer names for display
        officer_options = [f"{officer['username']} - {officer['full_name']} ({officer['department']})"
                           for officer in officers]
        officer_combo['values'] = officer_options
        officer_combo.pack(pady=10)

        def confirm_officer_assignment():
            selected_officer = officer_var.get()
            if not selected_officer:
                messagebox.showwarning("Warning", "Please select an officer")
                return

            # Extract username from the selected option
            officer_username = selected_officer.split(' - ')[0]
            officer = next((o for o in officers if o['username'] == officer_username), None)

            if officer:
                if self.auth.assign_report_to_officer(report_id, officer['id']):
                    messagebox.showinfo("Success", "Officer assigned successfully")
                    officer_dialog.destroy()
                    self.load_reports()
                else:
                    messagebox.showerror("Error", "Failed to assign officer")

        # Buttons
        button_frame = tk.Frame(officer_dialog, bg='#ecf0f1')
        button_frame.pack(pady=20)

        confirm_btn = tk.Button(button_frame, text="Assign Officer", font=('Arial', 10),
                                bg='#27ae60', fg='white', padx=15,
                                command=confirm_officer_assignment)
        confirm_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(button_frame, text="Cancel", font=('Arial', 10),
                               bg='#95a5a6', fg='white', padx=15,
                               command=officer_dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
    def delete_report(self):
        if self.user_data['role'] != 'admin':
            messagebox.showinfo("Access Denied", "Only administrators can delete reports.")
            return
            
        selection = self.reports_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report first")
            return
        
        item = self.reports_tree.item(selection[0])
        report_id = item['values'][0]
        
        if messagebox.askyesno("Confirm", "Delete this report?"):
            if self.auth.delete_report(report_id):
                messagebox.showinfo("Success", "Report deleted successfully")
                self.load_reports()
            else:
                messagebox.showerror("Error", "Failed to delete report")
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            # Restart the application
            import main
            main.start_application()
