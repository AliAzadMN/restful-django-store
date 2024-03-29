from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register("categories", views.CategoryViewSet, basename='category')
router.register("products", views.ProductViewSet, basename='product')

products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("comments", views.CommentViewSet, basename='product-comments')

urlpatterns = router.urls + products_router.urls
