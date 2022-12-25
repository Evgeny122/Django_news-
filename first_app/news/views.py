from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import NewsModelForm, CommentaryModelForm
from news.models import News, Commentaries, Likes, Dnot_likes
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse


def index(request, *args, **kwargs):
    qs = News.objects.all()
    context = {'news_list' : qs}
    return render(request, 'index.html', context)


def detail_view(request, pk):
    user = request.user
    liked = False
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404

    if request.user.is_authenticated and obj.likes.filter(user=user):
        liked = True
    
    return render(request, 'news/detail.html', {'single_object': obj, 'liked':liked})


@login_required
@permission_required('user.is_staff', raise_exception=True)
def create_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = NewsModelForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return render(request, 'forms.html', {'form':form, 'obj':obj})
    form = NewsModelForm(request.POST or None)
    return render(request, 'forms.html', {'form':form} ) 
        
@login_required
@permission_required('user.is_staf')
def edit_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = NewsModelForm(request.POST, instance=obj)
        if form.is_valid():
            edited_obj = form.save(commit=False)
            edited_obj.save()
    else:
        form = NewsModelForm(instance=obj)
    
    
    return render(request, 'edit_news_forms.html', {'single_object': obj, 'form' : form})

@login_required
@permission_required('user.is_staff')
def delete_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
        all_commentary = obj.commentary.all()
        all_like = obj.likes.all()
        all_dnot_like = obj.dnot_likes.all()
    except News.DoesNotExist:
        raise Http404
    all_dnot_like.delete()
    all_like.delete()
    all_commentary.delete()
    obj.delete()
    return HttpResponseRedirect(reverse('index'))

@login_required
def commentary_view(request, pk):
    form = CommentaryModelForm(request.POST or None)
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    
    if form.is_valid():
        text = form.cleaned_data.get('text')
        user = request.user
        commentary_obj = Commentaries(user=user, text=text)
        commentary_obj.save()
        obj.commentary.add(commentary_obj)
        obj.save()
        
        return HttpResponseRedirect(reverse('detail-news', args=[pk]))

    return render (request, 'news/commentary.html', {'single_object' : obj, 'form': form})

@login_required
def commentary_view_delete(request, pk):
    try:
        commentary = Commentaries.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    commentary.delete()
    
    return redirect(('/'))

@login_required
def commentary_view_edit(request, pk):
    try:
        commentary = Commentaries.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = CommentaryModelForm(request.POST, instance=commentary)
        if form.is_valid():
            edit_com = form.save(commit=False)
            edit_com.save()
            return redirect(('/'))
    else:
        form = CommentaryModelForm(instance=commentary)
    
    return render(request, 'edit_commentary_forms.html', {'single_object' : commentary, 'form' : form})
    
def likes_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        user = request.user
        if not obj.likes.filter(user=user):
            like_obj = Likes(user=user, like=True)
            like_obj.save()
            obj.likes.add(like_obj)
            obj.save()
            if obj.dnot_likes.filter(user=user):
                obj.dnot_likes.filter(user=user).delete()      
        elif not obj.dnot_likes.filter(user=user):
            dnot_like_obj = Dnot_likes(user=user, dnot_like=True)
            dnot_like_obj.save()
            obj.dnot_likes.add(dnot_like_obj)
            obj.save()
            if obj.likes.filter(user=user):
                obj.likes.filter(user=user).delete()
    return HttpResponseRedirect(reverse('detail-news', args=[pk]))