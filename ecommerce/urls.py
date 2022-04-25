from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('product', views.ProductViewSet)

router.register('customer', views.CustomerViewSet)

urlpatterns = [
    path('seller/', views.SellerViews.as_view()),
    path('', include(router.urls)),
    path("order/", views.OrderView.as_view())
]