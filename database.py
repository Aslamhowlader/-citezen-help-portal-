import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""  # Set your MySQL password here
        self.database = "smart_citizen_portal"
        self.connection = None
        self.create_database()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.connection
        except Error as e:
            print(f"Database connection error: {e}")
            return None
    
    def create_database(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")
            
            # Enhanced Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(100),
                    full_name VARCHAR(100),
                    phone VARCHAR(20),
                    nid_number VARCHAR(50),
                    date_of_birth DATE,
                    address TEXT,
                    role ENUM('citizen', 'officer', 'admin') DEFAULT 'citizen',
                    department VARCHAR(100),
                    status ENUM('active', 'suspended') DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP NULL
                )
            ''')
            
            # Services table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS services (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    category VARCHAR(50),
                    requirements TEXT,
                    processing_time VARCHAR(50),
                    fee DECIMAL(10,2) DEFAULT 0,
                    status ENUM('active', 'inactive') DEFAULT 'active',
                    created_by INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
                )
            ''')
            
            # Applications table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    service_id INT,
                    application_data TEXT,
                    status ENUM('pending', 'under_review', 'approved', 'rejected', 'cancelled') DEFAULT 'pending',
                    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    assigned_officer_id INT,
                    notes TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE,
                    FOREIGN KEY (assigned_officer_id) REFERENCES users(id) ON DELETE SET NULL
                )
            ''')
            
            # Reports table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reports (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    category VARCHAR(100),
                    location TEXT,
                    image_path VARCHAR(500),
                    status ENUM('submitted', 'under_review', 'resolved', 'rejected', 'closed') DEFAULT 'submitted',
                    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
                    submitted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    assigned_officer_id INT,
                    resolution_notes TEXT,
                    resolved_date TIMESTAMP NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (assigned_officer_id) REFERENCES users(id) ON DELETE SET NULL
                )
            ''')
            
            # Notifications table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    title VARCHAR(255) NOT NULL,
                    message TEXT,
                    type ENUM('info', 'success', 'warning', 'error') DEFAULT 'info',
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # Departments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS departments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    contact_email VARCHAR(100),
                    contact_phone VARCHAR(20),
                    status ENUM('active', 'inactive') DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Service categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS service_categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    icon VARCHAR(50),
                    status ENUM('active', 'inactive') DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insert default data
            self.insert_default_data(cursor)
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Error as e:
            print(f"Database creation error: {e}")
    
    def insert_default_data(self, cursor):
        # Insert default users
        cursor.execute('''
            INSERT IGNORE INTO users (username, password, full_name, email, role, department) 
            VALUES 
            ('admin', %s, 'System Administrator', 'admin@system.com', 'admin', 'Administration'),
            ('officer1', %s, 'John Officer', 'officer1@system.com', 'officer', 'Public Services'),
            ('officer2', %s, 'Sarah Officer', 'officer2@system.com', 'officer', 'Health Department'),
            ('citizen1', %s, 'Regular Citizen', 'citizen1@system.com', 'citizen', NULL)
        ''', (self.hash_password('admin123'), self.hash_password('officer123'), 
              self.hash_password('officer123'), self.hash_password('citizen123')))
        
        # Insert sample services
        cursor.execute('''
            INSERT IGNORE INTO services (name, description, category, requirements, processing_time, fee, status, created_by)
            VALUES 
            ('Birth Certificate', 'Apply for a new birth certificate or duplicate', 'Civil Registration', 'Proof of birth, Parent IDs, Application form', '5-7 working days', 10.0, 'active', 1),
            ('Passport Application', 'Apply for a new passport or renewal', 'Immigration', 'Current passport, Photo, Application form, NID', '15-20 working days', 50.0, 'active', 1),
            ('Driver License', 'Apply for a new driver license or renewal', 'Transport', 'Medical certificate, NID, Photo, Application form', '10-12 working days', 25.0, 'active', 1),
            ('Business Registration', 'Register a new business or company', 'Commerce', 'Business plan, NID, Proof of address, Tax certificate', '20-25 working days', 100.0, 'active', 1),
            ('Building Permit', 'Apply for construction or renovation permit', 'Construction', 'Land title, Building plans, NID, Location map', '30-35 working days', 200.0, 'active', 1),
            ('Marriage Certificate', 'Apply for marriage registration certificate', 'Civil Registration', 'Marriage registration form, NIDs of both spouses, Witness details', '7-10 working days', 15.0, 'active', 1),
            ('Death Certificate', 'Apply for death registration certificate', 'Civil Registration', 'Death declaration, Hospital certificate, Applicant NID', '3-5 working days', 5.0, 'active', 1),
            ('Trade License', 'Apply for business trade license', 'Commerce', 'Business registration, NID, Location proof, Tax certificate', '15-18 working days', 75.0, 'active', 1),
            ('Water Connection', 'Apply for new water supply connection', 'Utility Services', 'NID, Property documents, Location details', '10-15 working days', 50.0, 'active', 1),
            ('Electricity Connection', 'Apply for new electricity connection', 'Utility Services', 'NID, Property documents, Location details', '12-18 working days', 80.0, 'active', 1)
        ''')
        
        # Insert departments
        cursor.execute('''
            INSERT IGNORE INTO departments (name, description, contact_email, contact_phone)
            VALUES 
            ('Public Services', 'Handles all public service applications', 'public@government.gov', '+880-2-XXXXXXX'),
            ('Health Department', 'Manages health-related services and certificates', 'health@government.gov', '+880-2-XXXXXXX'),
            ('Transport Authority', 'Handles driver licenses and vehicle registration', 'transport@government.gov', '+880-2-XXXXXXX'),
            ('Commerce Department', 'Manages business registration and trade licenses', 'commerce@government.gov', '+880-2-XXXXXXX'),
            ('Utility Services', 'Handles water, electricity, and other utility connections', 'utilities@government.gov', '+880-2-XXXXXXX'),
            ('Civil Registration', 'Manages birth, marriage, and death certificates', 'civil@government.gov', '+880-2-XXXXXXX')
        ''')
        
        # Insert service categories
        cursor.execute('''
            INSERT IGNORE INTO service_categories (name, description, icon)
            VALUES 
            ('Civil Registration', 'Birth, marriage, death certificates and other civil documents', '📝'),
            ('Immigration', 'Passport, visa, and immigration services', '🛂'),
            ('Transport', 'Driver licenses, vehicle registration, and transport permits', '🚗'),
            ('Commerce', 'Business registration, trade licenses, and commercial permits', '💼'),
            ('Construction', 'Building permits, construction approvals, and land development', '🏗️'),
            ('Utility Services', 'Water, electricity, gas, and other utility connections', '⚡'),
            ('Education', 'Educational certificates, scholarships, and academic services', '🎓'),
            ('Healthcare', 'Health certificates, medical services, and healthcare programs', '🏥')
        ''')
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    # User Management Methods
    def register_user(self, user_data):
        conn = self.connect()
        if not conn:
            return False, "Database connection failed"
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            role_mapping = {
                "Citizen": "citizen",
                "Government Officer": "officer", 
                "Administrator": "admin"
            }
            
            db_role = role_mapping.get(user_data['role'], 'citizen')
            
            cursor.execute('''
                INSERT INTO users (username, password, email, full_name, phone, nid_number, 
                                date_of_birth, address, role, department)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                user_data['username'],
                self.hash_password(user_data['password']),
                user_data.get('email'),
                user_data['full_name'],
                user_data.get('phone'),
                user_data.get('nid'),
                user_data.get('date_of_birth'),
                user_data.get('address'),
                db_role,
                user_data.get('department')
            ))
            
            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()
            conn.close()
            
            return True, f"User registered successfully with ID: {user_id}"
            
        except Error as e:
            print(f"Registration error: {e}")
            return False, f"Registration failed: {str(e)}"
    
    def login_user(self, username, password):
        conn = self.connect()
        if not conn:
            return False, "Database connection failed"
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT id, username, password, full_name, email, role, status, department 
                FROM users WHERE username = %s
            ''', (username,))
            
            user = cursor.fetchone()
            
            if user:
                # Update last login
                cursor.execute('''
                    UPDATE users SET last_login = %s WHERE id = %s
                ''', (datetime.now(), user['id']))
                conn.commit()
            
            cursor.close()
            conn.close()
            
            if not user:
                return False, "Invalid username or password"
            
            if user['status'] != 'active':
                return False, "Account is suspended. Please contact administrator."
            
            if user['password'] != self.hash_password(password):
                return False, "Invalid username or password"
            
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'name': user['full_name'],
                'email': user['email'],
                'role': user['role'],
                'department': user['department']
            }
            
            return True, user_data
            
        except Error as e:
            print(f"Login error: {e}")
            return False, f"Login failed: {str(e)}"
    
    def get_user_profile(self, user_id):
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT id, username, email, full_name, phone, nid_number, 
                       date_of_birth, address, role, department, created_at, last_login
                FROM users WHERE id = %s
            ''', (user_id,))
            
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return user
            
        except Error as e:
            print(f"Get profile error: {e}")
            return None
    
    def update_user_profile(self, user_id, updated_data):
        """Update user profile information"""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET full_name = %s, email = %s, phone = %s, nid_number = %s, 
                    date_of_birth = %s, address = %s
                WHERE id = %s
            ''', (
                updated_data.get('full_name'),
                updated_data.get('email'),
                updated_data.get('phone'),
                updated_data.get('nid_number'),
                updated_data.get('date_of_birth'),
                updated_data.get('address'),
                user_id
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Error as e:
            print(f"Update user profile error: {e}")
            return False

    def check_username_availability(self, username):
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return result is None
            
        except Error as e:
            print(f"Check username error: {e}")
            return False
    
    def check_nid_availability(self, nid):
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE nid_number = %s", (nid,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return result is None
            
        except Error as e:
            print(f"Check NID error: {e}")
            return False
    
    # Services Management
    def get_all_services(self):
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT s.*, u.username as created_by_name 
                FROM services s 
                LEFT JOIN users u ON s.created_by = u.id 
                WHERE s.status = 'active'
                ORDER BY s.name ASC
            ''')
            
            services = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return services
            
        except Error as e:
            print(f"Get services error: {e}")
            return []

    def search_services(self, query):
        """Search services by name, description, or category"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT s.*, u.username as created_by_name 
                FROM services s 
                LEFT JOIN users u ON s.created_by = u.id 
                WHERE s.status = 'active' AND 
                      (s.name LIKE %s OR s.description LIKE %s OR s.category LIKE %s)
                ORDER BY s.name ASC
            ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
            
            services = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return services
            
        except Error as e:
            print(f"Search services error: {e}")
            return []

    def get_service_by_id(self, service_id):
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT s.*, u.username as created_by_name 
                FROM services s 
                LEFT JOIN users u ON s.created_by = u.id 
                WHERE s.id = %s
            ''', (service_id,))
            
            service = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return service
            
        except Error as e:
            print(f"Get service by ID error: {e}")
            return None

    def create_service(self, service_data):
        conn = self.connect()
        if not conn:
            return False, "Database connection failed"
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO services (name, description, category, requirements, processing_time, fee, status, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                service_data['service_name'],
                service_data.get('description', ''),
                service_data.get('category', 'General'),
                service_data.get('requirements', ''),
                service_data.get('processing_time', ''),
                service_data.get('fee', 0),
                'active',
                service_data.get('created_by', 1)
            ))
            
            conn.commit()
            service_id = cursor.lastrowid
            cursor.close()
            conn.close()
            
            return True, service_id
            
        except Error as e:
            print(f"Add service error: {e}")
            return False, f"Failed to add service: {str(e)}"
    
    def update_service(self, service_id, service_data):
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE services 
                SET name = %s, description = %s, category = %s, requirements = %s, 
                    processing_time = %s, fee = %s, status = %s 
                WHERE id = %s
            ''', (
                service_data['name'],
                service_data['description'],
                service_data['category'],
                service_data.get('requirements', ''),
                service_data.get('processing_time', ''),
                service_data.get('fee', 0),
                service_data.get('status', 'active'),
                service_id
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Error as e:
            print(f"Update service error: {e}")
            return False
    
    def delete_service(self, service_id):
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM services WHERE id = %s', (service_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Error as e:
            print(f"Delete service error: {e}")
            return False

    # Applications Management
    def create_application(self, user_id, service_id, details, uploaded_files=None):
        """Create a new service application"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO applications (user_id, service_id, application_data, status)
                VALUES (%s, %s, %s, 'pending')
            ''', (user_id, service_id, details))
            
            conn.commit()
            application_id = cursor.lastrowid
            cursor.close()
            conn.close()
            
            return application_id
            
        except Error as e:
            print(f"Create application error: {e}")
            return None

    def get_user_applications(self, user_id):
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT a.*, s.name as service_name, s.category as service_category,
                       s.processing_time, s.fee,
                       o.username as officer_name, o.full_name as officer_full_name
                FROM applications a 
                JOIN services s ON a.service_id = s.id 
                LEFT JOIN users o ON a.assigned_officer_id = o.id 
                WHERE a.user_id = %s 
                ORDER BY a.applied_date DESC
            ''', (user_id,))
            
            applications = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return applications
            
        except Error as e:
            print(f"Get user applications error: {e}")
            return []

    def search_applications(self, user_id, query):
        """Search applications by service name or status for a specific user"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT a.*, s.name as service_name, s.category as service_category,
                       o.username as officer_name, o.full_name as officer_full_name
                FROM applications a 
                JOIN services s ON a.service_id = s.id 
                LEFT JOIN users o ON a.assigned_officer_id = o.id 
                WHERE a.user_id = %s AND 
                      (s.name LIKE %s OR a.status LIKE %s OR a.application_data LIKE %s)
                ORDER BY a.applied_date DESC
            ''', (user_id, f'%{query}%', f'%{query}%', f'%{query}%'))
            
            applications = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return applications
            
        except Error as e:
            print(f"Search applications error: {e}")
            return []

    def get_applications_by_status(self, user_id, status):
        """Get applications filtered by status for a specific user"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT a.*, s.name as service_name, s.category as service_category,
                       o.username as officer_name, o.full_name as officer_full_name
                FROM applications a 
                JOIN services s ON a.service_id = s.id 
                LEFT JOIN users o ON a.assigned_officer_id = o.id 
                WHERE a.user_id = %s AND a.status = %s
                ORDER BY a.applied_date DESC
            ''', (user_id, status))
            
            applications = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return applications
            
        except Error as e:
            print(f"Get applications by status error: {e}")
            return []

    def get_application_details(self, application_id):
        """Get detailed information about a specific application"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT a.*, s.name as service_name, s.description as service_description,
                       s.category as service_category, s.processing_time, s.fee, s.requirements,
                       u.username as user_name, u.full_name as user_full_name, u.email as user_email,
                       u.phone as user_phone, u.nid_number as user_nid,
                       o.username as officer_name, o.full_name as officer_full_name
                FROM applications a 
                JOIN services s ON a.service_id = s.id 
                JOIN users u ON a.user_id = u.id 
                LEFT JOIN users o ON a.assigned_officer_id = o.id 
                WHERE a.id = %s
            ''', (application_id,))
            
            application = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return application
            
        except Error as e:
            print(f"Get application details error: {e}")
            return None

    def cancel_application(self, application_id):
        """Cancel an application"""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE applications 
                SET status = 'cancelled', notes = 'Cancelled by user'
                WHERE id = %s
            ''', (application_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Error as e:
            print(f"Cancel application error: {e}")
            return False

    def update_application(self, application_id, update_data, uploaded_files=None):
        """Update an application with additional information"""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Get current application data
            cursor.execute('SELECT application_data FROM applications WHERE id = %s', (application_id,))
            current_data = cursor.fetchone()
            
            if current_data:
                current_data = current_data[0] or ""
                new_data = current_data + "\n\n--- Update ---\n" + update_data
            else:
                new_data = update_data
            
            cursor.execute('''
                UPDATE applications 
                SET application_data = %s, status = 'under_review'
                WHERE id = %s
            ''', (new_data, application_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Error as e:
            print(f"Update application error: {e}")
            return False

    # Reports Management
    def create_report(self, user_id, title, category, priority, description, location=None, image_path=None):
        """Create a new report/complaint"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reports (user_id, title, description, category, priority, location, image_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (user_id, title, description, category, priority, location, image_path))
            
            conn.commit()
            report_id = cursor.lastrowid
            cursor.close()
            conn.close()
            
            return report_id
            
        except Error as e:
            print(f"Create report error: {e}")
            return None

    def get_user_reports(self, user_id):
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT r.*, o.username as officer_name, o.full_name as officer_full_name
                FROM reports r 
                LEFT JOIN users o ON r.assigned_officer_id = o.id 
                WHERE r.user_id = %s 
                ORDER BY r.submitted_date DESC
            ''', (user_id,))
            
            reports = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return reports
            
        except Error as e:
            print(f"Get user reports error: {e}")
            return []

    def search_reports(self, user_id, query):
        """Search reports by title, category, or description for a specific user"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT r.*, o.username as officer_name, o.full_name as officer_full_name
                FROM reports r 
                LEFT JOIN users o ON r.assigned_officer_id = o.id 
                WHERE r.user_id = %s AND 
                      (r.title LIKE %s OR r.category LIKE %s OR r.description LIKE %s)
                ORDER BY r.submitted_date DESC
            ''', (user_id, f'%{query}%', f'%{query}%', f'%{query}%'))
            
            reports = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return reports
            
        except Error as e:
            print(f"Search reports error: {e}")
            return []

    def get_reports_by_status(self, user_id, status):
        """Get reports filtered by status for a specific user"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT r.*, o.username as officer_name, o.full_name as officer_full_name
                FROM reports r 
                LEFT JOIN users o ON r.assigned_officer_id = o.id 
                WHERE r.user_id = %s AND r.status = %s
                ORDER BY r.submitted_date DESC
            ''', (user_id, status))
            
            reports = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return reports
            
        except Error as e:
            print(f"Get reports by status error: {e}")
            return []

    def get_report_details(self, report_id):
        """Get detailed information about a specific report"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT r.*, u.username as user_name, u.full_name as user_full_name,
                       u.email as user_email, u.phone as user_phone,
                       o.username as officer_name, o.full_name as officer_full_name
                FROM reports r 
                JOIN users u ON r.user_id = u.id 
                LEFT JOIN users o ON r.assigned_officer_id = o.id 
                WHERE r.id = %s
            ''', (report_id,))
            
            report = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return report
            
        except Error as e:
            print(f"Get report details error: {e}")
            return None

    def update_report(self, report_id, update_data, uploaded_files=None):
        """Update a report with additional information"""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Get current description
            cursor.execute('SELECT description FROM reports WHERE id = %s', (report_id,))
            current_description = cursor.fetchone()
            
            if current_description:
                current_description = current_description[0] or ""
                new_description = current_description + "\n\n--- Update ---\n" + update_data
            else:
                new_description = update_data
            
            cursor.execute('''
                UPDATE reports 
                SET description = %s, status = 'under_review'
                WHERE id = %s
            ''', (new_description, report_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Error as e:
            print(f"Update report error: {e}")
            return False

    def close_report(self, report_id):
        """Close a report"""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE reports 
                SET status = 'closed', resolved_date = %s
                WHERE id = %s
            ''', (datetime.now(), report_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Error as e:
            print(f"Close report error: {e}")
            return False

    # ADD THIS MISSING METHOD
    def delete_report(self, report_id):
        """Delete a report"""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM reports WHERE id = %s', (report_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Error as e:
            print(f"Delete report error: {e}")
            return False

    # Additional Methods for Dashboard
    def get_user_stats(self, user_id):
        """Get statistics for user dashboard"""
        conn = self.connect()
        if not conn:
            return {}
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Get applications count by status
            cursor.execute('''
                SELECT status, COUNT(*) as count 
                FROM applications 
                WHERE user_id = %s 
                GROUP BY status
            ''', (user_id,))
            application_stats = cursor.fetchall()
            
            # Get reports count by status
            cursor.execute('''
                SELECT status, COUNT(*) as count 
                FROM reports 
                WHERE user_id = %s 
                GROUP BY status
            ''', (user_id,))
            report_stats = cursor.fetchall()
            
            # Get total counts
            cursor.execute('SELECT COUNT(*) as total FROM applications WHERE user_id = %s', (user_id,))
            total_applications = cursor.fetchone()['total']
            
            cursor.execute('SELECT COUNT(*) as total FROM reports WHERE user_id = %s', (user_id,))
            total_reports = cursor.fetchone()['total']
            
            cursor.close()
            conn.close()
            
            return {
                'applications': {
                    'total': total_applications,
                    'by_status': application_stats
                },
                'reports': {
                    'total': total_reports,
                    'by_status': report_stats
                }
            }
            
        except Error as e:
            print(f"Get user stats error: {e}")
            return {}

    def get_service_categories(self):
        """Get all service categories"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT * FROM service_categories 
                WHERE status = 'active'
                ORDER BY name ASC
            ''')
            
            categories = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return categories
            
        except Error as e:
            print(f"Get service categories error: {e}")
            return []

    def get_departments(self):
        """Get all departments"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT * FROM departments 
                WHERE status = 'active'
                ORDER BY name ASC
            ''')
            
            departments = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return departments
            
        except Error as e:
            print(f"Get departments error: {e}")
            return []

    # Admin/Officer Methods
    def get_all_users(self, role_filter=None):
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            if role_filter:
                cursor.execute('''
                    SELECT id, username, email, full_name, phone, role, status, department, created_at, last_login
                    FROM users WHERE role = %s ORDER BY created_at DESC
                ''', (role_filter,))
            else:
                cursor.execute('''
                    SELECT id, username, email, full_name, phone, role, status, department, created_at, last_login
                    FROM users ORDER BY created_at DESC
                ''')
            
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return users
            
        except Error as e:
            print(f"Get users error: {e}")
            return []

    def update_user_status(self, user_id, status):
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET status = %s WHERE id = %s
            ''', (status, user_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Error as e:
            print(f"Update user status error: {e}")
            return False

    def update_user_role(self, user_id, role):
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET role = %s WHERE id = %s
            ''', (role, user_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Error as e:
            print(f"Update user role error: {e}")
            return False

    def delete_user(self, user_id):
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # First delete related records to avoid foreign key constraint issues
            # Delete applications by this user
            cursor.execute('DELETE FROM applications WHERE user_id = %s', (user_id,))
            
            # Delete reports by this user  
            cursor.execute('DELETE FROM reports WHERE user_id = %s', (user_id,))
            
            # Delete notifications for this user
            cursor.execute('DELETE FROM notifications WHERE user_id = %s', (user_id,))
            
            # Now delete the user
            cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Error as e:
            print(f"Delete user error: {e}")
            return False

    def search_users(self, search_term):
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT id, username, email, full_name, phone, role, status, department, created_at
                FROM users 
                WHERE username LIKE %s OR email LIKE %s OR full_name LIKE %s 
                ORDER BY created_at DESC
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return users
            
        except Error as e:
            print(f"Search users error: {e}")
            return []

    def get_all_applications(self, user_role=None, user_id=None):
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            if user_role == 'officer':
                cursor.execute('''
                    SELECT a.*, u.username as user_name, u.full_name as user_full_name,
                           s.name as service_name, o.username as officer_name
                    FROM applications a 
                    JOIN users u ON a.user_id = u.id 
                    JOIN services s ON a.service_id = s.id 
                    LEFT JOIN users o ON a.assigned_officer_id = o.id 
                    WHERE a.assigned_officer_id = %s OR a.assigned_officer_id IS NULL
                    ORDER BY a.applied_date DESC
                ''', (user_id,))
            else:
                cursor.execute('''
                    SELECT a.*, u.username as user_name, u.full_name as user_full_name,
                           s.name as service_name, o.username as officer_name
                    FROM applications a 
                    JOIN users u ON a.user_id = u.id 
                    JOIN services s ON a.service_id = s.id 
                    LEFT JOIN users o ON a.assigned_officer_id = o.id 
                    ORDER BY a.applied_date DESC
                ''')
            
            applications = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return applications
            
        except Error as e:
            print(f"Get applications error: {e}")
            return []

    def get_all_reports(self, user_role=None, user_id=None):
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            if user_role == 'officer':
                cursor.execute('''
                    SELECT r.*, u.username as user_name, u.full_name as user_full_name,
                           o.username as officer_name, o.full_name as officer_full_name
                    FROM reports r 
                    JOIN users u ON r.user_id = u.id 
                    LEFT JOIN users o ON r.assigned_officer_id = o.id 
                    WHERE r.assigned_officer_id = %s OR r.assigned_officer_id IS NULL
                    ORDER BY r.submitted_date DESC
                ''', (user_id,))
            else:
                cursor.execute('''
                    SELECT r.*, u.username as user_name, u.full_name as user_full_name,
                           o.username as officer_name, o.full_name as officer_full_name
                    FROM reports r 
                    JOIN users u ON r.user_id = u.id 
                    LEFT JOIN users o ON r.assigned_officer_id = o.id 
                    ORDER BY r.submitted_date DESC
                ''')
            
            reports = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return reports
            
        except Error as e:
            print(f"Get reports error: {e}")
            return []

    def update_application_status(self, application_id, status, processed_by, notes=None):
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE applications 
                SET status = %s, notes = %s, assigned_officer_id = %s 
                WHERE id = %s
            ''', (status, notes, processed_by, application_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Error as e:
            print(f"Update application error: {e}")
            return False

    def update_report_status(self, report_id, status, assigned_to=None, feedback=None):
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            resolved_date = datetime.now() if status == 'resolved' else None
            
            if assigned_to:
                cursor.execute('''
                    UPDATE reports 
                    SET status = %s, resolution_notes = %s, resolved_date = %s, assigned_officer_id = %s
                    WHERE id = %s
                ''', (status, feedback, resolved_date, assigned_to, report_id))
            else:
                cursor.execute('''
                    UPDATE reports 
                    SET status = %s, resolution_notes = %s, resolved_date = %s 
                    WHERE id = %s
                ''', (status, feedback, resolved_date, report_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Error as e:
            print(f"Update report error: {e}")
            return False

    def get_officers(self):
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT id, username, full_name, department 
                FROM users 
                WHERE role = 'officer' AND status = 'active'
            ''')
            
            officers = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return officers
            
        except Error as e:
            print(f"Get officers error: {e}")
            return []