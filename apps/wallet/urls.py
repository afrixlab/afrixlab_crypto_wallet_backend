from django.urls import path
from . import views

app_name = 'wallet_app'

urlpatterns = [
    path('wallet/<int:user_id>/', views.wallet_detail, name='wallet_detail'),
    path('create_transaction/<int:user_id>/', views.create_transaction, name='create_transaction'),
]
