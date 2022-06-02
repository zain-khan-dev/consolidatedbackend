from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('product', views.ProductViewSet)

router.register('customer', views.CustomerViewSet)

router.register("seller", views.SellerViewSet)

router.register("order", views.OrderView)


urlpatterns = [
    path('', include(router.urls)),
    path("addToCart/", views.AddToCartView.as_view()),
    path("cart/", views.UserCartView.as_view()),
    path('category/<str:type>', views.CategoryView.as_view()),
    path("uploadImage/", views.UploadImage.as_view()),
    path("productspecs/", views.ProductSpecs.as_view()),
    path("comments/", views.CommentView.as_view()),
    path("addFeature/", views.ProductFeatureView.as_view()),
    path("search/<str:query>", views.getSearchResult),
    path("orders/<str:filter>", views.getFilteredOrders),
    path("orders/<int:pk>/", views.changeOrderStatus)
]