from django.db import models

class Faculty(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    faculty = models.ForeignKey(
        "faculty.Faculty", on_delete=models.CASCADE, related_name="departments")

    def __str__(self):
        return self.name

