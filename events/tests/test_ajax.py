from django.test import TestCase
from django.test import Client
from django.urls import reverse
from events import create_event
from django.utils import translation

from events.models import Event, EventDescription
from groups.models import SportsGroup
from datetime import date
from accounts.models import User


class TestLoadEvents(TestCase):

    def setUp(self):

        # Create dummy user
        User.objects.create(email='testuser@test.com', password='4epape?Huf+V')

        # Create a new event with NTNUI as host
        event = Event.objects.create(start_date= date.today(), end_date= date.today(),
                                     priority=True, is_host_ntnui=True)

        # add norwegian and english description to the name and the description
        EventDescription.objects.create(name='Norsk', description_text='Norsk beskrivelse', language='nb', event=event)
        EventDescription.objects.create(name='Engelsk', description_text='Engelsk beskrivelse', language='en', event=event)

    def test_loading_events(self):
        c = Client()

        # login
        c.login(email='testuser@test.com', password='4epape?Huf+V')

        response = c.get(reverse('get_events'), follow=True)
        self.assertEquals(response.status_code, 200)

    def test_create_events(self):
        c = Client()

        # login
        c.login(email='testuser@test.com', password='4epape?Huf+V')

        response = c.post(reverse('create_event'),{'name_en': 'engelsk navn',
                                                   'name_no': 'norsk navn',
                                                   'description_text_en': 'engelsk beskrivelse',
                                                   'description_text_no': 'norsk beskrivelse',
                                                   'start_date': date.today(),
                                                   'end_date': date.today(),
                                                   'priority': 'false',
                                                   'host': 'NTNUI'
                                                   }, follow=True)

    def test_create_event_with_no_description(self):
        c = Client()

        # login
        c.login(email='testuser@test.com', password='4epape?Huf+V')

        response = c.post(reverse('create_event'), {'name_en': 'engelsk navn',
                                                    'name_no': 'norsk navn',
                                                    'description_text_en': '',
                                                    'description_text_no': 'norsk beskrivelse',
                                                    'start_date': date.today(),
                                                    'end_date': date.today(),
                                                    'priority': 'false',
                                                    'host': 'NTNUI'
                                                    }, follow=True)

        return self.assertEqual(
            create_event.event_has_description_and_name(response.get('description_text_en'), response.get('name_en')),
            (False, 'Event must have description'))