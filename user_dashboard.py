import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from auth_functions import AuthManager
from PIL import Image, ImageTk
import os
import datetime
from tkinter import scrolledtext
import shutil

class UserDashboard:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.auth = AuthManager()
        self.setup_dashboard()
    
    def setup_dashboard(self):
        self.root.title(f"Citizen Dashboard - {self.user_data['name']}")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f5f6fa')
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f5f6fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X, pady=(0,20))
        header_frame.pack_propagate(False)
        
        # Welcome message
        welcome_label = tk.Label(header_frame, 
                               text=f"Welcome, {self.user_data['name']}!", 
                               font=('Arial', 18, 'bold'), 
                               fg='white', bg='#2c3e50')
        welcome_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # User info
        role_label = tk.Label(header_frame, 
                            text=f"Role: {self.user_data['role'].title()}", 
                            font=('Arial', 12), 
                            fg='#ecf0f1', bg='#2c3e50')
        role_label.pack(side=tk.LEFT, padx=10, pady=20)
        
        # Logout button
        logout_btn = tk.Button(header_frame, text="Logout", 
                              font=('Arial', 12, 'bold'), 
                              bg='#e74c3c', fg='white', 
                              relief='flat', padx=20,
                              command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Dashboard content
        self.create_dashboard_content(main_frame)
    
    def create_dashboard_content(self, parent):
        # Create notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Profile Tab
        profile_frame = tk.Frame(notebook, bg="#f5f6fa")
        notebook.add(profile_frame, text="👤 User Profile")
        self.create_profile_tab(profile_frame)
        
        # Services Tab
        services_frame = tk.Frame(notebook, bg='#f5f6fa')
        notebook.add(services_frame, text="🛠️ Available Services")
        self.create_services_tab(services_frame)
        
        # Applications Tab
        applications_frame = tk.Frame(notebook, bg='#f5f6fa')
        notebook.add(applications_frame, text="📋 My Applications")
        self.create_applications_tab(applications_frame)
        
        # Reports Tab
        reports_frame = tk.Frame(notebook, bg='#f5f6fa')
        notebook.add(reports_frame, text="📝 Submit Report")
        self.create_reports_tab(reports_frame)
        
        # My Reports Tab
        my_reports_frame = tk.Frame(notebook, bg='#f5f6fa')
        notebook.add(my_reports_frame, text="📊 My Reports")
        self.create_my_reports_tab(my_reports_frame)
    
    def create_profile_tab(self, parent):
        # Get user profile data
        profile = self.auth.get_user_profile(self.user_data['id'])
        
        if not profile:
            tk.Label(parent, text="Error loading profile", 
                    font=('Arial', 14), bg='#f5f6fa').pack(pady=50)
            return
        
        # Profile container
        profile_container = tk.Frame(parent, bg='white', relief='raised', bd=1)
        profile_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Profile header
        header_frame = tk.Frame(profile_container, bg='#3498db', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Personal Information", 
                font=('Arial', 16, 'bold'), fg='white', bg='#3498db').pack(pady=20)
        
        # Profile details
        details_frame = tk.Frame(profile_container, bg='white')
        details_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        profile_fields = [
            ("Full Name", profile['full_name']),
            ("Username", profile['username']),
            ("Email", profile['email'] or "Not provided"),
            ("Phone", profile['phone'] or "Not provided"),
            ("NID Number", profile['nid_number'] or "Not provided"),
            ("Date of Birth", str(profile['date_of_birth']) if profile['date_of_birth'] else "Not provided"),
            ("Address", profile['address'] or "Not provided"),
            ("Role", profile['role'].title()),
            ("Member Since", profile['created_at'].strftime('%B %d, %Y') if profile['created_at'] else "Unknown"),
            ("Last Login", profile['last_login'].strftime('%Y-%m-%d %H:%M') if profile['last_login'] else "Never")
        ]
        
        for i, (label, value) in enumerate(profile_fields):
            row_frame = tk.Frame(details_frame, bg='white')
            row_frame.pack(fill=tk.X, pady=8)
            
            tk.Label(row_frame, text=f"{label}:", font=('Arial', 12, 'bold'), 
                    bg='white', fg='#2c3e50', width=15, anchor='w').pack(side=tk.LEFT)
            tk.Label(row_frame, text=value, font=('Arial', 12), 
                    bg='white', fg='#34495e').pack(side=tk.LEFT, padx=10)
        
        # Edit Profile Button
        edit_btn = tk.Button(profile_container, text="Edit Profile", 
                           font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                           padx=20, pady=10, command=self.edit_profile)
        edit_btn.pack(pady=20)
    
    def edit_profile(self):
        """Open profile editing window"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Profile")
        edit_window.geometry("500x600")
        edit_window.configure(bg='#ecf0f1')
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Get current profile
        profile = self.auth.get_user_profile(self.user_data['id'])
        
        tk.Label(edit_window, text="Edit Your Profile", 
                font=('Arial', 18, 'bold'), bg='#ecf0f1').pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(edit_window, bg='white', relief='raised', bd=1)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Form fields
        fields = [
            ("Full Name", "full_name", profile['full_name']),
            ("Email", "email", profile['email'] or ""),
            ("Phone", "phone", profile['phone'] or ""),
            ("NID Number", "nid_number", profile['nid_number'] or ""),
            ("Address", "address", profile['address'] or "")
        ]
        
        entries = {}
        
        for i, (label, field, value) in enumerate(fields):
            tk.Label(form_frame, text=label, font=('Arial', 12, 'bold'), 
                    bg='white', fg='#2c3e50').grid(row=i, column=0, padx=20, pady=15, sticky='w')
            
            entry = tk.Entry(form_frame, font=('Arial', 12), width=30)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=20, pady=15, sticky='ew')
            entries[field] = entry
        
        # Date of Birth
        tk.Label(form_frame, text="Date of Birth", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').grid(row=len(fields), column=0, padx=20, pady=15, sticky='w')
        
        dob_frame = tk.Frame(form_frame, bg='white')
        dob_frame.grid(row=len(fields), column=1, padx=20, pady=15, sticky='ew')
        
        # Date dropdowns (simplified)
        dob_entry = tk.Entry(dob_frame, font=('Arial', 12), width=30)
        if profile['date_of_birth']:
            dob_entry.insert(0, str(profile['date_of_birth']))
        dob_entry.pack(fill=tk.X)
        entries['date_of_birth'] = dob_entry
        
        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)
        
        def save_profile():
            updated_data = {}
            for field, entry in entries.items():
                updated_data[field] = entry.get()
            
            # Update profile in database
            if self.auth.update_user_profile(self.user_data['id'], updated_data):
                messagebox.showinfo("Success", "Profile updated successfully!")
                edit_window.destroy()
                # Refresh profile tab
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", "Failed to update profile")
        
        # Save button
        save_btn = tk.Button(edit_window, text="Save Changes", 
                           font=('Arial', 14, 'bold'), bg='#27ae60', fg='white',
                           padx=20, pady=10, command=save_profile)
        save_btn.pack(pady=20)
    
    def refresh_dashboard(self):
        """Refresh the dashboard to show updated data"""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_dashboard()
    
    def create_services_tab(self, parent):
        # Services container
        services_container = tk.Frame(parent, bg='#f5f6fa')
        services_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(services_container, text="Available Government Services", 
                font=('Arial', 18, 'bold'), bg='#f5f6fa', fg='#2c3e50').pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(services_container, bg='#f5f6fa')
        search_frame.pack(fill=tk.X, pady=10)
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 12), width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.insert(0, "Search services...")
        self.search_entry.config(fg='grey')
        
        # Bind events for search functionality
        self.search_entry.bind('<FocusIn>', self.clear_search_placeholder)
        self.search_entry.bind('<FocusOut>', self.set_search_placeholder)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_services())
        
        search_btn = tk.Button(search_frame, text="Search", font=('Arial', 10),
                              bg='#3498db', fg='white', command=self.search_services)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(search_frame, text="Clear", font=('Arial', 10),
                             bg='#95a5a6', fg='white', command=self.clear_search)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Services frame
        self.services_frame = tk.Frame(services_container, bg='#f5f6fa')
        self.services_frame.pack(fill=tk.BOTH, expand=True)
        
        # Load services
        self.load_services(self.services_frame)
    
    def clear_search_placeholder(self, event=None):
        if self.search_entry.get() == "Search services...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg='black')
    
    def set_search_placeholder(self, event=None):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search services...")
            self.search_entry.config(fg='grey')
    
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.set_search_placeholder()
        self.search_services()
    
    def load_services(self, parent_frame, services=None):
        # Clear existing services
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        if services is None:
            services = self.auth.get_all_services()
        
        if not services:
            no_services_label = tk.Label(parent_frame, text="No services found", 
                                       font=('Arial', 14), bg='#f5f6fa', fg='#7f8c8d')
            no_services_label.pack(pady=50)
            return
        
        # Create a canvas and scrollbar for services
        canvas = tk.Canvas(parent_frame, bg='#f5f6fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f5f6fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display services as cards
        row, col = 0, 0
        max_columns = 3
        
        for i, service in enumerate(services):
            if service.get('status', 'active') != 'active':
                continue
                
            card_frame = tk.Frame(scrollable_frame, bg='white', relief='raised', bd=1)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Service name
            tk.Label(card_frame, text=service['name'], 
                    font=('Arial', 14, 'bold'), bg='white', fg='#2c3e50').pack(pady=10, padx=15, anchor='w')
            
            # Service description
            desc_text = service.get('description', 'No description available')
            desc_label = tk.Label(card_frame, text=desc_text, 
                    font=('Arial', 10), bg='white', fg='#7f8c8d', wraplength=200, justify='left')
            desc_label.pack(pady=5, padx=15, anchor='w')
            
            # Service details
            details_frame = tk.Frame(card_frame, bg='white')
            details_frame.pack(fill=tk.X, padx=15, pady=5)
            
            tk.Label(details_frame, text=f"Category: {service.get('category', 'General')}", 
                    font=('Arial', 9), bg='white', fg='#3498db').pack(anchor='w')
            
            fee = service.get('fee', 0)
            fee_text = f"Fee: ${fee}" if fee and fee > 0 else "Fee: Free"
            tk.Label(details_frame, text=fee_text, 
                    font=('Arial', 9), bg='white', fg='#27ae60').pack(anchor='w')
            
            tk.Label(details_frame, text=f"Processing: {service.get('processing_time', '1-2 weeks')}", 
                    font=('Arial', 9), bg='white', fg='#f39c12').pack(anchor='w')
            
            # Requirements if available
            if service.get('requirements'):
                req_frame = tk.Frame(card_frame, bg='white')
                req_frame.pack(fill=tk.X, padx=15, pady=5)
                req_label = tk.Label(req_frame, text=f"Requirements: {service['requirements']}", 
                        font=('Arial', 8), bg='white', fg='#e74c3c', wraplength=200, justify='left')
                req_label.pack(anchor='w')
            
            # Apply button
            apply_btn = tk.Button(card_frame, text="Apply Now", font=('Arial', 10, 'bold'),
                     bg='#27ae60', fg='white', padx=15, pady=5,
                     command=lambda s=service: self.apply_service(s))
            apply_btn.pack(pady=10)
            
            # View Details button
            details_btn = tk.Button(card_frame, text="View Details", font=('Arial', 9),
                                  bg='#3498db', fg='white', padx=10, pady=3,
                                  command=lambda s=service: self.view_service_details(s))
            details_btn.pack(pady=(0, 10))
            
            col += 1
            if col >= max_columns:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(max_columns):
            scrollable_frame.columnconfigure(i, weight=1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def search_services(self, query=None):
        if query is None:
            query = self.search_entry.get()
        
        if query == "Search services..." or not query.strip():
            services = self.auth.get_all_services()
        else:
            services = self.auth.search_services(query)
        
        # Reload services with filtered results
        self.load_services(self.services_frame, services)
    
    def view_service_details(self, service):
        """Show detailed view of a service"""
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Service Details - {service['name']}")
        details_window.geometry("500x400")
        details_window.configure(bg='#ecf0f1')
        details_window.transient(self.root)
        
        # Header
        header_frame = tk.Frame(details_window, bg='#3498db', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=service['name'], 
                font=('Arial', 16, 'bold'), fg='white', bg='#3498db').pack(pady=20)
        
        # Content
        content_frame = tk.Frame(details_window, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        details = [
            ("Description", service.get('description', 'No description available')),
            ("Category", service.get('category', 'General')),
            ("Fee", f"${service.get('fee', 0)}" if service.get('fee', 0) > 0 else "Free"),
            ("Processing Time", service.get('processing_time', '1-2 weeks')),
            ("Requirements", service.get('requirements', 'None specified')),
            ("Status", service.get('status', 'active').title())
        ]
        
        for i, (label, value) in enumerate(details):
            row_frame = tk.Frame(content_frame, bg='white')
            row_frame.pack(fill=tk.X, pady=8)
            
            tk.Label(row_frame, text=f"{label}:", font=('Arial', 11, 'bold'), 
                    bg='white', fg='#2c3e50', width=15, anchor='w').pack(side=tk.LEFT)
            value_label = tk.Label(row_frame, text=value, font=('Arial', 11), 
                    bg='white', fg='#34495e', wraplength=300, justify='left')
            value_label.pack(side=tk.LEFT, padx=10)
        
        # Apply button
        apply_btn = tk.Button(details_window, text="Apply for this Service", 
                            font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                            padx=20, pady=10, command=lambda: self.apply_service(service))
        apply_btn.pack(pady=20)
    
    def apply_service(self, service):
        """Create application form - FIXED VERSION"""
        print(f"Applying for service: {service['name']}")
        
        # Create application form
        form_window = tk.Toplevel(self.root)
        form_window.title(f"Apply for {service['name']}")
        form_window.geometry("500x500")
        form_window.configure(bg='#ecf0f1')
        form_window.transient(self.root)
        form_window.grab_set()
        
        # Header
        header_frame = tk.Frame(form_window, bg='#3498db', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"Application for {service['name']}", 
                font=('Arial', 16, 'bold'), fg='white', bg='#3498db').pack(pady=20)
        
        # Application details
        details_frame = tk.Frame(form_window, bg='white')
        details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(details_frame, text="Service Details:", 
                font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', pady=10)
        
        # Show service requirements
        if service.get('requirements'):
            req_frame = tk.Frame(details_frame, bg='white', relief='sunken', bd=1)
            req_frame.pack(fill=tk.X, pady=5, padx=5, ipady=5)
            tk.Label(req_frame, text=f"Requirements: {service['requirements']}", 
                    font=('Arial', 10), bg='white', wraplength=400, justify='left').pack(anchor='w', padx=5, pady=5)
        
        tk.Label(details_frame, text="Application Details:", 
                font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', pady=(20,5))
        
        # Additional information field
        tk.Label(details_frame, text="Additional Information (if needed):", 
                font=('Arial', 10), bg='white').pack(anchor='w', pady=(10,5))
        
        details_text = scrolledtext.ScrolledText(details_frame, height=8, width=50, font=('Arial', 10))
        details_text.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # File upload section
        file_frame = tk.Frame(details_frame, bg='white')
        file_frame.pack(fill=tk.X, pady=10)
        
        uploaded_files = []  # Local variable for this form
        upload_btn = tk.Button(file_frame, text="Upload Document", font=('Arial', 9),
                              bg='#3498db', fg='white', 
                              command=lambda: self.upload_document(uploaded_files, file_label))
        upload_btn.pack(side=tk.LEFT, padx=5)
        
        file_label = tk.Label(file_frame, text="No files uploaded", 
                                  font=('Arial', 9), bg='white', fg='#7f8c8d')
        file_label.pack(side=tk.LEFT, padx=5)
        
        def submit_application():
            print("Submit application button clicked")
            
            application_data = details_text.get("1.0", tk.END).strip()
            
            # Validate required fields
            if service.get('requirements') and not application_data:
                messagebox.showwarning("Warning", "Please provide the required information for this application")
                return
            
            print(f"Submitting application for service ID: {service['id']}")
            
            # Save application to database - FIXED: Use positional arguments
            application_id = self.auth.create_application(
                self.user_data['id'],  # user_id (positional)
                service['id'],         # service_id (positional)
                application_data,      # details (positional)
                uploaded_files         # uploaded_files (positional)
            )
            
            print(f"Application ID returned: {application_id}")
            
            if application_id:
                messagebox.showinfo("Success", 
                                  f"Application for {service['name']} submitted successfully!\n\n"
                                  f"Application ID: {application_id}\n"
                                  f"Your application will be processed within {service.get('processing_time', 'specified time')}.")
                form_window.destroy()
                
                # Refresh applications tab if it exists
                if hasattr(self, 'applications_tree'):
                    self.load_applications_data()
            else:
                messagebox.showerror("Error", "Failed to submit application. Please try again.")
        
        # Button frame
        button_frame = tk.Frame(form_window, bg='#ecf0f1')
        button_frame.pack(fill=tk.X, pady=10)
        
        submit_btn = tk.Button(button_frame, text="Submit Application", font=('Arial', 12, 'bold'),
                              bg='#27ae60', fg='white', padx=20, pady=10,
                              command=submit_application)
        submit_btn.pack(side=tk.LEFT, padx=20)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", font=('Arial', 12),
                              bg='#95a5a6', fg='white', padx=20, pady=10,
                              command=form_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=20)
    
    def upload_document(self, uploaded_files, file_label):
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[("All files", "*.*"), 
                      ("PDF files", "*.pdf"), 
                      ("Image files", "*.jpg *.jpeg *.png"),
                      ("Document files", "*.doc *.docx *.txt")]
        )
        if file_path:
            # Create uploads directory if it doesn't exist
            upload_dir = "uploads"
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            # Copy file to uploads directory
            filename = os.path.basename(file_path)
            destination = os.path.join(upload_dir, filename)
            shutil.copy2(file_path, destination)
            
            uploaded_files.append(destination)
            file_label.config(text=f"{len(uploaded_files)} file(s) uploaded")
    
    def create_applications_tab(self, parent):
        applications_container = tk.Frame(parent, bg='#f5f6fa')
        applications_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(applications_container, text="My Applications", 
                font=('Arial', 18, 'bold'), bg='#f5f6fa', fg='#2c3e50').pack(pady=20)
        
        # Search and filter frame
        search_frame = tk.Frame(applications_container, bg='#f5f6fa')
        search_frame.pack(fill=tk.X, pady=10)
        
        self.app_search_entry = tk.Entry(search_frame, font=('Arial', 12), width=30)
        self.app_search_entry.pack(side=tk.LEFT, padx=5)
        self.app_search_entry.insert(0, "Search applications...")
        self.app_search_entry.bind('<KeyRelease>', lambda e: self.search_applications())
        
        search_btn = tk.Button(search_frame, text="Search", font=('Arial', 10),
                              bg='#3498db', fg='white', command=lambda: self.search_applications(self.app_search_entry.get()))
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Status filter
        status_frame = tk.Frame(search_frame, bg='#f5f6fa')
        status_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(status_frame, text="Filter by Status:", font=('Arial', 10), 
                bg='#f5f6fa').pack(side=tk.LEFT)
        
        self.status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(status_frame, textvariable=self.status_var,
                                   values=["All", "Pending", "Processing", "Approved", "Rejected", "Completed"],
                                   state="readonly", width=12)
        status_combo.pack(side=tk.LEFT, padx=5)
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_applications_by_status())
        
        refresh_btn = tk.Button(search_frame, text="Refresh", font=('Arial', 10),
                               bg='#27ae60', fg='white', command=self.load_applications_data)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Applications list
        tree_frame = tk.Frame(applications_container, bg='#f5f6fa')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview
        self.applications_tree = ttk.Treeview(tree_frame, columns=('ID', 'Service', 'Status', 'Date', 'Officer', 'Remarks'), show='headings')
        
        self.applications_tree.heading('ID', text='Application ID')
        self.applications_tree.heading('Service', text='Service')
        self.applications_tree.heading('Status', text='Status')
        self.applications_tree.heading('Date', text='Applied Date')
        self.applications_tree.heading('Officer', text='Assigned Officer')
        self.applications_tree.heading('Remarks', text='Remarks')
        
        self.applications_tree.column('ID', width=80)
        self.applications_tree.column('Service', width=150)
        self.applications_tree.column('Status', width=100)
        self.applications_tree.column('Date', width=100)
        self.applications_tree.column('Officer', width=120)
        self.applications_tree.column('Remarks', width=200)
        
        # Load applications data
        self.load_applications_data()
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.applications_tree.yview)
        self.applications_tree.configure(yscrollcommand=scrollbar.set)
        
        self.applications_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click event
        self.applications_tree.bind('<Double-1>', lambda e: self.view_application_details())
        
        # Action buttons
        button_frame = tk.Frame(applications_container, bg='#f5f6fa')
        button_frame.pack(fill=tk.X, pady=10)
        
        view_btn = tk.Button(button_frame, text="View Details", font=('Arial', 10),
                 bg='#3498db', fg='white', padx=15, command=self.view_application_details)
        view_btn.pack(side=tk.LEFT, padx=5)
        
        status_btn = tk.Button(button_frame, text="Check Status", font=('Arial', 10),
                 bg='#f39c12', fg='white', padx=15, command=self.check_application_status)
        status_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(button_frame, text="Cancel Application", font=('Arial', 10),
                 bg='#e74c3c', fg='white', padx=15, command=self.cancel_application)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        update_btn = tk.Button(button_frame, text="Update Application", font=('Arial', 10),
                 bg='#9b59b6', fg='white', padx=15, command=self.update_application)
        update_btn.pack(side=tk.LEFT, padx=5)

    def load_applications_data(self):
        # Clear existing data
        for item in self.applications_tree.get_children():
            self.applications_tree.delete(item)

        # Load applications from database
        applications = self.auth.get_user_applications(self.user_data['id'])

        for app in applications:
            # Use officer_name instead of assigned_officer
            officer_display = app.get('officer_name') or app.get('officer_full_name') or 'Not assigned'
            remarks = app.get('notes') or 'No remarks'

            self.applications_tree.insert('', 'end', values=(
                app['id'],
                app['service_name'],
                app['status'],
                app['applied_date'].strftime('%Y-%m-%d') if app['applied_date'] else 'N/A',
                officer_display,
                remarks
            ))
    def search_applications(self, query=None):
        if query is None:
            query = self.app_search_entry.get()

        if query == "Search applications..." or not query.strip():
            self.load_applications_data()
        else:
            # Filter applications based on search query
            for item in self.applications_tree.get_children():
                self.applications_tree.delete(item)

            filtered_apps = self.auth.search_applications(self.user_data['id'], query)
            for app in filtered_apps:
                # Use officer_name instead of assigned_officer
                officer_display = app.get('officer_name') or app.get('officer_full_name') or 'Not assigned'
                remarks = app.get('notes') or 'No remarks'

                self.applications_tree.insert('', 'end', values=(
                    app['id'],
                    app['service_name'],
                    app['status'],
                    app['applied_date'].strftime('%Y-%m-%d') if app['applied_date'] else 'N/A',
                    officer_display,
                    remarks
                ))

    def filter_applications_by_status(self):
        status = self.status_var.get()
        if status == "All":
            self.load_applications_data()
        else:
            for item in self.applications_tree.get_children():
                self.applications_tree.delete(item)

            # Map display status to database status
            status_mapping = {
                "Pending": "pending",
                "Processing": "under_review",
                "Approved": "approved",
                "Rejected": "rejected",
                "Completed": "completed"
            }

            db_status = status_mapping.get(status, status.lower())
            filtered_apps = self.auth.get_applications_by_status(self.user_data['id'], db_status)

            for app in filtered_apps:
                # Use officer_name instead of assigned_officer
                officer_display = app.get('officer_name') or app.get('officer_full_name') or 'Not assigned'
                remarks = app.get('notes') or 'No remarks'

                self.applications_tree.insert('', 'end', values=(
                    app['id'],
                    app['service_name'],
                    app['status'],
                    app['applied_date'].strftime('%Y-%m-%d') if app['applied_date'] else 'N/A',
                    officer_display,
                    remarks
                ))

    def view_application_details(self):
        selection = self.applications_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application to view details")
            return

        item = self.applications_tree.item(selection[0])
        app_id = item['values'][0]

        # Get application details from database
        application = self.auth.get_application_details(app_id)

        if not application:
            messagebox.showerror("Error", "Could not load application details")
            return

        details_window = tk.Toplevel(self.root)
        details_window.title(f"Application Details - #{app_id}")
        details_window.geometry("600x500")
        details_window.configure(bg='#ecf0f1')

        # Header
        header_frame = tk.Frame(details_window, bg='#3498db', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text=f"Application #{app_id}",
                 font=('Arial', 16, 'bold'), fg='white', bg='#3498db').pack(pady=20)

        # Content
        content_frame = tk.Frame(details_window, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Use officer_name instead of assigned_officer
        officer_display = application.get('officer_name') or application.get('officer_full_name') or 'Not assigned'

        details = [
            ("Service", application['service_name']),
            ("Status", application['status']),
            ("Applied Date",
             application['applied_date'].strftime('%Y-%m-%d %H:%M') if application['applied_date'] else 'N/A'),
            ("Last Updated",
             application['updated_at'].strftime('%Y-%m-%d %H:%M') if application['updated_at'] else 'N/A'),
            ("Assigned Officer", officer_display),
            ("Remarks", application.get('notes') or 'No remarks'),
            ("Application Details", application.get('application_data') or 'No additional details')
        ]

        for i, (label, value) in enumerate(details):
            row_frame = tk.Frame(content_frame, bg='white')
            row_frame.pack(fill=tk.X, pady=8)

            tk.Label(row_frame, text=f"{label}:", font=('Arial', 11, 'bold'),
                     bg='white', fg='#2c3e50', width=15, anchor='w').pack(side=tk.LEFT)

            # Use text widget for longer values
            if label == "Application Details" and len(value) > 50:
                text_widget = scrolledtext.ScrolledText(row_frame, height=4, width=50, font=('Arial', 10))
                text_widget.insert('1.0', value)
                text_widget.config(state='disabled')
                text_widget.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
            else:
                tk.Label(row_frame, text=value, font=('Arial', 11),
                         bg='white', fg='#34495e', wraplength=400, justify='left').pack(side=tk.LEFT, padx=10)
    def check_application_status(self):
        selection = self.applications_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application to check status")
            return
        
        item = self.applications_tree.item(selection[0])
        app_id = item['values'][0]
        status = item['values'][2]
        
        messagebox.showinfo("Application Status", 
                          f"Application ID: {app_id}\n"
                          f"Current Status: {status}\n\n"
                          f"You will be notified when there are updates to your application.")
    
    def cancel_application(self):
        selection = self.applications_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application to cancel")
            return
        
        item = self.applications_tree.item(selection[0])
        app_id = item['values'][0]
        service_name = item['values'][1]
        current_status = item['values'][2]
        
        if current_status in ['Approved', 'Completed', 'Rejected']:
            messagebox.showwarning("Cannot Cancel", 
                                 f"This application cannot be cancelled because it's already {current_status}.")
            return
        
        confirm = messagebox.askyesno("Confirm Cancellation", 
                                     f"Are you sure you want to cancel your application for {service_name}?")
        
        if confirm:
            if self.auth.cancel_application(app_id):
                messagebox.showinfo("Success", "Application cancelled successfully")
                self.load_applications_data()
            else:
                messagebox.showerror("Error", "Failed to cancel application")
    
    def update_application(self):
        selection = self.applications_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application to update")
            return
        
        item = self.applications_tree.item(selection[0])
        app_id = item['values'][0]
        service_name = item['values'][1]
        current_status = item['values'][2]
        
        if current_status in ['Approved', 'Completed', 'Rejected']:
            messagebox.showwarning("Cannot Update", 
                                 f"This application cannot be updated because it's already {current_status}.")
            return
        
        # Create update window
        update_window = tk.Toplevel(self.root)
        update_window.title(f"Update Application - #{app_id}")
        update_window.geometry("500x400")
        update_window.configure(bg='#ecf0f1')
        
        tk.Label(update_window, text=f"Update Application for {service_name}", 
                font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(pady=20)
        
        # Update form
        form_frame = tk.Frame(update_window, bg='white', relief='raised', bd=1)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(form_frame, text="Additional Information or Updates:", 
                font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', pady=10, padx=20)
        
        update_text = scrolledtext.ScrolledText(form_frame, height=10, width=50, font=('Arial', 11))
        update_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # File upload for additional documents
        file_frame = tk.Frame(form_frame, bg='white')
        file_frame.pack(fill=tk.X, pady=10, padx=20)
        
        self.update_uploaded_files = []
        upload_btn = tk.Button(file_frame, text="Upload Additional Documents", font=('Arial', 9),
                              bg='#3498db', fg='white', command=lambda: self.upload_update_document())
        upload_btn.pack(side=tk.LEFT, padx=5)
        
        self.update_file_label = tk.Label(file_frame, text="No files uploaded", 
                                         font=('Arial', 9), bg='white', fg='#7f8c8d')
        self.update_file_label.pack(side=tk.LEFT, padx=5)
        
        def submit_update():
            update_data = update_text.get("1.0", tk.END).strip()
            
            if not update_data and not self.update_uploaded_files:
                messagebox.showwarning("Warning", "Please provide update information or upload documents")
                return
            
            if self.auth.update_application(app_id, update_data, self.update_uploaded_files):
                messagebox.showinfo("Success", "Application updated successfully")
                update_window.destroy()
                self.load_applications_data()
            else:
                messagebox.showerror("Error", "Failed to update application")
        
        # Buttons
        button_frame = tk.Frame(update_window, bg='#ecf0f1')
        button_frame.pack(fill=tk.X, pady=10)
        
        submit_btn = tk.Button(button_frame, text="Submit Update", font=('Arial', 12, 'bold'),
                              bg='#27ae60', fg='white', padx=20, pady=10, command=submit_update)
        submit_btn.pack(side=tk.LEFT, padx=20)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", font=('Arial', 12),
                              bg='#95a5a6', fg='white', padx=20, pady=10, command=update_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=20)
    
    def upload_update_document(self):
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[("All files", "*.*"), 
                      ("PDF files", "*.pdf"), 
                      ("Image files", "*.jpg *.jpeg *.png"),
                      ("Document files", "*.doc *.docx *.txt")]
        )
        if file_path:
            self.update_uploaded_files.append(file_path)
            self.update_file_label.config(text=f"{len(self.update_uploaded_files)} file(s) uploaded")
    
    def create_reports_tab(self, parent):
        reports_container = tk.Frame(parent, bg='#f5f6fa')
        reports_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(reports_container, text="Submit Report/Complaint", 
                font=('Arial', 18, 'bold'), bg='#f5f6fa', fg='#2c3e50').pack(pady=20)
        
        # Report form
        form_frame = tk.Frame(reports_container, bg='white', relief='raised', bd=1)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        # Title
        tk.Label(form_frame, text="Report Title*:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(20,5), padx=20)
        self.title_entry = tk.Entry(form_frame, font=('Arial', 12), width=50)
        self.title_entry.pack(fill=tk.X, pady=5, padx=20, ipady=5)
        
        # Category
        tk.Label(form_frame, text="Category*:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(15,5), padx=20)
        self.category_var = tk.StringVar(value="General Complaint")
        category_combo = ttk.Combobox(form_frame, textvariable=self.category_var,
                                     values=["General Complaint", "Infrastructure Issue", 
                                             "Service Complaint", "Emergency", "Suggestion", "Other"],
                                     state="readonly", font=('Arial', 12))
        category_combo.pack(fill=tk.X, pady=5, padx=20, ipady=5)
        
        # Priority
        tk.Label(form_frame, text="Priority:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(15,5), padx=20)
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(form_frame, textvariable=self.priority_var,
                                     values=["Low", "Medium", "High", "Urgent"],
                                     state="readonly", font=('Arial', 12))
        priority_combo.pack(fill=tk.X, pady=5, padx=20, ipady=5)
        
        # Description
        tk.Label(form_frame, text="Description*:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(15,5), padx=20)
        self.desc_text = scrolledtext.ScrolledText(form_frame, font=('Arial', 11), height=8)
        self.desc_text.pack(fill=tk.BOTH, expand=True, pady=5, padx=20)
        
        # Location
        tk.Label(form_frame, text="Location (optional):", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(15,5), padx=20)
        self.location_entry = tk.Entry(form_frame, font=('Arial', 12), width=50)
        self.location_entry.pack(fill=tk.X, pady=5, padx=20, ipady=5)
        
        # Image upload
        self.report_image_path = None
        image_frame = tk.Frame(form_frame, bg='white')
        image_frame.pack(fill=tk.X, pady=10, padx=20)
        
        upload_btn = tk.Button(image_frame, text="Upload Image/Evidence", font=('Arial', 10),
                              bg='#3498db', fg='white', command=self.upload_report_image)
        upload_btn.pack(side=tk.LEFT, padx=5)
        
        self.report_image_label = tk.Label(image_frame, text="No image selected", 
                                          font=('Arial', 10), bg='white', fg='#7f8c8d')
        self.report_image_label.pack(side=tk.LEFT, padx=5)
        
        # Submit button
        submit_btn = tk.Button(form_frame, text="Submit Report", font=('Arial', 14, 'bold'),
                              bg='#27ae60', fg='white', padx=30, pady=10,
                              command=self.submit_report)
        submit_btn.pack(pady=20)
        
        # Clear form button
        clear_btn = tk.Button(form_frame, text="Clear Form", font=('Arial', 11),
                             bg='#95a5a6', fg='white', padx=20, pady=5,
                             command=self.clear_report_form)
        clear_btn.pack(pady=(0, 20))
    
    def upload_report_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image/Evidence",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
                      ("All files", "*.*")]
        )
        if file_path:
            self.report_image_path = file_path
            self.report_image_label.config(text=os.path.basename(file_path))
    
    def clear_report_form(self):
        self.title_entry.delete(0, tk.END)
        self.category_var.set("General Complaint")
        self.priority_var.set("Medium")
        self.desc_text.delete('1.0', tk.END)
        self.location_entry.delete(0, tk.END)
        self.report_image_path = None
        self.report_image_label.config(text="No image selected")
    
    def submit_report(self):
        title = self.title_entry.get().strip()
        category = self.category_var.get()
        priority = self.priority_var.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        location = self.location_entry.get().strip()
        
        if not title or not description:
            messagebox.showwarning("Warning", "Please fill in all required fields (Title and Description)")
            return
        
        # Save report to database - FIXED: Use positional arguments
        report_id = self.auth.create_report(
            self.user_data['id'],  # user_id (positional)
            title,                 # title (positional)
            category,              # category (positional)
            priority,              # priority (positional)
            description,           # description (positional)
            location,              # location (positional)
            self.report_image_path # image_path (positional)
        )
        
        if report_id:
            messagebox.showinfo("Success", 
                              f"Report submitted successfully!\n\n"
                              f"Report ID: {report_id}\n"
                              f"Your report has been recorded and will be processed shortly. "
                              f"You can track the status in 'My Reports' section.")
            self.clear_report_form()
            
            # Refresh my reports tab if it exists
            if hasattr(self, 'reports_tree'):
                self.load_reports_data()
        else:
            messagebox.showerror("Error", "Failed to submit report. Please try again.")
    
    def create_my_reports_tab(self, parent):
        my_reports_container = tk.Frame(parent, bg='#f5f6fa')
        my_reports_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(my_reports_container, text="My Reports", 
                font=('Arial', 18, 'bold'), bg='#f5f6fa', fg='#2c3e50').pack(pady=20)
        
        # Search and filter frame
        search_frame = tk.Frame(my_reports_container, bg='#f5f6fa')
        search_frame.pack(fill=tk.X, pady=10)
        
        self.report_search_entry = tk.Entry(search_frame, font=('Arial', 12), width=30)
        self.report_search_entry.pack(side=tk.LEFT, padx=5)
        self.report_search_entry.insert(0, "Search reports...")
        self.report_search_entry.bind('<KeyRelease>', lambda e: self.search_my_reports())
        
        search_btn = tk.Button(search_frame, text="Search", font=('Arial', 10),
                              bg='#3498db', fg='white', command=lambda: self.search_my_reports(self.report_search_entry.get()))
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Status filter
        status_frame = tk.Frame(search_frame, bg='#f5f6fa')
        status_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(status_frame, text="Filter by Status:", font=('Arial', 10), 
                bg='#f5f6fa').pack(side=tk.LEFT)
        
        self.report_status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(status_frame, textvariable=self.report_status_var,
                                   values=["All", "Submitted", "Under Review", "In Progress", "Resolved", "Closed"],
                                   state="readonly", width=12)
        status_combo.pack(side=tk.LEFT, padx=5)
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_reports_by_status())
        
        refresh_btn = tk.Button(search_frame, text="Refresh", font=('Arial', 10),
                               bg='#27ae60', fg='white', command=self.load_reports_data)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Reports list
        tree_frame = tk.Frame(my_reports_container, bg='#f5f6fa')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview
        self.reports_tree = ttk.Treeview(tree_frame, columns=('ID', 'Title', 'Category', 'Status', 'Priority', 'Submitted Date'), show='headings')
        
        self.reports_tree.heading('ID', text='Report ID')
        self.reports_tree.heading('Title', text='Title')
        self.reports_tree.heading('Category', text='Category')
        self.reports_tree.heading('Status', text='Status')
        self.reports_tree.heading('Priority', text='Priority')
        self.reports_tree.heading('Submitted Date', text='Submitted Date')
        
        self.reports_tree.column('ID', width=80)
        self.reports_tree.column('Title', width=200)
        self.reports_tree.column('Category', width=120)
        self.reports_tree.column('Status', width=100)
        self.reports_tree.column('Priority', width=80)
        self.reports_tree.column('Submitted Date', width=120)
        
        # Load reports data
        self.load_reports_data()
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.reports_tree.yview)
        self.reports_tree.configure(yscrollcommand=scrollbar.set)
        
        self.reports_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click event
        self.reports_tree.bind('<Double-1>', lambda e: self.view_report_details())
        
        # Action buttons
        button_frame = tk.Frame(my_reports_container, bg='#f5f6fa')
        button_frame.pack(fill=tk.X, pady=10)
        
        view_btn = tk.Button(button_frame, text="View Details", font=('Arial', 10),
                 bg='#3498db', fg='white', padx=15, command=self.view_report_details)
        view_btn.pack(side=tk.LEFT, padx=5)
        
        status_btn = tk.Button(button_frame, text="Check Status", font=('Arial', 10),
                 bg='#f39c12', fg='white', padx=15, command=self.check_report_status)
        status_btn.pack(side=tk.LEFT, padx=5)
        
        update_btn = tk.Button(button_frame, text="Update Report", font=('Arial', 10),
                 bg='#9b59b6', fg='white', padx=15, command=self.update_report)
        update_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(button_frame, text="Close Report", font=('Arial', 10),
                 bg='#e74c3c', fg='white', padx=15, command=self.close_report)
        close_btn.pack(side=tk.LEFT, padx=5)
    
    def load_reports_data(self):
        # Clear existing data
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)
        
        # Load reports from database
        reports = self.auth.get_user_reports(self.user_data['id'])
        
        for report in reports:
            self.reports_tree.insert('', 'end', values=(
                report['id'],
                report['title'],
                report['category'],
                report['status'],
                report['priority'],
                report['submitted_date'].strftime('%Y-%m-%d') if report['submitted_date'] else 'N/A'
            ))
    
    def search_my_reports(self, query=None):
        if query is None:
            query = self.report_search_entry.get()
        
        if query == "Search reports..." or not query.strip():
            self.load_reports_data()
        else:
            # Filter reports based on search query
            for item in self.reports_tree.get_children():
                self.reports_tree.delete(item)
            
            filtered_reports = self.auth.search_reports(self.user_data['id'], query)
            for report in filtered_reports:
                self.reports_tree.insert('', 'end', values=(
                    report['id'],
                    report['title'],
                    report['category'],
                    report['status'],
                    report['priority'],
                    report['submitted_date'].strftime('%Y-%m-%d') if report['submitted_date'] else 'N/A'
                ))
    
    def filter_reports_by_status(self):
        status = self.report_status_var.get()
        if status == "All":
            self.load_reports_data()
        else:
            for item in self.reports_tree.get_children():
                self.reports_tree.delete(item)
            
            filtered_reports = self.auth.get_reports_by_status(self.user_data['id'], status)
            for report in filtered_reports:
                self.reports_tree.insert('', 'end', values=(
                    report['id'],
                    report['title'],
                    report['category'],
                    report['status'],
                    report['priority'],
                    report['submitted_date'].strftime('%Y-%m-%d') if report['submitted_date'] else 'N/A'
                ))
    
    def view_report_details(self):
        selection = self.reports_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report to view details")
            return
        
        item = self.reports_tree.item(selection[0])
        report_id = item['values'][0]
        
        # Get report details from database
        report = self.auth.get_report_details(report_id)
        
        if not report:
            messagebox.showerror("Error", "Could not load report details")
            return
        
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Report Details - #{report_id}")
        details_window.geometry("600x500")
        details_window.configure(bg='#ecf0f1')
        
        # Header
        header_frame = tk.Frame(details_window, bg='#3498db', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"Report #{report_id}", 
                font=('Arial', 16, 'bold'), fg='white', bg='#3498db').pack(pady=20)
        
        # Content
        content_frame = tk.Frame(details_window, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        details = [
            ("Title", report['title']),
            ("Category", report['category']),
            ("Status", report['status']),
            ("Priority", report['priority']),
            ("Submitted Date", report['submitted_date'].strftime('%Y-%m-%d %H:%M') if report['submitted_date'] else 'N/A'),
            ("Last Updated", report['updated_at'].strftime('%Y-%m-%d %H:%M') if report['updated_at'] else 'N/A'),
            ("Location", report['location'] or 'Not specified'),
            ("Description", report['description'] or 'No description')
        ]
        
        for i, (label, value) in enumerate(details):
            row_frame = tk.Frame(content_frame, bg='white')
            row_frame.pack(fill=tk.X, pady=8)
            
            tk.Label(row_frame, text=f"{label}:", font=('Arial', 11, 'bold'), 
                    bg='white', fg='#2c3e50', width=15, anchor='w').pack(side=tk.LEFT)
            
            # Use text widget for longer values
            if label == "Description" and len(value) > 50:
                text_widget = scrolledtext.ScrolledText(row_frame, height=4, width=50, font=('Arial', 10))
                text_widget.insert('1.0', value)
                text_widget.config(state='disabled')
                text_widget.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
            else:
                tk.Label(row_frame, text=value, font=('Arial', 11), 
                        bg='white', fg='#34495e', wraplength=400, justify='left').pack(side=tk.LEFT, padx=10)
        
        # Show image if available
        if report.get('image_path'):
            img_frame = tk.Frame(content_frame, bg='white')
            img_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(img_frame, text="Attached Image:", font=('Arial', 11, 'bold'), 
                    bg='white', fg='#2c3e50').pack(anchor='w')
            
            try:
                img = Image.open(report['image_path'])
                img.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(img_frame, image=photo, bg='white')
                img_label.image = photo  # Keep a reference
                img_label.pack(pady=5)
            except Exception as e:
                tk.Label(img_frame, text=f"Could not load image: {str(e)}", 
                        font=('Arial', 9), bg='white', fg='#e74c3c').pack()
    
    def check_report_status(self):
        selection = self.reports_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report to check status")
            return
        
        item = self.reports_tree.item(selection[0])
        report_id = item['values'][0]
        status = item['values'][3]
        priority = item['values'][4]
        
        messagebox.showinfo("Report Status", 
                          f"Report ID: {report_id}\n"
                          f"Current Status: {status}\n"
                          f"Priority: {priority}\n\n"
                          f"You will be notified when there are updates to your report.")
    
    def update_report(self):
        selection = self.reports_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report to update")
            return
        
        item = self.reports_tree.item(selection[0])
        report_id = item['values'][0]
        title = item['values'][1]
        current_status = item['values'][3]
        
        if current_status in ['Resolved', 'Closed']:
            messagebox.showwarning("Cannot Update", 
                                 f"This report cannot be updated because it's already {current_status}.")
            return
        
        # Create update window
        update_window = tk.Toplevel(self.root)
        update_window.title(f"Update Report - #{report_id}")
        update_window.geometry("500x400")
        update_window.configure(bg='#ecf0f1')
        
        tk.Label(update_window, text=f"Update Report: {title}", 
                font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(pady=20)
        
        # Update form
        form_frame = tk.Frame(update_window, bg='white', relief='raised', bd=1)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(form_frame, text="Additional Information or Updates:", 
                font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', pady=10, padx=20)
        
        update_text = scrolledtext.ScrolledText(form_frame, height=10, width=50, font=('Arial', 11))
        update_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # File upload for additional evidence
        file_frame = tk.Frame(form_frame, bg='white')
        file_frame.pack(fill=tk.X, pady=10, padx=20)
        
        self.report_update_files = []
        upload_btn = tk.Button(file_frame, text="Upload Additional Evidence", font=('Arial', 9),
                              bg='#3498db', fg='white', command=lambda: self.upload_report_update_file())
        upload_btn.pack(side=tk.LEFT, padx=5)
        
        self.report_update_file_label = tk.Label(file_frame, text="No files uploaded", 
                                                font=('Arial', 9), bg='white', fg='#7f8c8d')
        self.report_update_file_label.pack(side=tk.LEFT, padx=5)
        
        def submit_update():
            update_data = update_text.get("1.0", tk.END).strip()
            
            if not update_data and not self.report_update_files:
                messagebox.showwarning("Warning", "Please provide update information or upload files")
                return
            
            if self.auth.update_report(report_id, update_data, self.report_update_files):
                messagebox.showinfo("Success", "Report updated successfully")
                update_window.destroy()
                self.load_reports_data()
            else:
                messagebox.showerror("Error", "Failed to update report")
        
        # Buttons
        button_frame = tk.Frame(update_window, bg='#ecf0f1')
        button_frame.pack(fill=tk.X, pady=10)
        
        submit_btn = tk.Button(button_frame, text="Submit Update", font=('Arial', 12, 'bold'),
                              bg='#27ae60', fg='white', padx=20, pady=10, command=submit_update)
        submit_btn.pack(side=tk.LEFT, padx=20)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", font=('Arial', 12),
                              bg='#95a5a6', fg='white', padx=20, pady=10, command=update_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=20)
    
    def upload_report_update_file(self):
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("All files", "*.*"), 
                      ("Image files", "*.jpg *.jpeg *.png"),
                      ("PDF files", "*.pdf"),
                      ("Document files", "*.doc *.docx *.txt")]
        )
        if file_path:
            self.report_update_files.append(file_path)
            self.report_update_file_label.config(text=f"{len(self.report_update_files)} file(s) uploaded")
    
    def close_report(self):
        selection = self.reports_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report to close")
            return
        
        item = self.reports_tree.item(selection[0])
        report_id = item['values'][0]
        title = item['values'][1]
        current_status = item['values'][3]
        
        if current_status == 'Closed':
            messagebox.showinfo("Already Closed", "This report is already closed.")
            return
        
        confirm = messagebox.askyesno("Confirm Close", 
                                     f"Are you sure you want to close the report '{title}'?\n\n"
                                     f"This action cannot be undone.")
        
        if confirm:
            if self.auth.close_report(report_id):
                messagebox.showinfo("Success", "Report closed successfully")
                self.load_reports_data()
            else:
                messagebox.showerror("Error", "Failed to close report")
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            # Restart the application
            import main
            main.start_application()