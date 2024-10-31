from django.core.management.base import BaseCommand
from website.models import MasseurPage, MasseurIndexPage
from wagtail.images.models import Image
from django.utils import timezone
from django.db import transaction
import random

class Command(BaseCommand):
    help = "Creates 7 sample MasseurPage entries under an existing MasseurIndexPage"

    def handle(self, *args, **options):
        # Check if MasseurIndexPage exists
        index_page = MasseurIndexPage.objects.first()
        if not index_page:
            self.stdout.write(self.style.ERROR("No MasseurIndexPage found. Please create one in the Wagtail admin."))
            return

        # Get an existing image for the image gallery
        sample_image = Image.objects.first()
        if not sample_image:
            self.stdout.write(self.style.ERROR("No image found in Wagtail. Please upload an image first."))
            return

        # Predefined list of seven Turkish female names
        masseur_names = [
            "Ayşe Yıldız",
            "Fatma Kara",
            "Elif Demir",
            "Seda Çelik",
            "Gül Özkan",
            "Zeynep Aksoy",
            "Nur Aydın"
        ]

        # Lists for random assignment
        experience_years_options = ["2", "3", "4", "5", "6"]
        descriptions = [
            "Experienced therapist with a focus on relaxation techniques.",
            "Skilled in deep tissue and sports massage.",
            "Certified in various massage therapies for wellness.",
            "Renowned for her attention to detail and client care.",
            "Passionate about holistic health and healing."
        ]
        locations = [
            "Istanbul, Turkey",
            "Ankara, Turkey",
            "Izmir, Turkey",
            "Bursa, Turkey",
            "Antalya, Turkey"
        ]

        # Wrap in a transaction to ensure atomic creation
        with transaction.atomic():
            for full_name in masseur_names:
                first_name, last_name = full_name.split()  # Split full name into first and last

                # Construct the unique slug
                slug = f"{first_name.lower()}-{random.randint(1, 99)}-{last_name.lower()}"

                # Create the MasseurPage
                masseur_page = MasseurPage(
                    title=full_name,
                    slug=slug,
                    name=full_name,
                    experience_years=random.choice(experience_years_options),
                    description=random.choice(descriptions),
                    phone="5357980393",
                    whatsapp="5357980393",
                    user_name=full_name,
                    membership_date="2023-05-09",
                    user_profile_url="https://example.com/profile",
                    location=random.choice(locations),
                    first_published_at=timezone.now(),
                    last_published_at=timezone.now(),
                    show_in_menus=True,
                )

                # Add page as a child of the index page and publish it
                index_page.add_child(instance=masseur_page)
                masseur_page.save_revision().publish()

                # Assign the same sample image to the image_gallery StreamField
                masseur_page.image_gallery = [
                    ("image", sample_image),
                ]
                masseur_page.save_revision().publish()

            self.stdout.write(self.style.SUCCESS("7 sample MasseurPage entries created and published."))
