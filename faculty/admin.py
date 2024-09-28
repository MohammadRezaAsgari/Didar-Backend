from django.contrib import admin

from faculty.models import Faculty, Department

class FacultyAdmin(admin.ModelAdmin):
    model = Faculty
    list_display = [
        "id",
        "name",
    ]

class DepartmentAdmin(admin.ModelAdmin):
    model = Department
    list_display = [
        "id",
        "name",
        "faculty",
    ]

admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department, DepartmentAdmin)

