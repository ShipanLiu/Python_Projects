from django.shortcuts import render, redirect
from .models import Post, Comment
from django.http import HttpResponse, HttpResponseRedirect

def post_list_handle(request):
    posts = Post.objects.all()
    dict = {
        "post_list": posts,
        "current_login": request.session.get("username")
    }
    return render(request, 'blog/post_list.html', dict) # {{ posts }} get delivered into html file

def create_post_handle(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        uid = request.session.get("uid")
        uname = request.session.get("username")
        post = Post.objects.create(title=title, content=content, uid=uid, uname=uname)
        return HttpResponseRedirect("/demo/blog/posts")

def create_comment_handle(request, post_id):
    warn = ""
    try:
        post = Post.objects.get(id=post_id)
        print(post_id)
    except Exception as e:
        print("error by getting post: %s"%(e))
        warn = "post dose not exist"
        return HttpResponseRedirect("/demo/blog/posts")
    if request.method == 'POST':
        content = request.POST['comment_content']
        uid = request.session.get("uid")
        uname = request.session.get("username")
        Comment.objects.create(post=post, content=content, uid=uid, uname=uname)
    return HttpResponseRedirect("/demo/blog/posts")

def create_comment_reply_handle(request, post_id, comment_id):
    # get related post
    post = Post.objects.get(id=post_id)
    # get related comment
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        content = request.POST['content']
        uid = request.session.get("uid")
        uname = request.session.get("username")
        Comment.objects.create(post=post, content=content, uid=uid, uname=uname, parent_comment=comment)
    return HttpResponseRedirect("/demo/blog/posts")
