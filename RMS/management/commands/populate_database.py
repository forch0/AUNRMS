from faker import Faker
import random
import uuid
from django.utils import timezone
from UserProfiles.models import (UserCred, Residents, Roles, Staffs)
from AcademicYear.models import (AcademicSession, Semester, Enrollment, StaffAssignment)
from Dorms.models import (Dorm, Room, Storage, StorageItem,)
from Actions.models import (MaintenanceRequest, Announcement, Complaint, Category, SubCategory)


fake = Faker()

def create_academic_sessions():
    for _ in range(3):
        AcademicSession.objects.create(
            start_year=fake.year(),
            end_year=fake.year() + 1
        )

def create_semesters():
    academic_sessions = AcademicSession.objects.all()
    for session in academic_sessions:
        for semester_type in ['Fall', 'Spring', 'Summer']:
            Semester.objects.create(
                semester_type=semester_type,
                start_date=fake.date_this_year(),
                end_date=fake.date_this_year(),
                academic_session=session
            )

def create_roles():
    roles = ['Residence Assistant', 'Residence Director', 'ResLife Director', 'Dean of Students Affairs']
    for role in roles:
        Roles.objects.create(name=role)

def create_categories():
    categories = ['Plumbing', 'Electrical', 'Cleaning', 'Furniture']
    for category in categories:
        Category.objects.create(name=category)

def create_subcategories():
    categories = Category.objects.all()
    subcategories = {
        'Plumbing': ['Leaky Faucet', 'Clogged Drain', 'Broken Pipe'],
        'Electrical': ['Power Outage', 'Broken Outlet', 'Faulty Wiring'],
        'Cleaning': ['Vacuuming', 'Dusting', 'Trash Removal'],
        'Furniture': ['Broken Chair', 'Wobbly Table', 'Broken Bed']
    }
    for category_name, subs in subcategories.items():
        category = categories.get(name=category_name)
        for sub in subs:
            SubCategory.objects.create(name=sub, category=category)

def create_staffs_and_users():
    roles = Roles.objects.all()
    for _ in range(10):
        user = UserCred.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password()
        )
        role = random.choice(roles)
        Staffs.objects.create(
            user=user,
            role=role
        )

def create_residents_and_users():
    rooms = Room.objects.all()
    for _ in range(10):
        user = UserCred.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password()
        )
        room = random.choice(rooms)
        Residents.objects.create(
            user=user,
            room=room,
            guardianPhoneNumber=fake.phone_number()
        )

def create_dorms():
    for _ in range(5):
        Dorm.objects.create(
            name=fake.word(),
            address=fake.address(),
            gender=random.choice(['M', 'F', 'C']),
            campus_status=random.choice(['ON', 'OFF'])
        )

def create_rooms():
    dorms = Dorm.objects.all()
    for dorm in dorms:
        for _ in range(3):
            Room.objects.create(
                number=fake.word(),
                capacity=random.randint(1, 4),
                room_plan=random.choice(['3_in_1_wof', '2_in_1_wof', '3_in_1_wf', '2_in_1_wf']),
                floor=random.randint(1, 4),
                dorm=dorm
            )

def create_storage():
    dorms = Dorm.objects.all()
    for dorm in dorms:
        for _ in range(2):
            Storage.objects.create(
                description=fake.text(),
                capacity=random.randint(10, 100),
                floor=random.randint(1, 4),
                dorm=dorm
            )

def create_maintenance_requests():
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    residents = Residents.objects.all()
    semesters = Semester.objects.all()
    academic_sessions = AcademicSession.objects.all()
    dorms = Dorm.objects.all()

    for _ in range(10):
        MaintenanceRequest.objects.create(
            dorm=random.choice(dorms),
            room=random.choice(Room.objects.all()),
            resident=random.choice(residents),
            semester=random.choice(semesters),
            academic_session=random.choice(academic_sessions),
            category=random.choice(categories),
            sub_category=random.choice(subcategories),
            description=fake.text(),
            status=random.choice(['P', 'IP', 'C']),
            updated_by=random.choice(Staffs.objects.all()) if random.choice([True, False]) else None
        )

def create_announcements():
    staff = Staffs.objects.all()
    semesters = Semester.objects.all()
    academic_sessions = AcademicSession.objects.all()
    dorms = Dorm.objects.all()

    for _ in range(5):
        Announcement.objects.create(
            title=fake.sentence(),
            message=fake.text(),
            created_by=random.choice(staff),
            is_global=random.choice([True, False]),
            semester=random.choice(semesters),
            academic_session=random.choice(academic_sessions),
            dorms=random.sample(list(dorms), k=random.randint(1, 3)) if random.choice([True, False]) else []
        )

def create_complaints():
    residents = Residents.objects.all()
    semesters = Semester.objects.all()
    academic_sessions = AcademicSession.objects.all()
    enrollments = Enrollment.objects.all()

    for _ in range(5):
        Complaint.objects.create(
            user=random.choice(residents).user if random.choice([True, False]) else None,
            enrollment=random.choice(enrollments),
            semester=random.choice(semesters),
            academic_session=random.choice(academic_sessions),
            description=fake.text(),
            is_anonymous=random.choice([True, False])
        )

def create_storage_items():
    storages = Storage.objects.all()
    residents = Residents.objects.all()
    semesters = Semester.objects.all()
    academic_sessions = AcademicSession.objects.all()

    for _ in range(10):
        StorageItem.objects.create(
            description=fake.text(),
            quantity=random.randint(1, 10),
            storage=random.choice(storages),
            room=random.choice(Room.objects.all()),
            resident=random.choice(residents),
            semester=random.choice(semesters),
            academic_session=random.choice(academic_sessions),
            status=random.choice(['P', 'A', 'R']),
            approved_by=random.choice(Staffs.objects.all()) if random.choice([True, False]) else None,
            collected_by=random.choice(residents) if random.choice([True, False]) else None
        )

# Call the functions to populate the database
create_academic_sessions()
create_semesters()
create_roles()
create_categories()
create_subcategories()
create_staffs_and_users()
create_residents_and_users()
create_dorms()
create_rooms()
create_storage()
create_maintenance_requests()
create_announcements()
create_complaints()
create_storage_items()
