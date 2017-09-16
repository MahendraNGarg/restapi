
from django.conf.urls import url, include

from . import views




urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sign_up/$', views.SignUp.as_view(), name="sign_up"),
    url(r'^login/$', views.UserAPILoginView.as_view(), name="login"),
    url(r'^user_activation_link/(?P<user_id>(\w+))/(?P<token>([A-Za-z0-9]+)-([A-Za-z0-9]+)-([A-Za-z0-9]+)-([A-Za-z0-9]+)-([A-Za-z0-9]+))+/$',
views.UserActivation.as_view(), name="user_activation_link"),

     # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = router.urls