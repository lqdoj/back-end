from rest_framework import routers

from users.views import UserView

router = routers.DefaultRouter()
router.register('', UserView, 'users')
urlpatterns = router.urls

