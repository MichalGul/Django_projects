from django.apps import AppConfig

"""
In order to register your signal receiver functions, when you use the receiver() decorator, 
you just need to import the signals module of your application inside the ready() method of 
the application configuration class. This method is called as soon as the application registry 
is fully populated. Any other initializations for your application should also be included in this method.
"""

class ImagesConfig(AppConfig):
    name = 'images'
    # app initialization method (run when django starts)
    def ready(self):
        # imports signal handlers
        pass