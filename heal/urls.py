from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


from .views import MemberViewSet

router = DefaultRouter()

router.register(r'member', MemberViewSet, base_name='member')

urlpatterns = [
	url(r'^api/', include(router.urls)),
]

