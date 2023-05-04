import datetime
from random import randint
from django.core.management import BaseCommand, CommandError
from users.models import CustomUser
from tasks.models import Task


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for user_id in options['user_id']:
            try:
                user = CustomUser.objects.get(pk=user_id)
            except CustomUser.DoesNotExist:
                raise CommandError(f'User {user_id} does not exist')

            for num in range(1, 100):
                year = 2023
                month = randint(1, 12)
                day = randint(10, 20)

                test_date = datetime.date(year, month, day)
                Task.objects.create(title=f'title{num}',
                                    description=f'description{num}',
                                    date=test_date,
                                    user=user
                                    )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created tasks')
        )
        