from django.conf.urls import patterns, include, url
from rest_framework import routers
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'labels', views.LabelViewSet)
router.register(r'hosts', views.HostViewSet)
router.register(r'tests', views.TestViewSet)
router.register(r'teststatuses', views.TestStatusViewSet)
router.register(r'profilers', views.ProfilerViewSet)
router.register(r'jobs', views.JobViewSet)
router.register(r'jobstatuses', views.JobStatusViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
