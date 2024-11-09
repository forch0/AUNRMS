# userprofiles/analytics.py

import plotly.express as px
import uuid
import pandas as pd
from Dorms.models import Dorm, Room
from Actions.models import *
from AcademicYear.models import * 
from django.db.models import Count
from .models import Residents, Roles



def total_enrollment_by_dorm():
    dorms = Dorm.objects.all()
    data = []
    for dorm in dorms:
        # Count residents enrolled in the dorm via the Enrollment model
        enrolled_residents = Enrollment.objects.filter(dorm=dorm).count()  # Use Enrollment to count residents
        data.append({'dorm': dorm.name, 'enrollment': enrolled_residents})
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Generate the bar chart
    fig = px.bar(df, x='dorm', y='enrollment', title="Total Enrollment by Dorm")
    
    return fig

def enrollment_trends():
    # Get all academic sessions
    sessions = AcademicSession.objects.all()
    
    data = []
    
    # Loop through each session to count the active enrollments
    for session in sessions:
        # Count the number of active enrollments for the current session
        active_enrollments = Enrollment.objects.filter(
            academic_session=session, 
            status='active'
        ).count()
        
        data.append({'session': session.name, 'enrollment': active_enrollments})
    
    # Convert data to a DataFrame for Plotly visualization
    df = pd.DataFrame(data)
    
    # Generate a line plot using Plotly
    fig = px.line(df, x='session', y='enrollment', title="Enrollment Trends")
    
    return fig

def resident_room_occupancy():
    # Fetch all rooms
    rooms = Room.objects.all()
    data = []

    # Loop through each room and get the number of residents
    for room in rooms:
        # Count residents in the room via the Enrollment model
        residents_count = Enrollment.objects.filter(room=room, status='active').count()

        # Append data
        data.append({
            'room_name': room.room_name,  # Assuming 'room_name' is a method that gives room name
            'resident_count': residents_count
        })

    # Convert data to DataFrame for visualization
    df = pd.DataFrame(data)
    fig = px.bar(df, x='room_name', y='resident_count', title="Resident Room Occupancy")
    return fig


def maintenance_requests_by_category():
    # Fetch all categories, including those without any maintenance requests
    categories = Category.objects.all()

    # Fetch maintenance requests, counting the number of requests per category
    maintenance_requests = MaintenanceRequest.objects.values('category__name') \
        .annotate(count=Count('category')) \
        .order_by('category__name')

    # Create a DataFrame for maintenance requests count
    df_requests = pd.DataFrame(list(maintenance_requests))

    # Get all categories' names (to ensure we include even those with zero requests)
    category_names = [cat.name for cat in categories]

    # Create a DataFrame for all categories (ensure no category is excluded)
    df_categories = pd.DataFrame(category_names, columns=['Category'])

    # Merge the categories and the maintenance request data, ensuring no category is missing
    df = pd.merge(df_categories, df_requests, how='left', left_on='Category', right_on='category__name')

    # Fill NaN values (categories with no requests) with 0
    df['count'].fillna(0, inplace=True)

    # Convert the 'Category' field to string (for any UUID or non-string fields)
    df['Category'] = df['Category'].astype(str)

    # Rename the columns for readability
    df.rename(columns={'Category': 'Category', 'count': 'Number of Requests'}, inplace=True)

    # Create the bar chart (maintenance requests by category)
    fig = px.bar(df, x='Category', y='Number of Requests', title="Maintenance Requests by Category",
                 labels={'Category': 'Category', 'Number of Requests': 'Number of Requests'})

    return fig


def request_completion_rate_per_dorm():
    data = []
    
    # Retrieve all dorms
    dorms = Dorm.objects.all()

    # Loop through all dorms to ensure each dorm is represented
    for dorm in dorms:
        # Retrieve maintenance requests for this dorm
        requests = MaintenanceRequest.objects.filter(room__dorm=dorm)

        if requests.exists():
            # Calculate the completion time for each request
            for req in requests:
                if req.completion_date and req.created_at:
                    completion_time = (req.completion_date - req.created_at).days
                    data.append({'dorm_name': dorm.name, 'completion_time': completion_time})
        else:
            # If no requests exist for the dorm, add a 0 value for completion time
            data.append({'dorm_name': dorm.name, 'completion_time': 0})
    
    # If no data is available, return an empty chart with a message
    if not data:
        return px.bar(x=[], y=[], title="No Completion Data Available")

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    # Calculate the average completion time per dorm (even if it's 0)
    avg_completion_per_dorm = df.groupby('dorm_name')['completion_time'].mean().reset_index()

    # Generate the bar chart for average completion time per dorm
    fig = px.bar(avg_completion_per_dorm, x='dorm_name', y='completion_time', 
                 title="Average Request Completion Time Per Dorm",
                 labels={'dorm_name': 'Dorm', 'completion_time': 'Average Completion Time (days)'})

    return fig


