from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('create_account/', views.create_account, name='create_address'),
    path('account_info/<int:pk>', views.account_info, name='account_info'),
    path('deploy/', views.deploy, name='deploy'),
    path('send/',views.send_token, name='send'),
    path('send_eth', views.send_eth, name='send_eth'),
    path('send_presto', views.send_presto, name='send_presto'),
    path('etherf', views.etherf, name='etherf')
]
