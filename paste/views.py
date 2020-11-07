from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Paste, PasteCatalog
from django.core.exceptions import PermissionDenied
from .forms import PasteEditForm, PasteCreateForm, CatalogForm
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse_lazy
from django.core.paginator import Paginator


def show_page(request, page):

    paste_list = Paste.unexpired_objects.order_by('-creation_date')
    p = Paginator(paste_list, 10)
    page_obj = p.page(page)

    context = {'paste_list': page_obj.object_list, 'page_obj': page_obj}

    return render(request, 'paste/pastes.html', context)


def show_all(request):

    return redirect('paste:show_page', page=1)


def detail(request, paste_hash):

    paste = get_object_or_404(Paste.unexpired_objects, hash=paste_hash)
    form = PasteEditForm(instance=paste, user=None)
    context = {'form': form}

    return render(request, 'paste/detail.html', context)


def download(request, paste_hash):

    paste = get_object_or_404(Paste.unexpired_objects, hash=paste_hash)

    return HttpResponse(paste.text, content_type='text/plain')


@login_required(login_url=reverse_lazy('common:login'))
def show_my_page(request, page):

    paste_list = Paste.unexpired_objects.filter(owner=request.user, catalog__isnull=True)
    p = Paginator(paste_list, 10)
    page_obj = p.page(page)

    catalog_list = PasteCatalog.objects.filter(owner=request.user)

    context = {'paste_list': page_obj.object_list, 'page_obj': page_obj, 'catalog_list': catalog_list}

    return render(request, 'paste/pastes.html', context)


@login_required(login_url=reverse_lazy('common:login'))
def show_my_pastes(request):

    return redirect('paste:show_my_page', page=1)


def edit(request, paste_hash):

    paste = get_object_or_404(Paste, hash=paste_hash, owner=request.user)

    if request.method == 'POST':

        if request.POST.get('_method', '').lower() == 'delete':
            paste.delete()
            return redirect('paste:show_my_pastes')

        form = PasteEditForm(request.user, request.POST, instance=paste)
        if form.is_valid():
            try:
                form.save()
                return redirect('paste:detail', paste_hash)

            except IntegrityError:
                form.add_error(None, "Invalid data")

        return render(request, "paste/edit.html", {'form': form})

    if request.method == 'GET':

        form = PasteEditForm(request.user, instance=paste)
        return render(request, "paste/edit.html", {'form': form})


def create(request):

    if request.method == 'GET':
        form = PasteCreateForm(request.user)
        return render(request, "paste/create.html", {'form': form})

    if request.method == 'POST':
        form = PasteCreateForm(request.user, request.POST)

        if form.is_valid():
            new_paste = form.save(commit=False)
            if request.user.is_authenticated:
                new_paste.owner = request.user
            try:
                new_paste.save()
                return redirect('paste:detail', new_paste.hash)
            except IntegrityError as e:
                pass

        form.add_error(None, "Invalid data")
        return render(request, "paste/create.html", {'form': form})


@login_required(login_url=reverse_lazy('common:login'))
def create_catalog(request):

    if request.method == 'GET':
        form = CatalogForm(request.user)
        return render(request, "paste/create_folder.html", {'form': form})

    if request.method == 'POST':

        form = CatalogForm(request.user, request.POST)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                form.add_error(None, "Invalid data")
                return render(request, "paste/create_folder.html", {'form': form})

        return redirect('paste:show_my_pastes')


@login_required(login_url=reverse_lazy('common:login'))
def detail_catalog(request, catalog_name):

    catalog = get_object_or_404(PasteCatalog, name=catalog_name, owner=request.user)

    if request.method == 'POST' and request.POST.get('_method') == 'delete':
        catalog.delete()
        return redirect('paste:show_my_pastes')

    if request.method == 'GET':

        catalog = get_object_or_404(PasteCatalog, owner=request.user, name=catalog_name)
        paste_list = Paste.unexpired_objects.filter(catalog=catalog)

        return render(request, 'paste/detail_folder.html', {'paste_list': paste_list})
