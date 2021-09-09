from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class Action(models.Model):
    # The user who performed action
    user = models.ForeignKey('auth.User',
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)
    # describtion ofe the action that was performed
    verb = models.CharField(max_length=255)
    # foreign key field that potins to the ContentType model
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    # Int field for storing the primary key of the related object
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    # GenericForeignKey field to the related objects based on the combination of the two previous fields
    target = GenericForeignKey('target_ct', 'target_id')

    # date and time the action was created
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)