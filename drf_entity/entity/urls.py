from entity.api_views import EntityView
from rest_framework.routers import SimpleRouter

app_name = "entity"
urlpatterns = []
router = SimpleRouter()
router.register(r"", EntityView)
urlpatterns = urlpatterns + router.urls
