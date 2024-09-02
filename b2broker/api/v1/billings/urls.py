from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import TransactionViewSet, WalletViewSet

app_name = "billings"

router = SimpleRouter(trailing_slash=False)
router.register("wallets", WalletViewSet)
router.register("transactions", TransactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
