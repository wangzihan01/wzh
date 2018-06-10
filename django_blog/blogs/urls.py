# @Time    : 18-6-5 下午2:19
# @Author  : wengwenyu
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
from .views import index
from .views import list
from .views import blog_detail
from .views import SearchView
urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^list/$',list,name = 'list'),
    url(r'^search/$',SearchView.as_view(),name='search'),
    url(r'^tags/(?P<tid>[0-9]+)/$',list,name='tags'),
    url(r'^category/(?P<cid>[0-9]+)/$', list,name='category'),
    url(r'^blog/(?P<bid>[0-9]+)/$', blog_detail,name='blog_detail')
]
