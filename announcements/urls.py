from rest_framework import routers
from announcements.views import AnnouncementsView

router = routers.DefaultRouter()
router.register('', AnnouncementsView, 'announcements')

urlpatterns = router.urls
