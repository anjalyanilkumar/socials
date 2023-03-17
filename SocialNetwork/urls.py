"""SocialNetwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socials.views import LoginView, IndexView, signup, update_profile, sign_out_view, like_post, add_cmnts, cmt_like, follow,AddPostView,MyProfileView, deletepost
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='signin'),
    path('signup/', signup, name='signup'),
    path('profile/',MyProfileView.as_view(), name='profile'),
    path('editprofile/',update_profile,name='editprofile'),
    path('post/add/',AddPostView.as_view(), name='createpost'),
    path('posts/<int:id>/like/', like_post,name='like-post'),
    path('posts/<int:id>/comment/add', add_cmnts,name='add-cmt'),
    path('comment/<int:id>/like/', cmt_like,name='cmt-like'),
    path('home/', IndexView.as_view(), name='home'),
    path("logout", sign_out_view, name="logout"),
    path("posts/<int:id>/delete", deletepost, name='deletepost'),
    path("follow/<int:id>/user", follow, name='follow')


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
