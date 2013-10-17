
from django.db import models

class Bug(models.Model):

    assignee = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    milestone = models.DateField()

    class Meta:
        db_table = "engineering_bugs"


class BuildStatus(models.Model):

    published = models.DateField()
    status = models.CharField(max_length=255)
    project = models.CharField(max_length=255)

    class Meta:
        db_table = "engineering_build_status"