def complaint_status_analysis():
    # Get all complaint types from the COMPLAINT_TYPE_CHOICES directly
    complaint_types = Complaint.COMPLAINT_TYPE_CHOICES
    
    data = []
    
    # Loop through each complaint type and aggregate status counts
    for ctype in complaint_types:
        # Get complaints for each type
        complaints_in_type = Complaint.objects.filter(complaint_type=ctype[0])
        
        if not complaints_in_type.exists():
            # Skip if there are no complaints of this type
            continue
        
        # Get the count of complaints for each status within the complaint type
        status_counts = complaints_in_type.values('status').annotate(count=Count('status'))
        
        # Append data with complaint_type, status, and count
        for status in status_counts:
            data.append({
                'complaint_type': ctype[1],  # Use the label (e.g., 'Wi-Fi') for the complaint type
                'status': status['status'], 
                'count': status['count']
            })
    
    if not data:
        # Return an empty figure if there is no data
        return px.bar(title="No complaints data to display")
    
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(data)

    # Debugging step: Print the columns and the first few rows to ensure the structure is correct
    print(df.columns)  # Check the DataFrame columns
    print(df.head())   # Print the first few rows of the DataFrame
    
    # Create a bar chart using Plotly
    fig = px.bar(df, x='complaint_type', y='count', color='status', title="Complaints by Type and Status")
    
    # Debugging step: Check if the figure has been generated correctly
    print(fig)
    
    return fig

def anonymous_vs_non_anonymous_complaints():
    anonymous_complaints = Complaint.objects.filter(is_anonymous=True).count()
    non_anonymous_complaints = Complaint.objects.filter(is_anonymous=False).count()
    
    df = pd.DataFrame({
        'type': ['Anonymous', 'Non-Anonymous'],
        'count': [anonymous_complaints, non_anonymous_complaints]
    })
    fig = px.pie(df, names='type', values='count', title="Anonymous vs Non-Anonymous Complaints")
    return fig

def complaint_trends():
    sessions = AcademicSession.objects.all()  # Ensure this model is imported
    data = []
    for session in sessions:
        complaints_in_session = Complaint.objects.filter(academic_session=session).count()
        data.append({'session': session.name, 'complaints': complaints_in_session})
    
    df = pd.DataFrame(data)
    fig = px.line(df, x='session', y='complaints', title="Complaint Trends")
    return fig

def staff_assignment_by_role():
    # Retrieve all roles
    roles = Roles.objects.all()
    data = []
    
    # Loop through each role and count staff assignments for each dorm
    for role in roles:
        # For each role, get the staff assignments and their related dorms
        staff_assigned = StaffAssignment.objects.filter(role=role).values('dorm').annotate(staff_count=Count('dorm'))
        
        # Loop through the result to add the role, dorm, and staff count
        for assignment in staff_assigned:
            dorm_name = Dorm.objects.get(id=assignment['dorm']).name  # Get the dorm name from its ID
            data.append({
                'role': role.name,
                'dorm': dorm_name,
                'staff_assigned': assignment['staff_count']
            })
    
    # If no data is collected, return an empty figure
    if not data:
        return px.bar(title="No staff assignments to display")

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(data)

    # Create a bar chart using Plotly, grouped by role and dorm
    fig = px.bar(df, x='role', y='staff_assigned', color='dorm', title="Staff Assignment by Role and Dorm")

    # Return the generated figure
    return fig

def semester_based_dorm_usage():
    semesters = Semester.objects.all()  # Get all semesters
    data = []
    
    for semester in semesters:
        # Get the count of residents for each semester through the Enrollment model
        dorm_usage = Enrollment.objects.filter(semester=semester).count()
        
        # Create a more informative name for the semester using semester_type and start_date
        semester_name = f"{semester.get_semester_type_display()} {semester.start_date.year}"
        
        data.append({'semester': semester_name, 'dorm_usage': dorm_usage})
    
    df = pd.DataFrame(data)
    fig = px.line(df, x='semester', y='dorm_usage', title="Semester-based Dorm and Room Usage")
    return fig

def vendors_per_dorm():
    # Get all dorms and annotate the count of vendors, including those with zero vendors
    dorms_data = Dorm.objects.annotate(vendor_count=Count('vendors')).order_by('name')

    # Prepare the data for display
    data = []
    for dorm in dorms_data:
        data.append({
            'dorm': dorm.name,  # Dorm name
            'vendor_count': dorm.vendor_count  # Number of vendors in the dorm (including zero)
        })
    
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Create a bar chart using Plotly
    fig = px.bar(df, x='dorm', y='vendor_count', title="Vendors Per Dorm", labels={'vendor_count': 'Number of Vendors'})
    
    return fig