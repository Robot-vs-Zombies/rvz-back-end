# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

import math
import random


class Room:
    def __init__(self, id, name, description, x_UL, y_UL, x_LR, y_LR):
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

    # def __repr__(self):
    #     if self.e_to is not None:
    #         return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
    #     return f"({self.x}, {self.y})"

    # def connect_rooms(self, connecting_room, direction):
    #     '''
    #     Connect two rooms in the given n/s/e/w direction
    #     '''
    #     reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
    #     reverse_dir = reverse_dirs[direction]
    #     setattr(self, f"{direction}_to", connecting_room)
    #     setattr(connecting_room, f"{reverse_dir}_to", self)

    # def get_room_in_direction(self, direction):
    #     '''
    #     Connect two rooms in the given n/s/e/w direction
    #     '''
    #     return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 1
        self.height = 1

    def check_for_intersections(self, x_UL, y_UL, x_LR, y_LR):
        for y in range(y_UL, y_LR - 1, -1):
            for x in range(x_UL, x_LR):
                #print( "check: (" + str(x) + "," + str(y) + ")")
                if self.grid[y][x] is not None:
                    print("intersection")
                    return True
        print("rect: %d, %d, %d, %d" % (x_UL, y_UL, x_LR, y_LR))
        print("no intersections")
        return False

    def generate_rooms(self, size_x, size_y, num_rooms):

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        room_count = 0
        # initialize area of board left as the total area
        area_of_board_left = self.width * self.height
        while room_count < num_rooms:

            print("room count: " + str(room_count))

            number_left = num_rooms - room_count
            max_length = math.sqrt(area_of_board_left - number_left)

            #print( "width: " + str(width))
            #print( "height: " + str(height))

            # while loop

            width = 0
            height = 0
            while True:

                width = max(1, int(random.randint(1, int(max_length)) * 0.25))
                height = max(1, int(random.randint(1, int(max_length)) * 0.25))

                room_point_x = random.randint(0, self.width - width)
                #print("room_point_x: " + str(room_point_x))
                room_point_y = random.randint(height, self.height - height)
                #print("room_point_y: " + str(room_point_y))

                if self.check_for_intersections(room_point_x, room_point_y, room_point_x + width, room_point_y - height) == False:
                    break

            # subtract room's area from running total
            area_of_board_left -= width * height

            room = Room(room_count, "A Generic Room",
                        "This is a generic room.", room_point_x, room_point_y, room_point_x + width, room_point_y - height)
            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            print("w: %d, h: %d" % (width, height))
            for y in range(room_point_y, room_point_y - height, -1):
                for x in range(room_point_x, room_point_x + width):
                    print("place %d, %d" % (x, y))
                    self.grid[y][x] = room

            # self.grid[y][x] = room

            # # Connect the new room to the previous room
            # if previous_room is not None:
            #     previous_room.connect_rooms(room, room_direction)

            # Update iteration variables
            previous_room = room
            room_count += 1

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        out = "# " * ((3 + self.width * 3) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.

        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            out += "# "
            for room in row:
                if room is not None:
                    out += " %02d" % (room.id,)
                    #out += " " + str(room.id) + " "
                else:
                    out += "   "
            out += " #\n"

        # Add bottom border
        out += "# " * ((3 + self.width * 3) // 2) + "\n"

        # Print string
        print(out)


w = World()
num_rooms = 44
width = 15
height = 30
w.generate_rooms(width, height, num_rooms)
w.print_rooms()


print(
    f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
