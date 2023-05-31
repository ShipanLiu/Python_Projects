from django.shortcuts import render, redirect
from .models import Post, Comment
from django.http import HttpResponse, HttpResponseRedirect

def post_list_handle(request):
    posts = Post.objects.all()
    dict = {
        "post_list": posts
    }
    return render(request, 'blog/post_list.html', dict) # {{ posts }} get delivered into html file

def create_post_handle(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        user = request.session.get("uid")
        post = Post.objects.create(title=title, content=content, user=user)
        return HttpResponseRedirect("/demo/blog/posts")

def create_comment_handle(request, post_id):
    warn = ""
    try:
        print("post_id: \n", post_id);
        post = Post.objects.get(id = post_id)
        print(post);
    except Exception as e:
        print("error by getting post: %s"%(e))
        warn = "post dose not exist"
        return HttpResponseRedirect("/demo/blog/posts")
    if request.method == 'POST':
        content = request.POST['comment_content']
        user = request.session.get("uid")
        Comment.objects.create(post=post, content=content, user=user)
    return HttpResponseRedirect("/demo/blog/posts")

def create_comment_reply(request, post_id, comment_id):
    post = Post.objects.get(pk=post_id)
    comment = Comment.objects.get(pk=comment_id)
    if request.method == 'POST':
        content = request.POST['content']
        user = request.user
        Comment.objects.create(post=post, content=content, user=user, parent_comment=comment)
        return redirect('post_list')
    return redirect('post_list')
