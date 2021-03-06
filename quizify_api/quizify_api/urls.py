"""quizify_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from quiz.views import CategoryViewSet, GameViewSet, RoundViewSet, accept_invite
from accounts.views import register, PlayerViewSet, login, search_by_username

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'games', GameViewSet)
router.register(r'rounds', RoundViewSet)
router.register(r'players', PlayerViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^register/', register),
    url(r'^login/', login),
    url(r'^accept_invite/', accept_invite),
    url(r'^search_by_username/', search_by_username),
]
