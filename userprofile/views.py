from django.shortcuts import render
from django.http import HttpResponseRedirect
from user.views import check_login_view
# Create your views here.
from basic.models import Blog
from userprofile.models import UserProfile
import json


def profile_view(request):
    is_logged_in = check_login_view(request)
    if is_logged_in:
        my_blogs = Blog.objects.filter(user=request.user)
        profile = UserProfile.objects.get(user=request.user)
        liked_blogs = Blog.objects.filter(
            id__in=json.loads(profile.liked_blog_ids))
        hidden_blogs = Blog.objects.filter(is_published__exact = False)
        context = {
            "is_logged_in": is_logged_in,
            "my_blogs": my_blogs,
            "liked_list": json.loads(profile.liked_blog_ids),
            "liked_blogs" : liked_blogs,
            "hidden_blogs" : hidden_blogs
        }
        return render(request, 'userprofile/userprofile.html', context=context)
    else:
        return HttpResponseRedirect('/')
