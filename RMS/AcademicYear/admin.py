from django.contrib import admin
from .models import AcademicSession, Semester
from .forms import SemesterForm
@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','start_year','end_year')
    search_fields = ('timeline',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    form = SemesterForm
    list_display = ('id', 'semester_type', 'academic_session', 'start_date', 'end_date')
    list_filter = ('semester_type', 'academic_session__start_year', 'academic_session__end_year')
    search_fields = ('semester_type', 'academic_session__name')
    fieldsets = (
        (None, {
            'fields': ('semester_type', 'start_date', 'end_date', 'academic_session')
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('academic_session')  # Ensure academic_session is fetched in one query
        return queryset

    def academic_session__start_year(self, obj):
        return obj.academic_session.start_year

    academic_session__start_year.admin_order_field = 'academic_session__start_year'
    academic_session__start_year.short_description = 'Academic Start Year'

    def academic_session__end_year(self, obj):
        return obj.academic_session.end_year

    academic_session__end_year.admin_order_field = 'academic_session__end_year'
    academic_session__end_year.short_description = 'Academic End Year'
    form = SemesterForm
    list_display = ('id', 'semester_type', 'academic_session', 'start_date', 'end_date')
    list_filter = ('semester_type', 'academic_session__start_year', 'academic_session__end_year')
    search_fields = ('semester_type', 'academic_session__name')
    fieldsets = (
        (None, {
            'fields': ('semester_type', 'start_date', 'end_date', 'academic_session')
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('academic_session')  # Ensure academic_session is fetched in one query
        return queryset

    def academic_session__start_year(self, obj):
        return obj.academic_session.start_year

    academic_session__start_year.admin_order_field = 'academic_session__start_year'
    academic_session__start_year.short_description = 'Academic Start Year'

    def academic_session__end_year(self, obj):
        return obj.academic_session.end_year

    academic_session__end_year.admin_order_field = 'academic_session__end_year'
    academic_session__end_year.short_description = 'Academic End Year'
    list_display = ('id', 'semester_type', 'academic_session', 'start_date', 'end_date')
    list_filter = ('semester_type', 'academic_session__start_year', 'academic_session__end_year')
    search_fields = ('semester_type', 'academic_session__name')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('academic_session')  # Ensure academic_session is fetched in one query
        return queryset

    def academic_session__start_year(self, obj):
        return obj.academic_session.start_year

    academic_session__start_year.admin_order_field = 'academic_session__start_year'
    academic_session__start_year.short_description = 'Academic Start Year'

    def academic_session__end_year(self, obj):
        return obj.academic_session.end_year

    academic_session__end_year.admin_order_field = 'academic_session__end_year'
    academic_session__end_year.short_description = 'Academic End Year'
    list_display = ('id', 'semester_type', 'academic_session', 'start_date', 'end_date')
    list_filter = ('semester_type', 'academic_session__start_year', 'academic_session__end_year')
    search_fields = ('semester_type', 'academic_session__timeline')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('academic_session')  # Ensure academic_session is fetched in one query
        return queryset

    def academic_session__start_year(self, obj):
        return obj.academic_session.start_year

    academic_session__start_year.admin_order_field = 'academic_session__start_year'
    academic_session__start_year.short_description = 'Academic Start Year'

    def academic_session__end_year(self, obj):
        return obj.academic_session.end_year

    academic_session__end_year.admin_order_field = 'academic_session__end_year'
    academic_session__end_year.short_description = 'Academic End Year'
    list_display = ('id', 'semester_type', 'academic_session', 'start_date', 'end_date')
    list_filter = ('semester_type', 'academic_session__start_year', 'academic_session__end_year')
    search_fields = ('semester_type', 'academic_session__timeline')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('academic_session')  # Ensure academic_session is fetched in one query
        return queryset

    def academic_session__start_year(self, obj):
        return obj.academic_session.start_year

    academic_session__start_year.admin_order_field = 'academic_session__start_year'
    academic_session__start_year.short_description = 'Academic Start Year'

    def academic_session__end_year(self, obj):
        return obj.academic_session.end_year

    academic_session__end_year.admin_order_field = 'academic_session__end_year'
    academic_session__end_year.short_description = 'Academic End Year'