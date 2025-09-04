from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone
from hangarin.models import Task, SubTask, Note, Category, Priority


class Command(BaseCommand):
    help = 'Create initial data for Hangarin app'

    def handle(self, *args, **kwargs):
        self.create_tasks(20)

    def create_tasks(self, count):
        fake = Faker()
        categories = list(Category.objects.all())
        priorities = list(Priority.objects.all())

        for _ in range(count):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                priority=random.choice(priorities),
                category=random.choice(categories),
            )

            for _ in range(2):
                SubTask.objects.create(
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                    parent_task=task,
                )

            for _ in range(2):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )

        self.stdout.write(self.style.SUCCESS(
            f'{count} tasks with subtasks and notes created successfully!'
        ))
