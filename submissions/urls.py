from rest_framework.routers import DefaultRouter

from submissions.views import SubmissionView


router = DefaultRouter()
router.register(prefix='', basename='submissions', viewset=SubmissionView)

urlpatterns = router.urls
