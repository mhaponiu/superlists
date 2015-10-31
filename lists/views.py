from django.http.response import HttpResponse


def home_page(request):
    return HttpResponse('<html><title>Lista rzeczy do zrobienia</title></html>')

