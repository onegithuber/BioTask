from django.conf.urls import include, url
from tast.views import EditView, RegisterView

urlpatterns = [
    url(r'^all/$', 'tast.views.index', name='index'),
    url(r'^all/(\d+)/$', 'tast.views.platform', name='platform'),
    url(r'^reedit/(\d+)/$', 'tast.views.reedit', name='reedit'),
    url(r'^detail/(\d+)/$', 'tast.views.detail', name='detail'),
    url(r'^all/search/$', 'tast.views.search', name='search'),
    url(r'^edit/$', EditView.as_view(), name='edit'),
    url(r'^login/$', 'tast.views.loginview', name='login'),
    url(r'^loginout/$', 'tast.views.loginoutview', name='loginout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^tast_histogram', 'tast.views.histogram', name='histogram'),
    url(r'downfile/(.+)/(.+)', 'tast.views.send_file', name='downfile'),
    url(r'^$', 'tast.views.home', name='home'),
    url(r'^workinghour/$', 'tast.views.statistical_work_hours', name='workinghour'),
    url(r'^stackedbarchart', 'tast.views.stacked_bar_chart', name='stacked'),
    url(r'^json', 'tast.views.jsonlist', name='jsonlist'),
]
