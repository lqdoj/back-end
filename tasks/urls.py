from rest_framework.routers import DefaultRouter

from tasks.views import TasksView

router = DefaultRouter()
router.register(prefix='', basename='tasks', viewset=TasksView)

urlpatterns = router.urls
