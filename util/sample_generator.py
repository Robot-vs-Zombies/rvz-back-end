# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

import math
import random


class Player:
    def __init__(self, world):
        self.x = world.width // 2
        self.y = 0
        self.sprite = " X "


class Room:
    def __init__(self, id, name, description, x_UL, y_UL, x_LR, y_LR, x_coordinate, y_coordinate):
        self.id = id
        self.name = name
        self.description = description
        self.width = 1
        self.height = 1
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x_UL = x_UL
        self.y_UL = y_UL
        self.x_LR = x_LR
        self.y_LR = y_LR
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

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

                width = max(1, int(random.randint(1, max_length) * 1) - 1)
                #height = max( 1, int(random.randint( int(width * 0.5), min( int( width * 2 ), int(max_length) ) ) * 1) - 1 )
                height = max(1, int(random.randint(1, max_length) * 1) - 1)

                #print( "w: %d, h: %d" % (width, height))

                room_point_x = random.randint(0, self.width - width)
                #print("room_point_x: " + str(room_point_x))
                room_point_y = random.randint(height - 1, self.height - 1)
                #print("room_point_y: " + str(room_point_y))

                #print( "x: %d, y: %d" % (room_point_x, room_point_y) )

                if self.check_for_intersections(room_point_x, room_point_y, room_point_x + width, room_point_y - height) == False:
                    break

            # subtract room's area from running total
            area_of_board_left -= width * height

            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            #print( "w: %d, h: %d" % (width, height) )
            for y in range(room_point_y, room_point_y - height, -1):
                for x in range(room_point_x, room_point_x + width):
                    room = Room(room_count, "A Generic Room", "This is a generic room.",
                                room_point_x, room_point_y, room_point_x + width, room_point_y - height, x, y)
                    #print( "place %d, %d" % (x, y) )
                    self.grid[y][x] = room

            # self.grid[y][x] = room

            # # Connect the new room to the previous room
            # if previous_room is not None:
            #     previous_room.connect_rooms(room, room_direction)

            # Update iteration variables
            previous_room = room
            room_count += 1

        for y in range(self.y_UL, self.y_LR - 1, -1):
            for x in range(self.x_UL, self.x_LR):
                empty_room = Room(0, "An Empty Space",
                                  "This is an empty space", x, y, x, y, x, y)
                #print( "check: (" + str(x) + "," + str(y) + ")")
                if self.grid[y][x] is None:
                    self.grid[y][x] = empty_room

    def print_rooms(self, player):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        out = "# " * (((self.width * 3) // 2) + 1) + "#\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.

        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()

        for row in reverse_grid:
            out += "#"
            for room in row:

                if room is not None:
                    if room.id != 0:
                        if room.x_coordinate == player.x and room.y_coordinate == player.y:
                            out += player.sprite
                        else:
                            out += " %02d" % (room.id,)
                    else:
                        if room.x_UL == player.x and room.y_UL == player.y:
                            out += player.sprite
                        else:
                            out += "   "
                else:
                    out += "   "
            out += " #\n"

        # Add bottom border
        out += "# " * (((self.width * 3) // 2) + 1) + "#\n"

        # Print string
        print(out)

    def draw_sprite(self, player):
        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()

        # for row in reverse_grid:
        #     for room in row:
        #         if player.x :
        #             out += " %02d" % (room.id,)
        #             #out += " " + str(room.id) + " "
        #         else:
        #             out += "   "
        #     out += " #\n"


num_rooms = 10
width = 20
height = 17
w = World(width, height)
j = Player(w)
# print(j.x, j.y, "j")
w.generate_rooms(width, height, num_rooms)
w.print_rooms(j)


print(
    f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
