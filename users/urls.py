from rest_framework import routers

from users.views import UserView

router = routers.SimpleRouter()
router.register('', UserView, 'users')
urlpatterns = router.urls
