from django.contrib import admin

from schedule.models import Schedule


class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule
    readonly_fields = ("created_at", "updated_at")
    list_display = [
        "code",
        "title",
        "instructor",
        "day_of_week",
        "start_time",
        "end_time",
    ]

    fieldsets = (
        (None, {"fields": ("code",)}),
        ("Info", {
         "fields": ("title", "instructor", "day_of_week", "start_time", "end_time")}),
        (
            None,
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def day_of_week(self, obj):
        return obj.get_day_of_week_display()

    def instructor(self, obj):
        return obj.instructor.user.get_full_name()


admin.site.register(Schedule, ScheduleAdmin)
