from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register("categories", views.CategoryViewSet, basename='category')

urlpatterns = router.urls
