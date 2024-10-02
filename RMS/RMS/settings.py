"""
Django settings for RMS project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv
# from UserProfiles.authentication_backends import EmailBackend
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

import logging
from logging.handlers import RotatingFileHandler

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',  # Adjust level to capture only major changes
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'major_changes.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,  # Keep 5 backup files
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',  # Adjust level to capture only major changes
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',  # Capture INFO level logs
            'propagate': False,
        },
        'authentication': {
            'handlers': ['file', 'console'],
            'level': 'INFO',  # Capture INFO level logs
            'propagate': False,
        },
    },
}
# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f%vw+e-$)x!t(*+g912h60b!la@koq&an%l)&!sk@$1!4-@b0%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "unfold",
    'admin_tools_stats',  # this must be BEFORE 'admin_tools' and 'django.contrib.admin'
    'django_nvd3',
    'cache_cleaner',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'UserProfiles',
    'Dorms',
    'AcademicYear',
    'Actions',
    'Home',
    'Dashboard',
    # 'django_ratelimit',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout',
    # 'UserProfiles.middleware.RatelimitMiddleware',
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default backend
    # 'UserProfiles.authentication_backends.EmailBackend',
    # 'UserProfiles.auth_backends.StaffBackend',    # Custom staff backend
    # 'UserProfiles.auth_backends.ResidentBackend', # Custom resident backend
    # Add other backends as needed
]

ROOT_URLCONF = 'RMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]

WSGI_APPLICATION = 'RMS.wsgi.application'



'''ERIC AND YOLANDA, USE THIS DATABASE'''
'''ALL YOU NEDD TO DO IS TO APPLY MIGRATIONS'''
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

'''COMMENT THIS WHEN WORKING ON YOUR FILE'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),                  
    },

    # 'supabase': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'postgres',
    #     'USER': 'postgres.cesztotrungramvrtiqa',
    #     'PASSWORD': 'nSbWwmdEk#f2dv3',
    #     'HOST': 'aws-0-eu-central-1.pooler.supabase.com',
    #     'PORT': '5432',  # Default PostgreSQL port
        # python manage.py migrate --database=supabase
    # }
}



# DATABASE_ROUTERS = ['RMS.routers.DatabaseRouter']


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'UserProfiles.UserCred'



UNFOLD = {
    "SITE_HEADER": "Appears in sidebar at the top",
    "SITE_ICON": {
        "light": lambda request: static("images/2.png"),  # light mode
        "dark": lambda request: static("images/2.png"),
        },

    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png+xml",
            "href": lambda request: static("images/2.png"),
        },
    ],

    "SHOW_HISTORY": True,

    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Dashboard"),
                "separator": True,  # Top border
                "collapsible": True,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Home"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),     
                    },
                    {
                        "title": _("Analytics"),
                        "icon": "Timeline",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:admin_tools_stats_dashboardstats_changelist"), 
                        # "link": reverse_lazy("admin:AcademicYear_academicsession_changelist"),    
                    },
                    {
                        "title": _("Academic Sessions"),
                        "icon": "school",
                        "link": reverse_lazy("admin:AcademicYear_academicsession_changelist"),
                        # "badge": "formula.utils.badge_callback",
                    },
                    {
                        "title": _("Semesters"),
                        "icon": "book",
                        "link": reverse_lazy("admin:AcademicYear_semester_changelist"),
                    },
                    {
                        "title": _("Enrollments"),
                        "icon": "calendar_today",
                        "link": reverse_lazy("admin:AcademicYear_enrollment_changelist"),
                    },
                ],
            },
            {
                "title": _("Housing"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Dorms"),
                        "icon": "House",
                        "link": reverse_lazy("admin:Dorms_dorm_changelist"),
                    },
                    {
                        "title": _("Rooms"),
                        "icon": "Bed",
                        "link": reverse_lazy("admin:Dorms_room_changelist"),
                    },
                    {
                        "title": _("Storage Location"),
                        "icon": "Room",
                        "link": reverse_lazy("admin:Dorms_storage_changelist"),
                    },
                    {
                        "title": _("Storage Items"),
                        "icon": "apps",
                        "link": reverse_lazy("admin:Dorms_storageitem_changelist"),
                    },
                    {
                        "title": _("Announcements"),
                        "icon": "Notifications",
                        "link": reverse_lazy("admin:Actions_announcement_changelist"),
                    },
                    {
                        "title": _("Complaints"),
                        "icon": "Transcribe",
                        "link": reverse_lazy("admin:Actions_complaint_changelist"),
                    },
                    
                ],
            },
                        {
                "title": _("Maintenance"),
                "separator": True,  # Top border
                "collapsible": True,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Maintenance Requests"),
                        "icon": "Report",
                        "link": reverse_lazy("admin:Actions_maintenancerequest_changelist"),
                    },
                    {
                        "title": _("Maintenance Categories"),
                        "icon": "Category",
                        "link": reverse_lazy("admin:Actions_category_changelist"),
                    },
                    {
                        "title": _("Maintenance Sub-Categories"),
                        "icon": "Subject",
                        "link": reverse_lazy("admin:Actions_subcategory_changelist"),
                    },
                    
                ],
            },
            {
                "title": _("People"),
                "separator": True,  # Top border
                "collapsible": True,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Residents"),
                        "icon": "groups_3",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:UserProfiles_residents_changelist"),   
                        
                    },
                    {
                        "title": _("Staffs"),
                        "icon": "connect_without_contact",
                        "link": reverse_lazy("admin:UserProfiles_staffs_changelist"),
                        # "badge": "formula.utils.badge_callback",
                    },
                    {
                        "title": _("Staff Assignment"),
                        "icon": "social_distance",
                        "link": reverse_lazy("admin:AcademicYear_staffassignment_changelist"),
                        # "badge": "formula.utils.badge_callback",
                    },
                    {
                        "title": _("Roles"),
                        "icon": "hotel_class",
                        "link": reverse_lazy("admin:UserProfiles_roles_changelist"),
                    },
                    {
                        "title": _("Users"),
                        "icon": "person_search",
                        "link": reverse_lazy("admin:UserProfiles_usercred_changelist"),
                    },
                ],
            },
            
        ],
    },

    

}


from datetime import timedelta

AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(minutes=5),
    'SESSION_TIME': timedelta(minutes=30),
    'MESSAGE': 'The session has expired. Please login again to continue.',
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
}