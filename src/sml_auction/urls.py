from sml_auction import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'auctions', views.AuctionApi)
urlpatterns = router.urls
