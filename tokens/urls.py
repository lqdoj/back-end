from rest_framework.routers import DefaultRouter

from tokens.views import TokenView

router = DefaultRouter()
router.register(prefix='', basename='tokens', viewset=TokenView)

urlpatterns = router.urls
