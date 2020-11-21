from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult
from .tasks import compile_and_run


def get_compile_form(request):
    if request.method == "POST":
        return render(request, 'compiler/compile_form.html', {'code': request.POST.get('code')})

    return render(request, 'compiler/compile_form.html')

@csrf_exempt
def compile_api(request):
    if request.method == 'POST':
        result = compile_and_run.delay(request.POST.get('text'), request.POST.get('stdin'))
        data = {'task_id': result.id}

        return JsonResponse(data)

    if request.method == 'GET':
        task_id = request.GET.get('task_id')
        res = AsyncResult(task_id)

        result = {}

        result.update({'status': res.status})

        if res.status == 'SUCCESS':
            result.update(res.result)

        return JsonResponse(result)
