import re
from database import DatabaseManager

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()

    def validate_email(self, email):
        """Validate email format"""
        if not email:
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        """Validate phone number"""
        if not phone:
            return True
        pattern = r'^01[3-9]\d{8}$'
        return re.match(pattern, phone) is not None

    def validate_nid(self, nid):
        """Validate NID number"""
        if not nid:
            return True
        return nid.isdigit() and 10 <= len(nid) <= 17

    def validate_date(self, date_str):
        """Validate date format YYYY-MM-DD"""
        try:
            year, month, day = map(int, date_str.split('-'))
            if len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
                return False
            if year < 1900 or year > 2023:
                return False
            if month < 1 or month > 12:
                return False
            if day < 1 or day > 31:
                return False
            return True
        except:
            return False

    def register_user(self, user_data):
        """Register a new user with validation"""
        # Required fields validation
        required_fields = [
            ('full_name', 'Full Name'),
            ('phone', 'Phone Number'),
            ('nid', 'NID Number'),
            ('date_of_birth', 'Date of Birth'),
            ('address', 'Address'),
            ('username', 'Username'),
            ('password', 'Password')
        ]
        
        for field, field_name in required_fields:
            if not user_data.get(field):
                return False, f"{field_name} is required"
        
        # Email validation
        if user_data.get('email') and not self.validate_email(user_data['email']):
            return False, "Please enter a valid Gmail address"
        
        # Phone validation
        if not self.validate_phone(user_data['phone']):
            return False, "Please enter a valid Bangladeshi phone number (01XXXXXXXXX)"
        
        # NID validation
        if not self.validate_nid(user_data['nid']):
            return False, "Please enter a valid NID number (10-17 digits)"
        
        # Date validation
        if not self.validate_date(user_data['date_of_birth']):
            return False, "Please enter date in YYYY-MM-DD format (between 1900-2023)"
        
        # Password strength
        if len(user_data['password']) < 6:
            return False, "Password must be at least 6 characters long"
        
        # Database checks
        if not self.db.check_username_availability(user_data['username']):
            return False, "Username already exists"
        
        if not self.db.check_nid_availability(user_data['nid']):
            return False, "NID already registered"
        
        # Register user in database
        return self.db.register_user(user_data)

    def login_user(self, username, password):
        """Authenticate user login"""
        if not username or not password:
            return False, "Please enter both username and password"
        
        return self.db.login_user(username, password)

    def get_user_profile(self, user_id):
        """Get user profile"""
        return self.db.get_user_profile(user_id)

    # Admin methods
    def get_all_users(self, role_filter=None):
        """Get all users (admin only)"""
        return self.db.get_all_users(role_filter)

    def update_user_status(self, user_id, status):
        """Update user status"""
        return self.db.update_user_status(user_id, status)

    def delete_user(self, user_id):
        """Delete a user"""
        return self.db.delete_user(user_id)

    def update_user_role(self, user_id, new_role):
        """Update user role"""
        return self.db.update_user_role(user_id, new_role)

    def get_user_stats(self, user_id):
        """Get user statistics"""
        return self.db.get_user_stats(user_id)

    # Service methods
    def get_all_services(self):
        """Get all services"""
        return self.db.get_all_services()

    def search_services(self, query):
        """Search services"""
        return self.db.search_services(query)

    def get_service_by_id(self, service_id):
        """Get service by ID"""
        return self.db.get_service_by_id(service_id)

    def add_service(self, service_data, created_by):
        """Add a new service - FIXED METHOD"""
        # Extract service data and add created_by
        service_data['created_by'] = created_by
        return self.db.create_service(service_data)

    def update_service(self, service_id, service_data):
        """Update service"""
        return self.db.update_service(service_id, service_data)

    def delete_service(self, service_id):
        """Delete service"""
        return self.db.delete_service(service_id)

    # Application methods - FIXED THESE METHODS
    def create_application(self, user_id, service_id, details, uploaded_files=None):
        """Create a new application - FIXED SIGNATURE"""
        return self.db.create_application(user_id, service_id, details, uploaded_files)

    def get_user_applications(self, user_id):
        """Get user applications"""
        return self.db.get_user_applications(user_id)

    def get_all_applications(self, user_role=None, user_id=None):
        """Get all applications"""
        return self.db.get_all_applications(user_role, user_id)

    def update_application_status(self, application_id, status, notes=None, assigned_officer_id=None):
        """Update application status - FIXED SIGNATURE"""
        return self.db.update_application_status(application_id, status, assigned_officer_id if assigned_officer_id else self.current_user['id'] if hasattr(self, 'current_user') else None, notes)

    def delete_application(self, application_id):
        """Delete application"""
        return self.db.delete_application(application_id)

    def get_application_details(self, application_id):
        """Get application details"""
        return self.db.get_application_details(application_id)

    def cancel_application(self, application_id):
        """Cancel application"""
        return self.db.cancel_application(application_id)

    def update_application(self, application_id, update_data, uploaded_files=None):
        """Update application"""
        return self.db.update_application(application_id, update_data, uploaded_files)

    def search_applications(self, user_id, query):
        """Search applications"""
        return self.db.search_applications(user_id, query)

    def get_applications_by_status(self, user_id, status):
        """Get applications by status"""
        return self.db.get_applications_by_status(user_id, status)

    # Report methods - FIXED THESE METHODS
    def create_report(self, user_id, title, category, priority, description, location=None, image_path=None):
        """Create a new report - FIXED SIGNATURE"""
        return self.db.create_report(user_id, title, category, priority, description, location, image_path)

    def get_user_reports(self, user_id):
        """Get reports for a specific user"""
        return self.db.get_user_reports(user_id)

    def get_all_reports(self, user_role=None, user_id=None):
        """Get all reports"""
        return self.db.get_all_reports(user_role, user_id)

    def update_report_status(self, report_id, status, feedback=None, assigned_to=None):
        """Update report status - FIXED SIGNATURE"""
        return self.db.update_report_status(report_id, status, assigned_to, feedback)

    def delete_report(self, report_id):
        """Delete a report"""
        return self.db.delete_report(report_id)

    def get_report_details(self, report_id):
        """Get specific report by ID"""
        return self.db.get_report_details(report_id)

    def update_report(self, report_id, update_data, uploaded_files=None):
        """Update report"""
        return self.db.update_report(report_id, update_data, uploaded_files)

    def close_report(self, report_id):
        """Close report"""
        return self.db.close_report(report_id)

    def search_reports(self, user_id, query):
        """Search reports"""
        return self.db.search_reports(user_id, query)

    def get_reports_by_status(self, user_id, status):
        """Get reports by status"""
        return self.db.get_reports_by_status(user_id, status)
    def get_applications_by_status(self, user_id, status):
        return self.db.get_applications_by_status(user_id, status)
    
    def assign_report_to_officer(self, report_id, officer_id):
        """Assign report to government officer"""
        return self.db.update_report_status(report_id, 'under_review', officer_id, "Assigned to officer")
    def edit_service(self):
        return self.db.edit_service()
    def get_officers(self):
        """Get all officers"""
        return self.db.get_officers()

    def search_users(self, search_term):
        """Search users"""
        return self.db.search_users(search_term)

    def update_user_profile(self, user_id, updated_data):
        """Update user profile"""
        return self.db.update_user_profile(user_id, updated_data)