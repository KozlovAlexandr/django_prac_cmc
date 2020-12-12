from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.db import IntegrityError
from django.views import View
from django.shortcuts import get_object_or_404
from .models import ShortUrl
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.core.paginator import Paginator


from .forms import UrlCreateForm, UrlEditForm


class CreateView(View):

    def get(self, request):

        form = UrlCreateForm()
        return render(request, "shortener/create.html", {'form': form})

    def post(self, request):

        form = UrlCreateForm(request.POST)

        if form.is_valid():

            new_short_url = form.save(commit=False)
            if request.user.is_authenticated:
                new_short_url.owner = request.user
            try:
                new_short_url.save()
                short_url_str = request.build_absolute_uri(reverse('shortener:my_redirect',
                                                           args=[new_short_url.hash]))
                return render(request, "shortener/success_created.html", {'short_url': short_url_str})

            except IntegrityError as e:
                pass

        return render(request, "shortener/create.html", {'form': form})

@login_required(login_url=reverse_lazy('common:login'))
def show_my_page(request, page):

    unexpired = ShortUrl.unexpired_objects.filter(owner=request.user).order_by('-creation_date')

    p = Paginator(unexpired, 20)
    page_obj = p.page(page)

    context = {'url_list': page_obj.object_list, 'page_obj': page_obj}

    return render(request, 'shortener/my_urls.html', context)




@login_required(login_url=reverse_lazy('common:login'))
def show_my(request):

    return redirect('shortener:show_page', page=1)




def my_redirect(request, url_hash):

    short_url = get_object_or_404(ShortUrl.unexpired_objects, hash=url_hash)

    short_url.clicked += 1
    short_url.save()

    return redirect(short_url.original_url)


@login_required(login_url=reverse_lazy('common:login'))
def edit(request, url_hash):

    url = get_object_or_404(ShortUrl, hash=url_hash, owner=request.user)

    if request.method == 'POST':
        if request.POST.get('_method', '').lower() == 'delete':
            url.delete()
            return redirect('shortener:show')

        form = UrlEditForm(request.POST, instance=url)
        if form.is_valid():
            try:
                form.save()
                return redirect('shortener:show')

            except IntegrityError:
                pass

        return render(request, "shortener/edit.html", {'form': form})

    if request.method == 'GET':

        form = UrlEditForm(instance=url)
        return render(request, "shortener/edit.html", {'form': form})