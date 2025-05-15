from django.shortcuts import render
from basic.models import Blog
from basic.forms import BlogForm
from django.http import HttpResponseRedirect
from django.db.models import Q
from user.views import check_login_view
from django.contrib.auth.decorators import login_required
from userprofile.models import UserProfile
import json 

def home_view(request):
    # import sqlite3
    # print(sqlite3.version)
    # data = Blog.objects.all().values() // important  : if you don't want foreign key data 
    is_logged_in = check_login_view(request)
    data = Blog.objects.filter(is_published__exact = True).select_related('user')
    if is_logged_in:
        profile = UserProfile.objects.get(user = request.user)
        dict = {
        "blogs": data,
        "is_logged_in" : is_logged_in,
        "liked_list" : json.loads(profile.liked_blog_ids)
    }
    else:
        dict = {
        "blogs": data,
        "is_logged_in" : is_logged_in
    }
    # print(data)
    # print(is_logged_in)    
    
    return render(request, 'basic/blogCard.html', context=dict)

@login_required
def create_blog_view(request):

    # print(request.method)
    if request.method == "POST":
        # print(request.POST)
        fm = BlogForm(request.POST)
        # print(fm)
        if fm.is_valid():  # validate form at server side
            # print("create somse data")
           #  print(fm.cleaned_data)
            title = fm.cleaned_data.get('title')
            content = fm.cleaned_data.get('content')
            is_published = fm.cleaned_data.get('is_published')
            create_data = Blog.objects.create(
                title=title,
                content=content,
                is_published=is_published,
                user = request.user
            )
            print(create_data.__dict__)
            return HttpResponseRedirect(f'/blog-content/{create_data.id}/no')
    else:
        fm = BlogForm()

    context = {
        "form": fm
    }
    return render(request, 'basic/createblog.html', context=context)


def blog_content_view(request, blog_id, confirm):
    # print("confirm", confirm)
    # print(blog_id)
    data = Blog.objects.get(id=blog_id)
    
    print(data.user.username)
    is_logged_in = check_login_view(request)
    # print(data.__dict__)
    context = {
        "blog": data,
        "confirm": confirm,
        "is_logged_in" : is_logged_in
    }
    return render(request, 'basic/blogContent.html', context=context)


def delete_blog_view(request, blog_id):
    # print(request.method)
    # print("eufasdfjklasdjl;", blog_id)
    if request.method == "POST":
        data = Blog.objects.get(id=blog_id)
        data.delete()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'basic/errorpage.html')

@login_required
def update_blog_view(request, blog_id):
    print("blog : ", blog_id)
    if request.method == "POST":
        print(request.POST)
        data = Blog.objects.get(id=blog_id)
        fm = BlogForm(request.POST)
        if fm.is_valid():
            title = fm.cleaned_data.get("title")
            content = fm.cleaned_data.get("content")
            is_published = fm.cleaned_data.get("is_published")
            print(title, content, is_published)
            data.title = title
            data.content = content
            data.is_published = is_published
            data.save()
        #    print(data.__dict__)
        return HttpResponseRedirect(f'/blog-content/{blog_id}/no')
    else:
        fm = BlogForm()
        data = Blog.objects.get(id=blog_id)
        context = {"form": fm, "blog": data}
        return render(request, 'basic/updateblog.html', context=context)


def search_blog_view(request):
    # print(request.method)
    # print(request.GET)
    search_value = request.GET.get("search")

    if search_value:
        print(search_value)
        # result = Blog.objects.filter(title__icontains=search_value,content__icontains  = search_value) # AND Condition
        result = Blog.objects.filter(Q(title__icontains=search_value) | Q(content__icontains  = search_value)) # OR Condition
        context = {
            "blogs": result
        }
        return render(request, "basic/searchPage.html", context=context)
    else:
        return render(request, "basic/searchPage.html")

@login_required
def update_like_count_view(request,blog_id):
    
    if request.method == "POST":
        data = Blog.objects.get(id=blog_id)
        print(data.like)
        
        previous_like = data.like

        profile = UserProfile.objects.get(user = request.user)
        # print(profile.__dict__)
        liked_list_str = profile.liked_blog_ids
        liked_list = json.loads(liked_list_str) # converting string "[]" into list []
        print(type(liked_list))


        if blog_id in liked_list:
            liked_list.remove(blog_id)
            data.like = previous_like - 1
            print("************************")
        else:
            liked_list.append(blog_id)
            data.like = previous_like + 1
            print("************************")
        # print(type(liked_list))
        # profile.liked_blog_ids = liked_list
        print("----------------------------")
        profile.liked_blog_ids = json.dumps(liked_list) # list [1,2,5] will convert into "[1,2,5]"
      
        profile.save()
        data.save()
        return HttpResponseRedirect('/')
    else:
        context = {
            'error' : "Get request is not accepted"
        }
        return HttpResponseRedirect('/')
