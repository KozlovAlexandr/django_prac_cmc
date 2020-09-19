from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Paste
from django.core.exceptions import PermissionDenied
from .forms import PasteEditForm, PasteCreateForm
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views import View

def show_all(request):

    paste_list = Paste.unexpired_objects.order_by('-creation_date')
    context = {'paste_list': paste_list}
    return render(request, 'paste/pastes.html', context)


def detail(request, paste_hash):

    paste = get_object_or_404(Paste.unexpired_objects, hash=paste_hash)
    can_edit = paste.owner == request.user
    context = {'paste': paste, 'can_edit': can_edit}

    return render(request, 'paste/detail.html', context)


@login_required(login_url='/login')
def show_my_pastes(request):

    paste_list = Paste.unexpired_objects.filter(owner=request.user).order_by('-creation_date')

    return render(request, 'paste/pastes.html', {'paste_list': paste_list})


def edit(request, paste_hash):

    paste = get_object_or_404(Paste, hash=paste_hash)
    if paste.owner != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = PasteEditForm(request.POST, instance=paste)
        if form.is_valid():
            try:
                form.save()
                return redirect('detail', paste_hash)

            except IntegrityError:
                form.add_error(None, "Invalid data")

        return render(request, "paste/edit.html", {'form': form})

    if request.method == 'GET':
        paste = get_object_or_404(Paste, hash=paste_hash)
        if paste.owner != request.user:
            raise PermissionDenied

        form = PasteEditForm(instance=paste)
        form.expiration_date = paste.expiration_date
        return render(request, "paste/edit.html", {'form': form})


def create(request):

    if request.method == 'GET':
        form = PasteCreateForm()
        return render(request, "paste/create.html", {'form': form})

    if request.method == 'POST':
        form = PasteCreateForm(request.POST)
        if form.is_valid():
            new_paste = form.save(commit=False)
            new_paste.owner = request.user
            new_paste.save()
            return redirect('detail', new_paste.hash)
        else:
            form.add_error(None, "Invalid data")
            return render(request, "paste/create.html", {'form': form})