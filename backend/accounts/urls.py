from django.urls import path
from .views import sign_up, validate_token, graph_data
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('sign_up/', sign_up.as_view(), name='sign_up'),
    path('login/', obtain_auth_token, name='login'),
    path('validate_token', validate_token, name='validate_token'),
    path('graph_data/', graph_data, name='graph_data')
]