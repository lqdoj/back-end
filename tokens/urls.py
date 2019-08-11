from rest_framework import routers
from rest_framework.routers import SimpleRouter, Route

from tokens.views import TokenView


class TokenRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """
    routes = [
        Route(
            url='',
            mapping={'post': 'create', 'delete': 'destroy'},
            detail=False,
            name='tokens',
            initkwargs={}
        ),
    ]


router = TokenRouter()
router.register('tokens', TokenView)

urlpatterns = router.urls
