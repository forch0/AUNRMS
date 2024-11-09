# from django_admin_charts import ChartConfig

# def setup_charts():
#     # Staff distribution by dorm and role (Bar chart)
#     ChartConfig.objects.get_or_create(
#         title="Staff Distribution by Dorm and Role",
#         model="AcademicYear.StaffAssignment",
#         chart_type="BarChart",
#         group_by="dorm__name",  
#         aggregate="count",      
#         field="role__name",     
#     )

#     # Assignment trends over time (Line chart)
#     ChartConfig.objects.get_or_create(
#         title="Assignment Trends Over Time",
#         model="AcademicYear.StaffAssignment",
#         chart_type="LineChart",
#         group_by="created_at",  
#         aggregate="count",      
#         field="role__name",     
#     )

#     # Role distribution (Pie chart)
#     ChartConfig.objects.get_or_create(
#         title="Role Distribution",
#         model="UserProfiles.Roles",
#         chart_type="PieChart",
#         group_by="name",            
#         aggregate="count",          
#     )

