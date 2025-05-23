from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, date
from .models import Image, Category

class GalleryViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Nature")

        # зображення за останній місяць
        self.recent_image = Image.objects.create(
            title="Recent",
            image="gallery_images/recent.jpg",
            created_date=date.today(),
            age_limit=0
        )
        self.recent_image.categories.add(self.category)

        # старе зображення
        self.old_image = Image.objects.create(
            title="Old",
            image="gallery_images/old.jpg",
            created_date=date.today() - timedelta(days=40),
            age_limit=0
        )
        self.old_image.categories.add(self.category)

    def test_gallery_view_status_code(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_gallery_view_context_contains_only_recent_images(self):
        response = self.client.get(reverse('main'))
        images = response.context['images']
        self.assertIn(self.recent_image, images)
        self.assertNotIn(self.old_image, images)

    def test_gallery_view_template_used(self):
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, 'gallery.html')


class ImageDetailViewTests(TestCase):
    def setUp(self):
        self.image = Image.objects.create(
            title="Detail Test",
            image="gallery_images/detail.jpg",
            created_date=date.today(),
            age_limit=0
        )

    def test_image_detail_view_status_code(self):
        response = self.client.get(reverse('image_detail', kwargs={'pk': self.image.pk}))
        self.assertEqual(response.status_code, 200)

    def test_image_detail_view_context_contains_correct_image(self):
        response = self.client.get(reverse('image_detail', kwargs={'pk': self.image.pk}))
        self.assertEqual(response.context['image'], self.image)

    def test_image_detail_template_used(self):
        response = self.client.get(reverse('image_detail', kwargs={'pk': self.image.pk}))
        self.assertTemplateUsed(response, 'image_detail.html')

    def test_image_detail_404_if_not_found(self):
        response = self.client.get(reverse('image_detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)
