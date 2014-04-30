from django.conf.urls import patterns, include, url
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'jobstatuses', views.JobStatusViewSet)
router.register(r'teststatuses', views.TestStatusViewSet)
router.register(r'jobs', views.JobViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
