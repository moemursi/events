from django.test import TestCase


class TestFilterSearchSortEvents(TestCase):

    def setUp(self):
        User.objects.create(email='testuser@test.com', password='4epape?Huf+V')

        # Create a new event with NTNUI as host
        event = Event.objects.create(start_date=date.today(), end_date=date.today(),
                                     priority=True, is_host_ntnui=True)

        # add norwegian and english description to the name and the description
        EventDescription.objects.create(name='Norsk', description_text='Norsk beskrivelse', language='nb', event=event)
        EventDescription.objects.create(name='Engelsk', description_text='Engelsk beskrivelse', language='en',
                                        event=event)

        # Create a second event with a group
        event = Event.objects.create(start_date=date.today(), end_date=date.today(),
                                     priority=True)
        # Add a sports group
        event.sports_groups.add(SportsGroup.objects.create(name='Test Group', description='this is a test group'))

        # add norwegian and english description to the name and the description
        EventDescription.objects.create(name='test norsk', description_text='test norsk', language='nb', event=event)
        EventDescription.objects.create(name='test engelsk', description_text='test engelsk', language='en',
                                        event=event)

    def test_filtering(self):
        c = Client()
        # login
        c.login(email='testuser@test.com', password='4epape?Huf+V')