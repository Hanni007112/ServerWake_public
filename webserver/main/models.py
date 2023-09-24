from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class ServerAllocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startTime = models.DateTimeField(blank=False)
    endTime = models.DateTimeField(blank=False)
    active = models.BooleanField(default=True)

    class Meta:
        permissions = [
            ("create_Allocation", "Can allocate the server"),
        ]
    
    def __str__(self):
        duration = self.endTime - self.startTime
        duration_sec = duration.seconds
        hour_count, rem = divmod(duration_sec, 3600)
        return str(self.user.__str__() + f" {duration.days} days {hour_count} hours")
    
class ServerPing(models.Model):
    timestamp = models.DateTimeField(blank=False)
    successful = models.BooleanField(blank=False)

    class Meta:
        get_latest_by = "timestamp"

    def __str__(self):
        timestampstr = self.timestamp.strftime("%d.%m.%Y, %H:%M ") + str(self.successful)
        return str(timestampstr )
    
class ServerStatistic(models.Model):
    date = models.DateField(blank = False)
    
    h_00 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_01 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_02 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_03 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_04 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_05 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_06 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_07 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_08 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_09 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_10 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_11 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_12 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_13 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_14 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_15 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_16 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_17 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_18 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_19 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_20 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_21 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_22 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    h_23 = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def OnPercent_hour(self, hour:int): #returns the % of on Time as Value betweeen 0 and 100
        if hour == 00: return self.h_00
        if hour == 1: return self.h_01
        if hour == 2: return self.h_02
        if hour == 3: return self.h_03
        if hour == 4: return self.h_04
        if hour == 5: return self.h_05
        if hour == 6: return self.h_06
        if hour == 7: return self.h_07
        if hour == 8: return self.h_08
        if hour == 9: return self.h_09
        if hour == 10: return self.h_10
        if hour == 11: return self.h_11
        if hour == 12: return self.h_12
        if hour == 13: return self.h_13
        if hour == 14: return self.h_14
        if hour == 15: return self.h_15
        if hour == 16: return self.h_16
        if hour == 17: return self.h_17
        if hour == 18: return self.h_18
        if hour == 19: return self.h_19
        if hour == 20: return self.h_20
        if hour == 21: return self.h_21
        if hour == 22: return self.h_22
        if hour == 23: return self.h_23
    
    def OnPercent_day(self):
        sum = 0
        for i in range(24):
            sum += self.OnPercent_hour(i)
        return int(sum/24)

    def __str__(self):
        return self.date.strftime("%d.%m.%Y ")  + str(self.OnPercent_day()) + "%"
