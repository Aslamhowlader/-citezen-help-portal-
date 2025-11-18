import tkinter as tk
from admin_officer_dashboard import AdminOfficerDashboard
from user_dashboard import UserDashboard

def start_dashboard(user_data):
    """Start the appropriate dashboard based on user role"""
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    
    if user_data['role'] in ['admin', 'officer']:
        AdminOfficerDashboard(root, user_data)
    else:
        UserDashboard(root, user_data)
    
    root.mainloop()