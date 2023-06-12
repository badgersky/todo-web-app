from django.db import models
from users.models import CustomUser


class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    date = models.DateField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ', ' + str(self.date)
