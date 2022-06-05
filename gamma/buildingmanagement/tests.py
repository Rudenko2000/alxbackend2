from django.test import TestCase
from .models import Room

# Create your tests here.

class RoomTestCase(TestCase):
    def test_str(self):
        room=Room(name="sala", people_count =0,max_people_count =10,image =None)
        self.assertEqual(str(room),"sala")



class PeopleTrackingTestCase(TestCase):
    fixtures = ['example']

    def test_mooving_people(self):
        room1=Room.objects.get(name='sala1')
        room2=Room.objects.get(name='sala2')



        room1.move_people_to(room2,2)

        room1 = Room.objects.get(name='sala1')
        room2 = Room.objects.get(name='sala2')

        self.assertEqual(room1.people_count,0)
        self.assertEqual(room2.people_count,2)



