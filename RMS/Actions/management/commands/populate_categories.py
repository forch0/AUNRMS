from django.core.management.base import BaseCommand
from Actions.models import Category, SubCategory

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        categories = {
            "Electrical": ["Bulb", "Socket", "Switch", "Lighting Fixture", "Air Condition"],
            "Woodwork": ["Door", "Window", "Bed","Matrass", "Wardrobe", "Reading Table"],
            "Plumbing": ["Toilet", "Sink", "Shower", "Drain", "Water Heater", "Water Pressure", "Leak Detection"],
        }

        for category_name, subcategories in categories.items():
            category, created = Category.objects.get_or_create(name=category_name)
            for subcategory_name in subcategories:
                SubCategory.objects.get_or_create(name=subcategory_name, category=category)

        self.stdout.write(self.style.SUCCESS('Categories and subcategories populated successfully.'))
