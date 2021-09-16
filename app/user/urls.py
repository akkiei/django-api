from django.conf.urls import url
from . import views

app_name = 'user'
urlpatterns = [

    url("create/", views.CreateUserView.as_view(), name='create'),
    url("token/", views.CreateTokenView.as_view(), name="token")
]
