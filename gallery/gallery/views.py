from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Image, Category

def gallery_view(request):
    today = timezone.now().date()
    one_month_ago = today - timedelta(days=30)
    recent_images = Image.objects.filter(created_date__gte=one_month_ago)
    return render(request, 'gallery.html', {'images': recent_images})

def image_detail(request, pk):
    pass