from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Image


# register the users_like_changed as a receiver using reciever decorator
@receiver(m2m_changed, sender=Image.users_like.through) # attach reciever to m2m_change signal  Then, you connect the function to Image.users_like.through so that the function is only called if the m2m_changed signal has been launched by this sender.
def users_like_changed(sender, instance, **kwargs):
    print('Signal recieved')
    print(sender)
    print(type(instance))
    print(instance)
    instance.total_likes = instance.users_like.count()
    instance.save()

