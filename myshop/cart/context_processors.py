from .cart import Cart

# custom context processor variable
# The cart context processor will be executed every time a template is rendered using Django's RequestContext.
# The cart variable will be set in the context of your templates. You can read more about RequestContext at
def cart(request):
    return {'cart': Cart(request)}
