from django.http import HttpResponse
from django.shortcuts import  redirect

def redirect_blog(request):
    return redirect('posts_list_url', permanent=True) # чтобы не временный 301, а посто-ый 302


