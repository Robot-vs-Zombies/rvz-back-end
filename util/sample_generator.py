# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

import math
import random


class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.width = 1
        self.height = 1
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x  # upper left corner of room
        self.y = y

    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"

    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)

    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 1
        self.height = 1

    def check_for_intersections(self, x_UL, y_UL, x_LR, y_LR):
        for y in range(y_UL, y_LR):
            for x in range(x_UL, x_LR):
                #print( "check: (" + str(x) + "," + str(y) + ")")
                if self.grid[y][x] is not None:
                    #print( "intersection" )
                    return True
        #print( "no intersections" )
        return False

    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west

        # While there are rooms to be created...
        previous_room = None

        # initialize area of board left as the total area
        area_of_board_left = self.width * self.height
        while room_count < num_rooms:
            number_left = num_rooms - room_count
            max_length = math.sqrt(area_of_board_left - number_left)

            #print( "width: " + str(width))
            #print( "height: " + str(height))

            # while loop

            while True:

                width = int(random.randint(0, int(max_length)) * 0.25)  # - 1
                height = int(random.randint(0, int(max_length)) * 0.25)  # - 1

                room_point_x = random.randint(1, self.width - int(width))
                #print("room_point_x: " + str(room_point_x))
                room_point_y = random.randint(1, self.height - int(height))
                #print("room_point_y: " + str(room_point_y))

                if self.check_for_intersections(room_point_x, room_point_y, room_point_x + width, room_point_y + height) == False:
                    break

            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1

            # Create a room in the given direction
            room = Room(room_count, "A Generic Room",
                        "This is a generic room.", x, y)
            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            for y in range(room_point_y, room_point_y + height):
                for x in range(room_point_x, room_point_x + width):
                    self.grid[y][x] = room

            self.grid[y][x] = room

            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)

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
            # str += "#"
            for room in row:
                if room is not None:
                    out += " " + str(room.id % 10) + " "
                else:
                    out += "   "
            out += "#\n"

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
