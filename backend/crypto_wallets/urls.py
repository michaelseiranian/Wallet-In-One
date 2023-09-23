from django.urls import path, include
from rest_framework.routers import DefaultRouter

from crypto_wallets import views

router = DefaultRouter()
router.register('', views.CryptoWalletViewSet, basename='crypto_wallet_view_set')

urlpatterns = [
    path('', include(router.urls), name='crypto_wallets'),
    path('insights', views.CryptoWalletInsights.as_view(), name='crypto_wallet_insights'),
    path('update', views.CryptoWalletUpdate.as_view(), name='crypto_wallet_update'),
]
