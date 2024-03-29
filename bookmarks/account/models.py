from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.



# However, the user model comes with very basic fields.
# You may wish to extend it to include additional data.
# The best way to do this is by creating a profile model that contains all
# additional fields and a one-to-one relationship with the Django User model.
# A one-to-one relationship is similar to a ForeignKey field with the parameter unique=True.
# The reverse side of the relationship is an implicit one-to-one relationship with the related model instead
# of a manager for multiple elements. From each side of the relationship, you retrieve a single related object.

# have all user filds plus given below (date_of_birth and photo)
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE) # delete profile when user is deleted
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)
    def __str__(self):
        return f'Profile for user {self.user.username}'


class Contact(models.Model):
    # User who creates the relationship
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    # User being followed
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    # when the relation was created
    created = models.DateTimeField(auto_now=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# Add following field to User dynamically todo change this to be in Profile model
user_model = get_user_model() #retrive User model
user_model.add_to_class('following', # add_to_class() method of Django models to monkey patch the User model
                        models.ManyToManyField('self',
                                               through=Contact,
                                               related_name='followers',
                                               symmetrical=False))
