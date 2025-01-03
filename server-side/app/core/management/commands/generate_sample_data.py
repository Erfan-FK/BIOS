from django.core.management.base import BaseCommand
from core.models._User import User
from core.models._Tour import Tour
from core.models._Review import Review
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Generate sample data for the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing existing data...")

        # Delete data in reverse dependency order
        Review.objects.all().delete()
        Tour.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("Generating sample data...")

        # Create Users (automatically creates related Guide, Visitor, Advisor models)
        for i in range(1, 6):
            User.objects.create_user(
                email=f"guide{i:02d}@mail.com",
                password="123",
                name=f"Guide {i}",
                role="guide"
            )

        for i in range(1, 6):
            User.objects.create_user(
                email=f"visitor{i:02d}@mail.com",
                password="123",
                name=f"Visitor {i}",
                role="visitor"
            )

        for i in range(1, 3):
            User.objects.create_user(
                email=f"advisor{i:02d}@mail.com",
                password="123",
                name=f"Advisor {i}",
                role="advisor"
            )

        User.objects.create_user(
            email="secretary@mail.com",
            password="123",
            name="Secretary",
            role="secretary"
        )

        User.objects.create_user(
            email="director@mail.com",
            password="123",
            name="Director",
            role="director"
        )
        
        User.objects.create_user(
            email="coordinator@mail.com",
            password="123",
            name="Coordinator",
            role="coordinator"
        )

        # # Create Tours
        # visitors = User.objects.filter(role="visitor")
        # guides = User.objects.filter(role="guide")
        # tours = []
        # for i in range(1, 6):
        #     tour = Tour.objects.create(
        #         date=datetime.now().date() + timedelta(days=i),
        #         slot="09.00 AM",  # Matches the first element of TIME_SLOTS
        #         visitor=visitors[i % len(visitors)].visitor_profile,
        #         status="ASSIGNED"
        #     )
        #     tour.guides.set([guides[i % len(guides)].guide_profile])
        #     tours.append(tour)

        # # Create Reviews
        # for i, tour in enumerate(tours[:3]):  # Add reviews for the first 3 tours
        #     review = Review.objects.create(
        #         review=f"Great tour experience {i + 1}",
        #         reviewRating=4.5 - i * 0.5,
        #         timestamp=datetime.now(),
        #         reviewer=tour.visitor
        #     )
        #     tour.review = review
        #     tour.save()

        self.stdout.write(self.style.SUCCESS("Sample data generated successfully."))
