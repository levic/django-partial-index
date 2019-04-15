"""
Tests for actual use of the indexes after creating models with them.
"""
import datetime

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from testapp.forms import RoomBookingAllFieldsForm, RoomBookingChildAllFieldsForm, RoomBookingNoConditionFieldForm, RoomBookingJustRoomForm, RoomBookingTextForm
from testapp.models import User, Room, RoomBookingQ, RoomBookingQChild

'''
class OnlyQTestCase(TestCase):
    def test_text_condition_improperlyconfigured(self):
        form = RoomBookingTextForm(data={'user': 1, 'room': 1})
        with self.assertRaises(ImproperlyConfigured):
            form.is_valid()
'''

class FormTestCase(object):
    """Base class for form tests.
    """
    formclass = None
    conflict_error = 'RoomBookingQ with the same values for room, user already exists.'

    def setUp(self):
        self.user1 = User.objects.create(name='User1')
        self.user2 = User.objects.create(name='User2')
        self.room1 = Room.objects.create(name='Room1')
        self.room2 = Room.objects.create(name='Room2')
        self.booking_child1 = RoomBookingQChild.objects.create(user=self.user1, room=self.room1)
        self.booking_child2 = RoomBookingQChild.objects.create(user=self.user1, room=self.room2)
        self.booking1 = self.booking_child1.roombookingq_ptr
        self.booking2 = self.booking_child2.roombookingq_ptr

    def test_add_duplicate_invalid(self):
        print(self.formclass.__name__)
        if self.formclass != RoomBookingJustRoomForm:
            form = self.formclass(data={'user': self.user1.id, 'room': self.room1.id})
            self.assertFalse(form.is_valid(), 'Form errors: %s' % form.errors)
            self.assertIn(self.conflict_error, form.errors['__all__'])
        else:
            pass  # Skipped - JustRoomForm only works for modifications.
'''
    def test_add_duplicate_when_deleted_valid(self):
        if self.formclass != RoomBookingJustRoomForm:
            self.booking1.deleted_at = datetime.datetime.utcnow()
            self.booking1.save()

            form = self.formclass(data={'user': self.user1.id, 'room': self.room1.id})
            self.assertTrue(form.is_valid(), 'Form errors: %s' % form.errors)
            self.assertFalse(form.errors)
        else:
            pass  # Skipped - JustRoomForm only works for modifications.

    def test_add_non_duplicate_valid(self):
        if self.formclass != RoomBookingJustRoomForm:
            form = self.formclass(data={'user': self.user2.id, 'room': self.room1.id})
            self.assertTrue(form.is_valid(), 'Form errors: %s' % form.errors)
            self.assertFalse(form.errors)
        else:
            pass  # Skipped - JustRoomForm only works for modifications.

    def test_modify_existing_valid(self):
        form = self.formclass(data={'user': self.user1.id, 'room': self.room1.id}, instance=self.booking1)
        self.assertTrue(form.is_valid(), 'Form errors: %s' % form.errors)
        self.assertFalse(form.errors)

    def test_modify_another_to_be_duplicate_invalid(self):
        form = self.formclass(data={'user': self.user1.id, 'room': self.room1.id}, instance=self.booking2)
        self.assertFalse(form.is_valid(), 'Form errors: %s' % form.errors)
        self.assertIn(self.conflict_error, form.errors['__all__'])

    def test_modify_another_to_be_duplicate_when_deleted_valid(self):
        self.booking1.deleted_at = datetime.datetime.utcnow()
        self.booking1.save()

        form = self.formclass(data={'user': self.user1.id, 'room': self.room1.id}, instance=self.booking2)
        self.assertTrue(form.is_valid(), 'Form errors: %s' % form.errors)
        self.assertFalse(form.errors)
'''

class AllFieldsFormTest(FormTestCase, TestCase):
    """Test that partial unique validation on a ModelForm works when all fields are present on the form."""
    formclass = RoomBookingAllFieldsForm


class AllFieldsChildFormTest(FormTestCase, TestCase):
    """Test that partial unique validation on a ModelForm works for models using multi-table inheritance."""
    formclass = RoomBookingChildAllFieldsForm


#
# class NoConditionFieldFormTest(FormTestCase, TestCase):
#     """Test that partial unique validation on a ModelForm works when all index fields, but not the condition field are present on the form."""
#     formclass = RoomBookingNoConditionFieldForm
#
#
# class SingleFieldFormTest(FormTestCase, TestCase):
#     """Test that partial unique validation on a ModelForm works when not all unique fields are present on the form.
#
#     These have to be provided from an existing instance.
#     """
#     formclass = RoomBookingJustRoomForm
