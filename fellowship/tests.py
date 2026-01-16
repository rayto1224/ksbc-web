from django.test import TestCase, Client
from django.urls import reverse
from .models import FellowshipEvent
from datetime import datetime

class FellowshipTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.event = FellowshipEvent.objects.create(
            title="測試團契",
            date_text="星期五",
            time_text="7:30 PM",
            location="教會",
            description="這是一個測試活動"
        )

    def test_fellowship_page_status_code(self):
        response = self.client.get(reverse("fellowship:fellowship"))
        self.assertEqual(response.status_code, 200)

    def test_fellowship_page_template(self):
        response = self.client.get(reverse("fellowship:fellowship"))
        self.assertTemplateUsed(response, "fellowship/fellowship.html")

    def test_fellowship_page_contains_event(self):
        response = self.client.get(reverse("fellowship:fellowship"))
        self.assertContains(response, "測試團契")
        self.assertContains(response, "這是一個測試活動")
