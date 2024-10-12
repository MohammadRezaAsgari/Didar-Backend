from datetime import datetime, timedelta

import factory
from faker import Faker

from schedule.models import Schedule
from users.factories import InstructorFactory

fake = Faker()


class ScheduleFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("word")
    instructor = factory.SubFactory(InstructorFactory)
    day_of_week = factory.Iterator(
        [
            Schedule.DAY_SATURDAY,
            Schedule.DAY_SUNDAY,
            Schedule.DAY_MONDAY,
            Schedule.DAY_TUESDAY,
            Schedule.DAY_WEDNESDAY,
            Schedule.DAY_THURSDAY,
        ]
    )
    start_time = factory.Faker("time_object")
    end_time = factory.Faker("time_object")

    @factory.lazy_attribute
    def end_time(self):
        # Ensures end_time is always after start_time
        start = self.start_time
        end = (datetime.combine(datetime.today(), start) + timedelta(hours=1)).time()
        return end

    class Meta:
        model = Schedule
