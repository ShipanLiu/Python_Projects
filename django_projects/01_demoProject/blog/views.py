from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment

def post_list_handle(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', locals()) # {{ posts }} get delivered into html file

def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user = request.user
        post = Post.objects.create(title=title, content=content, user=user)
        return redirect('post_list')
    return render(request, 'posts/create_post.html')

def create_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        content = request.POST['content']
        user = request.user
        Comment.objects.create(post=post, content=content, user=user)
        return redirect('post_list')
    return redirect('post_list')

def create_comment_reply(request, post_id, comment_id):
    post = Post.objects.get(pk=post_id)
    comment = Comment.objects.get(pk=comment_id)
    if request.method == 'POST':
        content = request.POST['content']
        user = request.user
        Comment.objects.create(post=post, content=content, user=user, parent_comment=comment)
        return redirect('post_list')
    return redirect('post_list')
