# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_world()
# to see the world.

import math
import random
import textwrap
import os
import colorama
from colorama import Fore, Style


class Player:
    def __init__(self, world):
        self.x = world.width // 2
        self.y = world.height - 1
        self.sprite = Fore.RED + " XX"

    def send_message(self, message):
        print(Fore.GREEN + "\n \n" + message + "\n \n")

    def move_up(self, world):

        reverse_grid = list(world.grid)  # make a copy of the list
        reverse_grid.reverse()

        if reverse_grid[self.y - 1][self.x].type == "wall":
            os.system('clear')
            world.print_world(self)
            self.send_message("do try not to run into walls...")
        else:
            os.system('clear')
            self.y -= 1
            world.print_world(self)

    def move_down(self, world):
        reverse_grid = list(world.grid)  # make a copy of the list
        reverse_grid.reverse()

        if reverse_grid[self.y + 1][self.x].type == "wall":
            os.system('clear')
            world.print_world(self)
            self.send_message("do try not to run into walls...")
        else:
            os.system('clear')
            self.y += 1
            world.print_world(self)

    def move_right(self, world):
        reverse_grid = list(world.grid)  # make a copy of the list
        reverse_grid.reverse()

        if reverse_grid[self.y][self.x + 1].type == "wall":
            os.system('clear')
            world.print_world(self)
            self.send_message("do try not to run into walls...")
        else:
            os.system('clear')
            self.x += 1
            world.print_world(self)

    def move_left(self, world):
        reverse_grid = list(world.grid)  # make a copy of the list
        reverse_grid.reverse()

        if reverse_grid[self.y][self.x - 1].type == "wall":
            os.system('clear')
            world.print_world(self)
            self.send_message("do try not to run into walls...", "RED")
        else:
            os.system('clear')
            self.x -= 1
            world.print_world(self)


class Tile:
    def __init__(self, x, y, room, type="free"):
        self.x = x
        self.y = y
        self.room = room
        self.type = type

    def build_wall(self):
        self.type = "wall"

    def build_door(self):
        self.type = "door"


class Room:
    def __init__(self, id, name, description, x_UL, y_UL, x_LR, y_LR):
        self.id = id
        self.name = name
        self.description = description
        self.width = 1
        self.height = 1
        self.x_UL = x_UL
        self.y_UL = y_UL
        self.x_LR = x_LR
        self.y_LR = y_LR

    def check_for_neighboring_rooms(self, world):
        # check to the north
        if self.y_UL - 1 >= 0:
            for x in range(self.x_UL, self.x_LR):
                if world[x][self.y_UL - 1] is not None:
                    return "neighbor to the north"
        # check to the south
        if self.y_LR + 1 < world.height:
            for x in range(self.x_UL, self.x_LR):
                if world[x][self.y_LR + 1] is not None:
                    return "neighbor to the south"
        # check to the east
        if self.x_LR + 1 < world.width:
            for y in range(self.y_UL, self.y_LR, -1):
                if world[self.x_LR + 1][y] is not None:
                    return "neighbor to the east"
        # check to the west
        if self.x_UL - 1 >= 0:
            for y in range(self.y_UL, self.y_LR, -1):
                if world[self.x_UL - 1][y] is not None:
                    return "neighbor to the west"


