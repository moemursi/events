from datetime import date

from accounts.models import User
from django.test import Client, TestCase
from django.urls import reverse
from events.models import (Category, CategoryDescription, Event,
                           EventDescription, SubEvent, SubEventDescription)
from groups.models import Board, Membership, SportsGroup
from hs.models import MainBoard, MainBoardMembership


class TestLoadEvents(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@test.com', password='4epape?Huf+V', customer_number=1)

        # Create a new event with NTNUI as host
        self.event = Event.objects.create(start_date=date.today(), end_date=date.today(),
                                          priority=True, is_host_ntnui=True)

        # add norwegian and english description to the name and the description
        EventDescription.objects.create(name='Norsk', description_text='Norsk beskrivelse', language='nb',
                                        event=self.event)
        EventDescription.objects.create(name='Engelsk', description_text='Engelsk beskrivelse', language='en',
                                        event=self.event)

        category = Category.objects.create(event=self.event)
        CategoryDescription.objects.create(name="test", category=category, language='en')
        CategoryDescription.objects.create(name="test", category=category, language='nb')

        # Create a new event with NTNUI as host
        sub_event = SubEvent.objects.create(start_date=date.today(), end_date=date.today(), category=category)

        # add norwegian and english description to the name and the description
        SubEventDescription.objects.create(name='Norsk', language='nb', sub_event=sub_event)
        SubEventDescription.objects.create(name='Engelsk', language='en',
                                           sub_event=sub_event)

        # create sports group/main board
        self.swimminggroup = SportsGroup.objects.create(name='Swimming', slug='slug',
                                                        description='Swimming events and tournaments',
                                                        )
        self.swimmingboard = Board.objects.create(president=self.user, vice_president=self.user,
                                                  cashier=self.user, sports_group=self.swimminggroup)
        self.swimminggroup.active_board = self.swimmingboard
        self.swimminggroup.save()

        # put user into mainboard
        Membership.objects.create(person=self.user, group=self.swimminggroup)

        hs = MainBoard.objects.create(name="super geir", slug="super-geir")
        MainBoardMembership.objects.create(person=self.user, role="president", board=hs)

        # Create a second event with a group
        event = Event.objects.create(start_date=date.today(), end_date=date.today(),
                                     priority=True)
        # Add a sports group
        event.sports_groups.add(SportsGroup.objects.create(name='Test Group', description='this is a test group'))

        # add norwegian and english description to the name and the description
        EventDescription.objects.create(name='test norsk', description_text='test norsk', language='nb', event=event)
        EventDescription.objects.create(name='test engelsk', description_text='test engelsk', language='en',
                                        event=event)

        self.client_signed_in = Client()
        # login
        self.client_signed_in.login(email='testuser@test.com', password='4epape?Huf+V')

        self.client_anonymous = Client()

    def test_loading_main_event_page_user(self):
        """Checks that a logged in user can load the main event page"""
        request = self.client_signed_in.get(reverse('get_main_page'))
        self.assertEquals(request.status_code, 200)

    def test_loading_main_event_page_guest(self):
        """Checks that a guest can load the main event page"""
        request = self.client_anonymous.get(reverse('get_main_page'))
        self.assertEquals(request.status_code, 200)

    def test_loading_create_event_page_guest(self):
        """Tests that a guest can not create a new event"""
        request = self.client_anonymous.get(reverse('create_event_page'))
        self.assertEquals(request.status_code, 302)

    def test_loading_create_event_page_user(self):
        """Checks that a user may create a new event"""
        request = self.client_signed_in.get(reverse('create_event_page'))
        self.assertEquals(request.status_code, 200)

    def test_loading_event_details_page_user(self):
        """Checks that a user may see event details"""
        request = self.client_signed_in.get('/events/' + str(self.event.id) + '/', follow=True)
        self.assertEquals(request.status_code, 200)

    def test_loading_event_details_page_user(self):
        """Checks that a user may see event details"""
        request = self.client_anonymous.get('/events/' + str(self.event.id) + '/', follow=True)
        self.assertEquals(request.status_code, 200)
