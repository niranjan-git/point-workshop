from django.utils.timezone import now
from django.db import models
from . import model_managers
try:
    from user.models import User
except Exception as e:
    print("Exception in importing User model: ",e)


# Create your models here.


class DatetimeCreated(models.Model):
    created = models.DateTimeField(auto_now_add=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class State(DatetimeCreated, models.Model):
    state_code = models.CharField(max_length=20)
    state_name = models.CharField(max_length=50)
    # zone = models.ForeignKey('Zone', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.state_code


class City(DatetimeCreated, models.Model):
    city_code = models.CharField(max_length=20)
    city_name = models.CharField(max_length=50)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.city_code


class Pincode(DatetimeCreated, models.Model):
    pincode = models.CharField(max_length=6)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.pincode


class Zone(DatetimeCreated, models.Model):
    zone_code = models.CharField(max_length=20)
    zone_name = models.CharField(max_length=50)
    remarks = models.CharField(max_length=100, null=True, blank=True)    

    def __str__(self):
        return self.zone_code


class ZoneStateMap(DatetimeCreated, models.Model):
    zone = models.ForeignKey('Zone', on_delete=models.CASCADE)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True)

    unique_together = ('zone', 'state')

    def __str__(self):
        return "%s  %s" % (self.zone.zone_code, self.state.state_code)


class Branch(DatetimeCreated, models.Model):
    zone = models.ForeignKey('Zone', on_delete=models.CASCADE)
    branch_code = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=50)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.branch_name



class Role(models.Model):
    '''
    Role for different user authorization
    '''

    id = models.AutoField(primary_key=True)
    role_short_name = models.CharField(unique=True, max_length=20)
    role_full_name = models.CharField(max_length=50, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_short_name




class UserAssignedRole(DatetimeCreated, models.Model):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True) 
    zone = models.ForeignKey('Zone', on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True)

    objects = model_managers.UserAssignedRoleManager()
    # def __str__(self):
    #     return str(self.user)

    def __str__(self):
        return '%s %s' % (self.user, self.role)


class Batch(DatetimeCreated, models.Model):
    name = models.CharField(max_length=50)
    remarks = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    st_date = models.DateField()
    en_date = models.DateField()


    def __str__(self):
        return self.name



class Participant(DatetimeCreated, models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=12)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class EnrolledParticipant(DatetimeCreated, models.Model):
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE)
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.batch.name, self.participant.email)