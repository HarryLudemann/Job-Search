from django.db import models

# Create your models here.
class Occupation(models.Model):
    userid = models.CharField(max_length=20)
    employer = models.BooleanField()
    student = models.BooleanField()

    def __str__(self):
        return self.userid
        return self.employer
        return self.student