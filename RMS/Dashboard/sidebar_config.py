# {"label": "Analytics", "icon": "Timeline", "url": "/admin/admin_tools_stats/dashboardstats/"},

def get_sidebar_items_for_role(user):
    """Returns sidebar items based on the user's role."""
    # Common sidebar items for all staff
    sidebar_items = [
        {"label": "Home", "icon": "dashboard", "url": "/admin/"},
        {"label": "Analytics", "icon": "Timeline", "url": "/admin/admin_tools_stats/dashboardstats/"},
        {"label": "Semester", "icon": "book", "url": "/admin/AcademicYear/semester/"},
    ]  

    if user.is_authenticated and user.is_staff and hasattr(user, 'staff'):
        staff_roles = user.staff.roles.values_list('name', flat=True)

        # Add role-specific items without using else
        if "ResLife Directors" in staff_roles:
            sidebar_items.extend([
                {"label": "Academic Session", "icon": "dashboard", "url": "/admin/AcademicYear/academicsession/"},
                {"label": "Dorms", "icon": "House", "url": "/admin/Dorms/dorm/"},
                {"label": "Rooms", "icon": "Bed", "url": "/admin/Dorms/room/"},
                {"label": "Staff Assignment", "icon": "social_distance", "url": "/admin/AcademicYear/staffassignment/"},
                {"label": "Enrollments", "icon": "calendar_today", "url": "/admin/AcademicYear/enrollment/"},
                {"label": "Anouncements", "icon": "Notifications", "url": "/admin/Actions/announcement/"},
                {"label": "Complaints", "icon": "Transcribe", "url": "/admin/Actions/complaint/"},
                {"label": "Maintenance Requests ", "icon": "Report", "url": "/admin/Actions/maintenancerequest/"},
                {"label": "Storage Items", "icon": "apps", "url": "/admin/Dorms/storageitem/"},
                {"label": "Residents ", "icon": "groups_3", "url": "/admin/UserProfiles/residents/"},
                {"label": "Staffs", "icon": "connect_without_contact", "url": "/admin/UserProfiles/staffs/"},
            ])

        elif "Residence Director" in staff_roles:
            sidebar_items.extend([
                {"label": "Academic Session", "icon": "dashboard", "url": "/admin/AcademicYear/academicsession/"},
                {"label": "Dorms", "icon": "House", "url": "/admin/Dorms/dorm/"},
                {"label": "Rooms", "icon": "Bed", "url": "/admin/Dorms/room/"},
                {"label": "Staff Assignment", "icon": "social_distance", "url": "/admin/AcademicYear/staffassignment/"},
                {"label": "Enrollments", "icon": "calendar_today", "url": "/admin/AcademicYear/enrollment/"},
                {"label": "Anouncements", "icon": "Notifications", "url": "/admin/Actions/announcement/"},
                {"label": "Complaints", "icon": "Transcribe", "url": "/admin/Actions/complaint/"},
                {"label": "Maintenance Requests ", "icon": "Report", "url": "/admin/Actions/maintenancerequest/"},
                {"label": "Storage Items", "icon": "apps", "url": "/admin/Dorms/storageitem/"},
                {"label": "Residents ", "icon": "groups_3", "url": "/admin/UserProfiles/residents/"},
                {"label": "Staffs", "icon": "connect_without_contact", "url": "/admin/UserProfiles/staffs/"},
                # Add other role-specific items for Residence Directors here
            ])

        elif "Residence Assistant" in staff_roles:
            sidebar_items.extend([
                {"label": "Dorms", "icon": "House", "url": "/admin/Dorms/dorm/"},
                {"label": "Rooms", "icon": "Bed", "url": "/admin/Dorms/room/"},
                {"label": "Staff Assignment", "icon": "social_distance", "url": "/admin/AcademicYear/staffassignment/"},
                {"label": "Enrollments", "icon": "calendar_today", "url": "/admin/AcademicYear/enrollment/"},
                {"label": "Anouncements", "icon": "Notifications", "url": "/admin/Actions/announcement/"},
                {"label": "Complaints", "icon": "Transcribe", "url": "/admin/Actions/complaint/"},
                {"label": "Maintenance Requests ", "icon": "Report", "url": "/admin/Actions/maintenancerequest/"},
                {"label": "Storage Items", "icon": "apps", "url": "/admin/Dorms/storageitem/"},
                {"label": "Residents ", "icon": "groups_3", "url": "/admin/UserProfiles/residents/"},
                {"label": "Staffs", "icon": "connect_without_contact", "url": "/admin/UserProfiles/staffs/"},

                                # Add other role-specific items for Residence Assistants here
            ])
    
    # Additional sidebar items for all residents (if needed)
    sidebar_items.extend([
        {"label": "Enrollments", "icon": "calendar_today", "url": "/admin/AcademicYear/enrollment/"},
        {"label": "Anouncements", "icon": "Notifications", "url": "/admin/Actions/announcement/"},
        {"label": "Complaints", "icon": "Transcribe", "url": "/admin/Actions/complaint/"},
        {"label": "Maintenance Requests ", "icon": "Report", "url": "/admin/Actions/maintenancerequest/"},
        {"label": "Storage Items", "icon": "apps", "url": "/admin/Dorms/storageitem/"},
    ])

    
    return sidebar_items


