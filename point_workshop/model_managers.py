from django.db import models

class UserAssignedRoleQuerySet(models.QuerySet):
    def ar(self):
        return self.filter(role__role_short_name='AR')

    def mod(self):
        return self.filter(role__role_short_name='MOD')

    def zone(self):
        return self.filter(role__role_short_name='ZONE')
    
    def central(self):
        return self.filter(role__role_short_name='CENTRAL')

    def core(self):
        return self.filter(role__role_short_name='CORE')


class UserAssignedRoleManager(models.Manager):
    def get_queryset(self):
        return UserAssignedRoleQuerySet(self.model, using=self._db)

    def ar(self):
        return self.get_queryset().ar()

    def mod(self):
        return self.get_queryset().mod()

    def zone(self):
        return self.get_queryset().zone()
    
    def central(self):
        return self.get_queryset().central()

    def core(self):
        return self.get_queryset().core()
