from urllib.parse import quote_plus

from django.core.urlresolvers import reverse
from django.contrib import messages 
from django.http import  HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.db.models import Q 
from django.shortcuts import render, get_object_or_404, redirect 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.utils import timezone

from .forms import PostForm,CommentForm
from .models import Post, Comment





# Create your views here.
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
       raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.success(request, " Not Successfully created")
    #form = PostForm()
    context = {
        "form":form,
    }
    return render (request,"post_form.html",context)

def post_detail(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    comments = instance.comments.all()
    form = CommentForm()
    if instance.publish > timezone.now() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "form": form,
        "comments": comments,
        "instance":instance,
        "share_string": share_string,
    }
    return render (request,"post_detail.html",context)

def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "title": "My User List",
        "page_request_var":page_request_var,
        "today": today,
    }
    return render (request,"post_list.html",context)


def post_update(request, slug):
    instance = get_object_or_404(Post,slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        #print (form.cleaned_data.get("title"))
        instance.save()
        #message success
        #messages.success(request, "<a href='#'> Item</a> Saved", extra_tags='html_safe')
        messages.success(request, "<a href='#'> Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    #else:
        #messages.error(request, "Not Succesfully Created")

    context  = {
        "title": instance.title,
        "product": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("post:list")


def add_comment_to_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            print("!!!!!!")
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    return redirect(reverse('post:detail', kwargs = {"slug": post.slug}))


# @login_required
# def comment_approve(request, slug):
#     comment = get_object_or_404(Comment, slug=slug)
#     comment.approve()
#     return redirect('post_detail', slug=comment.post.slug)

# @login_required
# def comment_remove(request, slug):
#     comment = get_object_or_404(Comment, slug=slug)
#     comment.delete()
#     return redirect('post_detail', slug=comment.post.slug)
#comments
# def addcomment(request, article_id):
#     if request.POST and ("pause" not in request.session):
#         form = CommentForm(request.POST)
#     if form.is_valid():

#         comment = form.save(commit=False)
#         comment.comments_author = request.user # ! получить пользователя !
#         comment.comments_article = Article.objects.get(id=article_id)


#     form.save()
#     request.session.set_expiry(60)
#     request.session['pause'] = True
#     return redirect('/articles/get/%s/' % article_id)