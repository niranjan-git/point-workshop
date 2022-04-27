from django.db import models

class UserAssignedRoleQuerySet(models.QuerySet):
    def role(self):
        return self.filter(role='AR')


class UserAssignedRoleManager(models.Manager):
    def get_queryset(self):
        return UserAssignedRoleQuerySet(self.model, using=self._db)

    def role(self):
        return self.get_queryset().role()
