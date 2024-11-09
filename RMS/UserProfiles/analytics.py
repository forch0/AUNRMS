# userprofiles/analytics.py

import plotly.express as px
import pandas as pd
from Dorms.models import Dorm, Room
from Actions.models import MaintenanceRequest, Complaint
from AcademicYear.models import * 
from django.db.models import Count
from .models import  Residents


def total_enrollment_by_dorm():
    dorms = Dorm.objects.all()
    data = []
    for dorm in dorms:
        enrolled_residents = Residents.objects.filter(room__dorm=dorm).count()  # Updated to use Residents
        data.append({'dorm': dorm.name, 'enrollment': enrolled_residents})
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Generate the bar chart
    fig = px.bar(df, x='dorm', y='enrollment', title="Total Enrollment by Dorm")
    
    return fig


def enrollment_trends():
    sessions = AcademicSession.objects.all()  # Make sure this model is imported correctly
    data = []
    for session in sessions:
        enrolled_residents = Resident.objects.filter(academic_session=session).count()
        data.append({'session': session.name, 'enrollment': enrolled_residents})
    
    df = pd.DataFrame(data)
    fig = px.line(df, x='session', y='enrollment', title="Enrollment Trends")
    return fig

def resident_room_occupancy():
    rooms = Room.objects.all()
    data = []
    for room in rooms:
        residents_in_room = room.residents.count()
        occupancy_rate = residents_in_room / room.capacity
        data.append({'room': room.room_name, 'occupancy_rate': occupancy_rate})
    
    df = pd.DataFrame(data)
    fig = px.bar(df, x='room', y='occupancy_rate', title="Resident Room Occupancy")
    return fig

def maintenance_requests_by_category():
    categories = MaintenanceRequest.objects.values('category').distinct()
    data = []
    for category in categories:
        requests_in_category = MaintenanceRequest.objects.filter(category=category['category']).count()
        data.append({'category': category['category'], 'requests': requests_in_category})
    
    df = pd.DataFrame(data)
    fig = px.pie(df, names='category', values='requests', title="Maintenance Requests by Category")
    return fig

def request_completion_rate():
    data = []
    requests = MaintenanceRequest.objects.all()
    for req in requests:
        completion_time = (req.completed_at - req.created_at).days
        data.append({'request_id': req.id, 'completion_time': completion_time})
    
    df = pd.DataFrame(data)
    avg_completion_time = df['completion_time'].mean()
    fig = px.histogram(df, x='completion_time', title=f"Request Completion Rate (Avg: {avg_completion_time:.2f} days)")
    return fig

def complaint_status_analysis():
    complaint_types = Complaint.objects.values('category').distinct()
    data = []
    for ctype in complaint_types:
        complaints_in_type = Complaint.objects.filter(category=ctype['category'])
        status_counts = complaints_in_type.values('status').annotate(count=Count('status'))
        for status in status_counts:
            data.append({'category': ctype['category'], 'status': status['status'], 'count': status['count']})
    
    df = pd.DataFrame(data)
    fig = px.bar(df, x='category', y='count', color='status', title="Complaints by Type and Status")
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
    roles = Role.objects.all()  # Ensure Role is properly imported
    data = []
    for role in roles:
        staff_assigned = StaffAssignment.objects.filter(role=role).count()
        data.append({'role': role.name, 'staff_assigned': staff_assigned})
    
    df = pd.DataFrame(data)
    fig = px.bar(df, x='role', y='staff_assigned', title="Staff Assignment by Role")
    return fig

def semester_based_dorm_usage():
    semesters = Semester.objects.all()  # Ensure Semester model is correctly imported
    data = []
    for semester in semesters:
        dorm_usage = Resident.objects.filter(semester=semester).count()
        data.append({'semester': semester.name, 'dorm_usage': dorm_usage})
    
    df = pd.DataFrame(data)
    fig = px.line(df, x='semester', y='dorm_usage', title="Semester-based Dorm and Room Usage")
    return fig