class World:
    def __init__(self, width=1, height=1):
        self.grid = None
        self.width = width
        self.height = height
        self.x_UL = 0
        self.y_UL = 0
        self.x_LR = self.width
        self.y_LR = -self.height

    def check_for_intersections(self, x_UL, y_UL, x_LR, y_LR):
        for y in range(y_UL, y_LR - 1, -1):
            for x in range(x_UL, x_LR):
                #print( "check: (" + str(x) + "," + str(y) + ")")
                if self.grid[y][x] is not None:
                    #print( "intersection" )
                    return True
        #print( "rect: %d, %d, %d, %d" % (x_UL, y_UL, x_LR, y_LR))
        #print( "no intersections" )
        return False

    def generate_rooms(self, size_x, size_y, num_rooms):

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y

        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        room_count = 1
        # initialize area of board left as the total area
        area_of_board_left = self.width * self.height
        while room_count < num_rooms:

            #print( "room count: " + str( room_count) )

            number_left = num_rooms - room_count
            max_length = int(math.sqrt(area_of_board_left - number_left) * 0.5)

            # print("left: %d / %d" % (number_left, area_of_board_left))

            # print( "max: %d" % (max_length,))

            # while loop

            width = 0
            height = 0
            while True:

                width = max(3, int(random.randint(3, max_length) * 1) - 1)
                #height = max( 1, int(random.randint( int(width * 0.5), min( int( width * 2 ), int(max_length) ) ) * 1) - 1 )
                height = max(3, int(random.randint(3, max_length) * 1) - 1)

                #print( "w: %d, h: %d" % (width, height))

                room_point_x = random.randint(0, self.width - width)
                #print("room_point_x: " + str(room_point_x))
                # room_point_y = random.randint(height - 1, self.height - 1)
                # changed this so that rooms can't spawn in first row
                room_point_y = random.randint(height, self.height - 1)
                #print("room_point_y: " + str(room_point_y))

                #print( "x: %d, y: %d" % (room_point_x, room_point_y) )

                if self.check_for_intersections(room_point_x, room_point_y, room_point_x + width, room_point_y - height) == False:
                    break

            # subtract room's area from running total
            area_of_board_left -= width * height

            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            #print( "w: %d, h: %d" % (width, height) )
            room = Room(room_count, "A Generic Room", "This is a generic room.",
                        room_point_x, room_point_y, room_point_x + width, room_point_y - height)
            for y in range(room_point_y, room_point_y - height, -1):
                for x in range(room_point_x, room_point_x + width):
                    #print( "place %d, %d" % (x, y) )
                    self.grid[y][x] = Tile(x, y, room)

          # add northern wall
            for x in range(room_point_x, room_point_x + width):
                self.grid[room_point_y][x].build_wall()
          # add southern wall
            for x in range(room_point_x, room_point_x + width):
                # print(str(x), str(y))
                self.grid[room_point_y - height + 1][x].build_wall()
          # add eastern wall
            for y in range(room_point_y, room_point_y - height, -1):
                self.grid[y][room_point_x + width - 1].build_wall()

          # add western wall

            for y in range(room_point_y, room_point_y - height, -1):
                self.grid[y][room_point_x].build_wall()

          # add northern door

            # get x position
            x_position = (room_point_x + room_point_x + width) // 2
            # get y position
            y_position = room_point_y

            self.grid[y_position][x_position].build_door()

          # add southern door

            # get x position
            x_position = (room_point_x + room_point_x + width) // 2
            # get y position
            y_position = room_point_y - height + 1

            self.grid[y_position][x_position].build_door()

            # Update iteration variables
            previous_room = room
            room_count += 1

        #print( "y loop: %d, %d" % (self.y_UL, self.y_LR - 1) )

        for y in range(self.y_UL, self.y_LR - 1, -1):

            #print( "x loop: %d, %d" % (self.x_UL, self.x_LR) )

            for x in range(self.x_UL, self.x_LR):
                empty_room = Room(0, "An Empty Space",
                                  "This is an empty space", x, y, x, y)
                #print( "check: (" + str(x) + "," + str(y) + ")")
                # print( "checking (%d, %d)" % (x,y) )
                if self.grid[y][x] is None:
                    self.grid[y][x] = Tile(x, y, empty_room)

    def print_world(self, player):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        out = Fore.BLUE + "# " * (((self.width * 3) // 2) + 1) + "#\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.

        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()

        for y in range(0, len(reverse_grid)):
            # for row in reverse_grid:
            out += Fore.BLUE + "#"
            row = reverse_grid[y]
            for x in range(0, len(row)):
                # for room in row:
                tile = row[x]
                room_id = tile.room.id
                if x == player.x and y == player.y:
                    out += player.sprite
                elif room_id == 0:
                    out += Style.RESET_ALL + "   "
                else:
                    if tile.type == "wall":
                        out += Style.RESET_ALL + " =="
                    elif tile.type == "door":
                        out += Fore.BLACK + " $$"
                    else:
                        out += Style.RESET_ALL + " %02d" % (room_id,)

            out += Fore.BLUE + " #\n"

        # Add bottom border
        out += "# " * (((self.width * 3) // 2) + 1) + "#\n"

        # Print string
        print(out)



num_rooms = 10
width = 20
height = 17
w = World(width, height)
j = Player(w)
# print(j.x, j.y, "j")
w.generate_rooms(width, height, num_rooms)
w.print_world(j)


# print(
#     f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")



def explore(player, world):
    user = 5
    while not user == 9:
        player.send_message("Welcome to my dungeon, brave explorer")
        user = int(input(Style.RESET_ALL +
                         "[1] up   [2] right   [3] down   [4] left      [9] quit   \n \n"))

        # user chooses up
        if user == 1:
            player.move_up(world)

        # user chooses right
        elif user == 2:
            player.move_right(world)

        # user chooses down
        elif user == 3:
            player.move_down(world)

        # user chooses left
        elif user == 4:
            player.move_left(world)

        elif user == 5:
            pass

        elif user == 9:
            pass

        else:
            print("Invalid selection. Please try again. \n \n")


explore(j, w)
