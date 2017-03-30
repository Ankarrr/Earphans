from django.test import TestCase
from django.utils import timezone
from .models import Question, Earphone
from django.urls import reverse

import datetime

class ListEarphonesViewTests(TestCase):
    def test_list_earphones_with_no_earphones(self):
        """
        If no earphones exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('firstapp:earphones'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No earphones are available.")
        self.assertQuerysetEqual(response.context['object_list'], [])

class SearchForEarphonesTests(TestCase):
    def test_search_for_earphones_with_no_earphones_searched(self):
        """
        If no earphones are searched, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('firstapp:search-for-earphones'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No earphones are available.")
        self.assertQuerysetEqual(response.context['earphones_list'], [])

    def test_search_for_earphones_with_name(self):
        create_earphone('Test earphone', 1000, 'Bose', 'Earbud', [])
        create_earphone('test earphone', 1000, 'Bose', 'Earbud', [])
        create_earphone('XXX earphone', 1000, 'Bose', 'Earbud', [])
        response = self.client.get(reverse('firstapp:search-for-earphones'), {'query-string': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['earphones_list'],
            ['<Earphone: Test earphone>', '<Earphone: test earphone>'],
            ordered=False
        )

    def test_search_for_earphones_with_type(self):
        create_earphone('One earphone', 1000, 'Bose', 'Earbud', [])
        create_earphone('Second earphone', 1000, 'Bose', 'Earbud', [])
        create_earphone('Third earphone', 1000, 'Bose', 'On-Ear', [])
        response = self.client.get(reverse('firstapp:search-for-earphones'), {'earphone-type': 'Earbud'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['earphones_list'],
            ['<Earphone: One earphone>', '<Earphone: Second earphone>'],
            ordered=False
        )

    def test_search_for_earphones_with_features(self):
        create_earphone('One earphone', 1000, 'Bose', 'Earbud', ['Wireless'])
        create_earphone('Second earphone', 1000, 'Bose', 'Earbud', ['Microphone'])
        create_earphone('Third earphone', 1000, 'Bose', 'On-Ear', ['Wireless', 'Microphone'])
        response = self.client.get(
            reverse('firstapp:search-for-earphones'),
            {'earphone-feature-wireless': 'Wireless', 'earphone-feature-microphone': 'Microphone'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['earphones_list'],
            ['<Earphone: Third earphone>'],
            ordered=False
        )

def create_earphone(name, price, brand, earphone_type, features):
    return Earphone.objects.create(
        earphone_name=name,
        price=price,
        brand_name=brand,
        earphone_type=earphone_type,
        pub_date=timezone.now(),
        earphone_features=features,
        earphone_image=False
    )

# ---------------------
# codes for experiments
# ---------------------

class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('firstapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No firstapp are available.")
        self.assertQuerysetEqual(response.context['object_list'], [])
    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('firstapp:index'))
        self.assertQuerysetEqual(
            response.context['object_list'],
            ['<Question: Past question.>']
        )
