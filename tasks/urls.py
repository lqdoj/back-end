from rest_framework.routers import DefaultRouter

from tasks.views import TaskView

router = DefaultRouter()
router.register(prefix='', basename='tasks', viewset=TaskView)

urlpatterns = router.urls
