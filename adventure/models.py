import inspect
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
import json


class World:

    def __init__(self):
        self.rooms = {}

    def roomFunc(self, roomGraph):
        newGraph = {}
        for key in roomGraph.keys():
            # Convert non-int keys to int
            newId = int(key)
            newGraph[newId] = {}
            # Add views
            if "views" not in roomGraph[key].keys():
                newGraph[newId]['views'] = {}
            newGraph[newId].update(roomGraph[key])
        roomGraph = newGraph

        for r in roomGraph.keys():
            current = roomGraph[r]
            self.rooms[r] = Room(r,
                                 current['room_id'], current['title'], current['description'], json.dumps(current['views']))
            self.rooms[r].save()

        for rm in self.rooms.keys():
            crm = roomGraph[rm]
            if 'n' in crm['exits']:
                self.rooms[rm].connectRooms(
                    self.rooms[int(crm['exits']['n'])], 'n')
            if 's' in crm['exits']:
                self.rooms[rm].connectRooms(
                    self.rooms[int(crm['exits']['s'])], 's')
            if 'w' in crm['exits']:
                self.rooms[rm].connectRooms(
                    self.rooms[int(crm['exits']['w'])], 'w')
            if 'e' in crm['exits']:
                self.rooms[rm].connectRooms(
                    self.rooms[int(crm['exits']['e'])], 'e')


class Room(models.Model):
    room_id = models.IntegerField(default=0)
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.TextField(
        default="DEFAULT DESCRIPTION")
    views = models.TextField(default='')
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)

    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
