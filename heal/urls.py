from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


from .views import MemberViewSet
from .views import CourseApplyViewSet

router = DefaultRouter()

router.register(r'member', MemberViewSet, base_name='member')
router.register(r'apply', CourseApplyViewSet, base_name='apply')

urlpatterns = [
	url(r'^api/', include(router.urls)),
]

