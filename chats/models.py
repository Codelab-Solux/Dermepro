from django.db import models
from accounts.models import CustomUser
# from .utils import ThreadManager
from django.db.models import Q

# class TrackingModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True


# class Thread(TrackingModel):
#     THREAD_TYPE = (
#         ('personal', 'Personal'),
#         ('group', 'Group')
#     )

#     name = models.CharField(max_length=50, null=True, blank=True)
#     thread_type = models.CharField(
#         max_length=15, choices=THREAD_TYPE, default='group')
#     users = models.ManyToManyField(CustomUser)

#     objects = ThreadManager()

#     def __str__(self) -> str:
#         if self.thread_type == 'personal' and self.users.count() == 2:
#             return f'{self.users.first()} and {self.users.last()}'
#         return f'{self.name}'


class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs

    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_second_person')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ThreadManager()

    class Meta:
        unique_together = ['first_person', 'second_person']

    def __str__(self) -> str:
        return f'{self.first_person.username} & {self.second_person.username}>'


class Message(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name='chat_thread')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'From <Thread - {self.thread}>'
