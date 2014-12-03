from django.conf.urls import patterns
from django.conf.urls import url

from .views import IndexView
from .views import LaunchView
from .views import ApplicationDetailedView
from .views import ApplicationStackLaunchView
from .views import ApplicationLaunchView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^launch$', LaunchView.as_view(), name='launch'),
    url(r'^application_detail$', ApplicationDetailedView.as_view(), name='application_detail'),
    url(r'^application_stacklaunch$', ApplicationStackLaunchView.as_view(), name='application_stacklaunch'),
    url(r'^application_launch$', ApplicationLaunchView.as_view(), name='application_launch')
)
