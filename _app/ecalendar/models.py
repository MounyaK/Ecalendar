from django.db import models

# Create your models here.
from django.urls import reverse


class Event(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    # description = models.TextField()
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    nbre_siege = models.PositiveIntegerField()
    salle_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()
    disposition_id = models.PositiveIntegerField()

    # requester = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        url = reverse('ecalendar:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    @property
    def get_info(self):
        return "start:%s\nend:%s" % (self.start_time, self.end_time)


class Room(models.Model):
    title = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    salle_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()
    objects = models.Manager()

    def __str__(self):
        return self.title

    @property
    def get_title(self):
        return self.title

    @property
    def get_email(self):
        return self.email

    @property
    def get_password(self):
        return self.password

    @property
    def get_id(self):
        return self.salle_id

    @property
    def get_userid(self):
        return self.user_id

    # @property
    # def set_room(self):
    #     global CURRENT_ROOM
    #     CURRENT_ROOM = self
    #     print(self)
    #     return True
