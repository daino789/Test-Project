from loginsystem.views import Signup, Login, Logout, signup_template, login_template
from rest_framework.routers import DefaultRouter
from django.conf.urls import url

router = DefaultRouter()

router.register(r'api_signup', Signup, base_name='api_signup'),
router.register(r'apI_login', Login, base_name='api_login'),
router.register(r'api_logout', Logout, base_name='api_logout'),
# router.register(r'pets', PetView, base_name='pets'),


urlpatterns = [
    url(r'^signup/$', signup_template, name='signup'),
    url(r'^login/$', login_template, name='login'),
]

urlpatterns += router.urls



