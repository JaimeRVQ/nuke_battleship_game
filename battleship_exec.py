# -*- coding: UTF-8 -*-
'''
Author: Jaime Rivera
File: battleship_exec.py
Date: 2018.09.23
Revision: 2018.09.23
Copyright: Copyright Jaime Rivera 2018 | www.jaimervq.com
           The program(s) herein may be used, modified and/or distributed in accordance with the terms and conditions
           stipulated in the Creative Commons license under which the program(s) have been registered. (CC BY-SA 4.0)

Brief: Executable file that displays a battleship game by using Nuke's interface items

'''

__author__ = 'Jaime Rivera <jaime.rvq@gmail.com>'
__copyright__ = 'Copyright 2018, Jaime Rivera'
__credits__ = []
__license__ = 'Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)'
__maintainer__ = 'Jaime Rivera'
__email__ = 'jaime.rvq@gmail.com'
__status__ = 'Testing'

import nuke
import random
import string
import datetime


# -------------------------------- SCENE PRESETS -------------------------------- #

# To be restored at the end of the game
dagColor = nuke.toNode('preferences')['DAGBackColor'].value()


# -------------------------------- BOARD PROPERTIES -------------------------------- #

dotDistance = 13  # Distance between dot nodes
dotNumber = 6  # Number of dots in every square side
squareSize = dotDistance * dotNumber
squareNumber = 10  # Number of squares on the board side
halfSquare = dotDistance * (dotNumber - 3)
totalSize = (squareSize * squareNumber) + dotDistance
user_com_distance = squareNumber * (90 + 300 * (1 / squareNumber))

backColor = 255  # Color to change the DAG to (255=black)


# -------------------------------- BOARD CREATION -------------------------------- #

def board_creation():
    # Changes to the scene
    nuke.toNode('preferences')['DAGBackColor'].setValue(backColor)

    # Progress bar
    nodes_progress = nuke.ProgressTask('Battleship game')
    nodes_progress.setMessage('Creating board')
    nodes_progress.setProgress(20)

    # CREATION OF BOARD
    # Creation of squares
    for i in range(0, totalSize, dotDistance):

        for j in range(0, totalSize, dotDistance):

            if j % squareSize == 0 or i % squareSize == 0:
                nuke.nodes.Dot(name='Dot_COM_bShip',
                               xpos=j,
                               ypos=i,
                               hide_input=True,
                               tile_color=1720943359)

                nuke.nodes.Dot(name='Dot_USER_bShip',
                               xpos=j,
                               ypos=i + user_com_distance,
                               hide_input=True,
                               tile_color=1720943359)

    nodes_progress.setProgress(60)

    # Creation of divider and COM/USER tags
    if squareNumber > 7:

        separation = totalSize + ((user_com_distance - totalSize) / 2)

        for X in range(-1, squareNumber + 4):
            no_op = nuke.nodes.NoOp(xpos=(X * 80) - 120,
                                    ypos=separation - 30,
                                    hide_input=True)

            no_op['name'].setValue('')

            if X == -1:
                nuke.nodes.StickyNote(name='COMtagbShip',
                                      label='COM',
                                      note_font='Arial Bold',
                                      note_font_size=25,
                                      note_font_color=4278190335,
                                      tile_color=backColor,
                                      xpos=(X * 80) - 120,
                                      ypos=separation - 100)

                nuke.nodes.StickyNote(name='USERtagbShip',
                                      label='USER',
                                      note_font='Arial Bold',
                                      note_font_size=25,
                                      note_font_color=536805631,
                                      tile_color=backColor,
                                      xpos=(X * 80) - 120,
                                      ypos=separation + 25)

    nodes_progress.setProgress(80)

    # Creation of coord labels
    label_size = 29
    for N in range(0, squareNumber):
        nuke.nodes.StickyNote(xpos=N * squareSize + 5,
                              ypos=-50,
                              note_font='Arial Black Bold Bold Bold Bold',
                              note_font_size=label_size,
                              tile_color=backColor,
                              label=str(N + 1),
                              name='bShip' + str(N + 1))

        nuke.nodes.StickyNote(xpos=N * squareSize + 5,
                              ypos=-50 + user_com_distance,
                              note_font='Arial Black Bold Bold Bold Bold',
                              note_font_size=label_size,
                              tile_color=backColor,
                              label=str(N + 1),
                              name='bShip' + str(N + 1))

        nuke.nodes.StickyNote(xpos=-80,
                              ypos=N * squareSize + 28,
                              note_font='Arial Black Bold Bold Bold Bold',
                              note_font_size=label_size,
                              tile_color=backColor,
                              label=string.uppercase[N],
                              name='bShip' + string.uppercase[N])

        nuke.nodes.StickyNote(xpos=-80,
                              ypos=N * squareSize + 28 + user_com_distance,
                              note_font='Arial Black Bold Bold Bold Bold',
                              note_font_size=label_size,
                              tile_color=backColor,
                              label=string.uppercase[N],
                              name='bShip' + string.uppercase[N])

    nodes_progress.setProgress(100)
    del nodes_progress

    # Framing the nodes
    for node in nuke.allNodes():
        node.setSelected(True)
    nuke.zoomToFitSelected()
    for node in nuke.allNodes():
        node.setSelected(False)

    # Changes to the Main node
    kMainButton.setLabel('<b><font size = 6>FIRE!')
    kMainButton.setValue('user_fires()')
    kInfo.setValue('''How to to fire:
-Select a coordinate (yellow dot node)
-Press the FIRE! button''')


# -------------------------------- COORDINATE CLASS -------------------------------- #

# IDs that will be used when calling most methods in this class:
USER = 1
COM = 0


class Coordinate(object):

    def __init__(self, com_main_coord, i, j):

        # GENERAL PROPERTIES
        self.row = i
        self.column = j
        self.name = chr(i + 65) + str(j + 1)

        # COM COORD PROPERTIES
        self.com_main_coord = com_main_coord
        self.main_dot = nuke.nodes.Dot(name='Coord_bShip_' + self.name,
                                       xpos=self.com_main_coord['xpos'],
                                       ypos=self.com_main_coord['ypos'],
                                       tile_color=4292085759,
                                       hide_input=True)
        self.com_coords = []
        for i in range((self.com_main_coord['ypos'] - halfSquare + dotDistance),
                       (self.com_main_coord['ypos'] + halfSquare),
                       dotDistance):
            for j in range((self.com_main_coord['xpos'] - halfSquare + dotDistance),
                           (self.com_main_coord['xpos'] + halfSquare), dotDistance):
                if not (i == self.com_main_coord['xpos'] and j == self.com_main_coord['xpos']):
                    self.com_coords.append({'ypos': i, 'xpos': j})

        self.com_has_boat = False
        self.com_is_revealed = False

        # USER COORD PROPERTIES
        self.user_coords = []
        for coord in self.com_coords:
            self.user_coords.append({'xpos': coord['xpos'], 'ypos': coord['ypos'] + user_com_distance})
        self.user_coords.append({'xpos': self.com_main_coord['xpos'],
                                 'ypos': self.com_main_coord['ypos'] + user_com_distance})

        self.user_has_boat = False
        self.has_boat_showed = False
        self.user_boat_dots = []
        self.user_is_revealed = False
        self.user_is_discarded = False

        # Node-related properties
        self.destruction_colors = [1444619007, 1142163967, 2385447935, 2471692543, 2182227711, 3239706624, 3931066112]
        self.boat_colors = [2576980479, 2863311615, 2863311615, 3149642751, 2576985599, 1431660799, 2004322815]
        self.water_colors = [456017151, 591157504, 675374592]

    def __str__(self):
        return 'Coordinate object {name} | ' \
               'Row: {row} | ' \
               'Column: {column}' \
               '\nCOM STATS: Has boat={comboat} | Is revealed={comrevealed}' \
               '\nUSER STATS: Has boat={userboat} | Is revealed={userrevealed} | Is discarded={userisdiscarded}' \
               ''.format(name=self.name,
                         row=self.row,
                         column=self.column,
                         comboat=self.com_has_boat,
                         comrevealed=self.com_is_revealed,
                         userboat=self.user_has_boat,
                         userrevealed=self.user_is_revealed,
                         userisdiscarded=self.user_is_discarded)

    # GENERAL METHODS
    def get_name(self):
        return self.name

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    # GAMEPLAY METHODS
    def get_has_boat(self, id):
        if id == 0:
            return self.com_has_boat
        elif id == 1:
            return self.user_has_boat

    def set_has_boat(self, id):
        if id == 0:
            self.com_has_boat = True
        elif id == 1:
            self.user_has_boat = True

    def get_is_revealed(self, id):
        if id == 0:
            return self.com_is_revealed
        elif id == 1:
            return self.user_is_revealed

    def set_is_revealed(self, id):
        if id == 0:
            self.com_is_revealed = True
        elif id == 1:
            self.user_is_revealed = True

    def take_fire(self, id):
        if id == 0:
            if self.com_has_boat:
                for element in self.com_coords:
                    nuke.nodes.Dot(name='Destroyed_bShip',
                                   xpos=element['xpos'],
                                   ypos=element['ypos'],
                                   tile_color=random.choice(self.destruction_colors),
                                   hide_input=True)
                self.main_dot['tile_color'].setValue(random.choice(self.destruction_colors))
            else:
                for element in self.com_coords:
                    nuke.nodes.Dot(name='Water_bShip',
                                   xpos=element['xpos'],
                                   ypos=element['ypos'],
                                   tile_color=random.choice(self.water_colors),
                                   hide_input=True)
                self.main_dot['tile_color'].setValue(random.choice(self.water_colors))

            self.set_is_revealed(COM)
            return self.com_has_boat

        elif id == 1:
            if self.user_has_boat:
                for node in self.user_boat_dots:
                    node['tile_color'].setValue(random.choice(self.destruction_colors))
            else:
                for element in self.user_coords:
                    nuke.nodes.Dot(name='Water_bShip',
                                   xpos=element['xpos'],
                                   ypos=element['ypos'],
                                   tile_color=random.choice(self.water_colors),
                                   hide_input=True)

            self.set_is_revealed(USER)
            return self.user_has_boat

    # COM EXCLUSIVE METHODS
    def get_x_coord(self, id):
        if id == 0:
            return self.com_main_coord['xpos']

    def get_y_coord(self, id):
        if id == 0:
            return self.com_main_coord['ypos']

    def show_nature(self, id):
        if id == 0:
            if self.com_has_boat:
                for element in self.com_coords:
                    nuke.nodes.Dot(name='Boat_bShip',
                                   xpos=element['xpos'],
                                   ypos=element['ypos'],
                                   tile_color=random.choice(self.boat_colors),
                                   hide_input=True)
                self.main_dot['tile_color'].setValue(random.choice(self.boat_colors))
            else:
                for element in self.com_coords:
                    nuke.nodes.Dot(name='Water_bShip',
                                   xpos=element['xpos'],
                                   ypos=element['ypos'],
                                   tile_color=random.choice(self.water_colors),
                                   hide_input=True)
                self.main_dot['tile_color'].setValue(random.choice(self.water_colors))

            self.set_is_revealed(COM)
            return self.com_has_boat

    # PLAYER EXCLUSIVE METHODS
    def get_is_discarded(self, id):
        if id == 1:
            return self.user_is_discarded

    def set_is_discarded(self, id):
        if id == 1:
            self.user_is_discarded = True

    def show_boat(self, id):
        if id == 1:
            if self.user_has_boat:
                for element in self.user_coords:
                    boat_node = nuke.nodes.Dot(name='Boat_bShip',
                                               xpos=element['xpos'],
                                               ypos=element['ypos'],
                                               tile_color=random.choice(self.boat_colors),
                                               hide_input=True)
                    self.user_boat_dots.append(boat_node)
            self.has_boat_showed = True

    def get_has_boat_showed(self):
        if id == 1:
            return self.has_boat_showed


# -------------------------------- COORDINATE OBJECTS-------------------------------- #

def coord_objects_creation():
    # Matrix of coordinate objects
    objects_matrix = [0] * squareNumber
    for s in range(squareNumber):
        objects_matrix[s] = [0] * squareNumber

    for i in range(0, squareNumber):

        for j in range(0, squareNumber):
            objects_matrix[i][j] = Coordinate(
                {'xpos': (j * squareSize) + halfSquare, 'ypos': (i * squareSize) + halfSquare}, i, j)

    return objects_matrix


# -------------------------------- VALID LAYOUTS -------------------------------- #

# Dictionary of boats in this configuration (10x10)
boatDict = {'5_boat': 1, '4_boat': 1, '3_boat': 2, '2_boat': 1}


# Method to set the board
def set_board():
    # List of valid layouts
    layout_list = [
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 1, 1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
         [0, 1, 1, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 1, 1, 0, 0, 1, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
         [1, 0, 0, 0, 1, 0, 0, 1, 0, 0], [1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
         [1, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
         [1, 0, 0, 0, 1, 0, 0, 1, 0, 0], [1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
         [1, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 1, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]],
        
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 1, 1, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 1, 1, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]],
        
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 1, 1, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ]

    while True:
        user_layout = random.choice(layout_list)
        com_layout = random.choice(layout_list)

        if user_layout != com_layout:
            break

    for i in range(squareNumber):
        for j in range(squareNumber):

            if bool(user_layout[i][j]):
                coord_objects[i][j].set_has_boat(USER)
            if bool(com_layout[i][j]):
                coord_objects[i][j].set_has_boat(COM)

    # Option to display user's boats
    if showUserAllBoats:

        for row in coord_objects:
            for element in row:
                element.show_boat(USER)


# -------------------------------- GAMEPLAY FUNCTIONS -------------------------------- #

def user_fires():

    # Check if the fire input is correct
    if len(nuke.selectedNodes()) > 1:

        nuke.message('<font size=3>Please select only one node')
        for node in nuke.allNodes():
            node.setSelected(False)

    elif len(nuke.selectedNodes()) == 0:
        nuke.message('<font size=3>Please select one of the yellow dots')

    else:
        # Check if it is a hit
        target = None
        for row in coord_objects:
            for element in row:
                if [element.get_x_coord(COM), element.get_y_coord(COM)] == [nuke.selectedNode()['xpos'].value(),
                                                                            nuke.selectedNode()['ypos'].value()]:
                    target = element

        if target.take_fire(COM):
            if not game_is_over():
                kInfo.setValue('''You have hit COM successfully, now you can fire again:
    -Select a coordinate (yellow dot node)
    -Press the FIRE! button''')
                nStickyMain['label'].setValue("It's a hit!\nNow you can shoot again")

                for node in nuke.allNodes():
                    node.setSelected(False)
            else:
                reveal_com_boats()
                end_game()

        else:
            kInfo.setValue('''How to to fire:
-Select a coordinate (yellow dot node)
-Press the FIRE! button''')

            for node in nuke.allNodes():
                node.setSelected(False)

            com_fires()


def com_fires(previous_coord=None, keep_tag=False):
    if not game_is_over():

        discard_coords()
        discard_water()

        if previous_coord is None:

            # Take all objects that have not been revealed
            candidate_coords = []

            for row in coord_objects:
                for element in row:
                    if (not element.get_is_revealed(USER)) and (not element.get_is_discarded(USER)):
                        candidate_coords.append(element)

            # Now choosing coords that have received fire and testing for adjacents
            best_candidate = None
            for row in coord_objects:
                for element in row:
                    if element.get_is_revealed(USER) and element.get_has_boat(USER) and (
                            not element.get_is_discarded(USER)):
                        if calculate_adjacent(element) is not None:
                            best_candidate = element

            # Choosing a target from availabe coords (giving priority to adjacents to already tested coords)
            if best_candidate is not None:
                target = calculate_adjacent(best_candidate)
            else:
                target = random.choice(candidate_coords)

            if not showUserAllBoats:
                target.show_boat(USER)

            # Now checking if the shot was successful
            print_available_coords()
            nuke.tprint('\nCOM fires at: {}\n-------------------'.format(target.get_name()))  # Game feedback
            if target.take_fire(USER):

                if keep_tag:
                    nStickyMain['label'].setValue(nStickyMain['label'].value() + ', at {}'.format(target.get_name()))
                else:
                    nStickyMain['label'].setValue('COM has hit you at {}'.format(target.get_name()))

                com_fires(target)

            else:

                if keep_tag:
                    nStickyMain['label'].setValue(
                        nStickyMain['label'].value() + '\nAnd has missed the next shot at {}'.format(target.get_name()))
                else:
                    nStickyMain['label'].setValue('COM has missed at {}'.format(target.get_name()))

        else:

            # Calculating adjacent to previous coord
            adjacentToPrevious = calculate_adjacent(previous_coord)

            # Choosing a target from availabe adjacents
            if adjacentToPrevious is not None:
                print_available_coords()
                nuke.tprint('\nCOM fires at: {}, from adjacents to previous shot at {}\n'
                            '-------------------------------------------------------'
                            .format(adjacentToPrevious.get_name(), previous_coord.get_name()))

                if not showUserAllBoats:
                    adjacentToPrevious.show_boat(USER)

                # Now checking if the shot was successful
                if adjacentToPrevious.take_fire(USER):

                    nStickyMain['label'].setValue(
                        nStickyMain['label'].value() + ', at {}'.format(adjacentToPrevious.get_name()))
                    com_fires(adjacentToPrevious, keep_tag=True)

                else:

                    nStickyMain['label'].setValue(
                        nStickyMain['label'].value() + '\nAnd has missed the next shot at {}'
                        .format(adjacentToPrevious.get_name()))

            else:

                com_fires(keep_tag=True)

    else:

        nStickyMain['note_font_size'].setValue(30)
        if 'COM' in nStickyMain['label'].value():
            nStickyMain['label'].setValue(
                "GAME IS OVER!\nNow COM's boats are being revealed\n<font size =2>" + nStickyMain['label'].value())
        else:
            nStickyMain['label'].setValue("GAME IS OVER!\nNow COM's boats are being revealed")

        reveal_com_boats()
        end_game()


def calculate_adjacent(coord_object):
    row = coord_object.get_row()
    column = coord_object.get_column()

    # Defining all 4 adjacents of given coord
    right_adjacent = None
    left_adjacent = None
    up_adjacent = None
    down_adjacent = None

    if 0 <= column + 1 <= 9:
        right_adjacent = coord_objects[row][column + 1]

    if 0 <= column - 1 <= 9:
        left_adjacent = coord_objects[row][column - 1]

    if 0 <= row - 1 <= 9:
        up_adjacent = coord_objects[row - 1][column]

    if 0 <= row + 1 <= 9:
        down_adjacent = coord_objects[row + 1][column]

    adjacents_list = [right_adjacent, left_adjacent, up_adjacent, down_adjacent]

    # Discarding by pairs of coords
    if (right_adjacent is not None and right_adjacent.get_is_revealed(USER) and right_adjacent.get_has_boat(USER)) or (
            left_adjacent is not None and left_adjacent.get_is_revealed(USER) and left_adjacent.get_has_boat(USER)):

        try:
            up_adjacent.set_is_discarded(USER)
        except:
            pass
        try:
            down_adjacent.set_is_discarded(USER)
        except:
            pass

    if (up_adjacent is not None and up_adjacent.get_is_revealed(USER) and up_adjacent.get_has_boat(USER)) or (
            down_adjacent is not None and down_adjacent.get_is_revealed(USER) and down_adjacent.get_has_boat(USER)):

        try:
            right_adjacent.set_is_discarded(USER)
        except:
            pass
        try:
            left_adjacent.set_is_discarded(USER)
        except:
            pass

    # Choosing the appropriate adjacent coord
    for adjacent in adjacents_list:
        if adjacent is None:
            adjacents_list.remove(adjacent)

    if right_adjacent is not None:

        if right_adjacent.get_is_revealed(USER):

            try:
                adjacents_list.remove(right_adjacent)
            except:
                pass

            if right_adjacent.get_has_boat(USER):

                try:
                    adjacents_list.remove(up_adjacent)
                except:
                    pass
                try:
                    adjacents_list.remove(down_adjacent)
                except:
                    pass

    if left_adjacent is not None:

        if left_adjacent.get_is_revealed(USER):

            try:
                adjacents_list.remove(left_adjacent)
            except:
                pass

            if left_adjacent.get_has_boat(USER):

                try:
                    adjacents_list.remove(up_adjacent)
                except:
                    pass
                try:
                    adjacents_list.remove(down_adjacent)
                except:
                    pass

    if up_adjacent is not None:

        if up_adjacent.get_is_revealed(USER):

            try:
                adjacents_list.remove(up_adjacent)
            except:
                pass

            if up_adjacent.get_has_boat(USER):

                try:
                    adjacents_list.remove(right_adjacent)
                except:
                    pass
                try:
                    adjacents_list.remove(left_adjacent)
                except:
                    pass

    if down_adjacent is not None:

        if down_adjacent.get_is_revealed(USER):

            try:
                adjacents_list.remove(down_adjacent)
            except:
                pass

            if down_adjacent.get_has_boat(USER):

                try:
                    adjacents_list.remove(right_adjacent)
                except:
                    pass
                try:
                    adjacents_list.remove(left_adjacent)
                except:
                    pass

    # Adjacent to return
    if len(adjacents_list) > 0:
        return random.choice(adjacents_list)
    else:
        return None


def discard_surrounding(coord_object):
    coord_object.set_is_discarded(USER)

    row = coord_object.get_row()
    column = coord_object.get_column()

    surroundingList = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != j and i != -j:

                if (0 <= row + i <= 9) and (0 <= column + j <= 9):
                    surroundingList.append(coord_objects[row + i][column + j])

    for coord in surroundingList:
        coord.set_is_discarded(USER)


def discard_coords():
    # Will be checked for every coord object
    for row in coord_objects:
        for element in row:

            if element.get_has_boat(USER) and element.get_is_revealed(USER):

                if not element.get_is_discarded(USER):

                    row = element.get_row()
                    column = element.get_column()

                    for i in range(5, 1, -1):

                        if boatDict['{}_boat'.format(i)] != 0:

                            right_adjacents = {'ID': 'RIGHT', 'coords': [], 'names': [], 'content': []}
                            left_adjacents = {'ID': 'LEFT', 'coords': [], 'names': [], 'content': []}
                            up_adjacents = {'ID': 'UP', 'coords': [], 'names': [], 'content': []}
                            down_adjacents = {'ID': 'DOWN', 'coords': [], 'names': [], 'content': []}

                            all_adjacents = [right_adjacents, left_adjacents, up_adjacents, down_adjacents]

                            for N in range(-1, i + 1):

                                if 0 <= column + N <= 9:
                                    right_adjacents['coords'].append(coord_objects[row][column + N])
                                    right_adjacents['names'].append(coord_objects[row][column + N].get_name())
                                    if coord_objects[row][column + N].get_is_revealed(USER):
                                        if coord_objects[row][column + N].get_has_boat(USER):
                                            right_adjacents['content'].append('HIT')
                                        else:
                                            right_adjacents['content'].append('WATER')
                                else:
                                    right_adjacents['coords'].append(None)
                                    right_adjacents['names'].append('OUT-OF-BOARD')
                                    right_adjacents['content'].append('OUT')

                                if 0 <= column - N <= 9:
                                    left_adjacents['coords'].append(coord_objects[row][column - N])
                                    left_adjacents['names'].append(coord_objects[row][column - N].get_name())
                                    if coord_objects[row][column - N].get_is_revealed(USER):
                                        if coord_objects[row][column - N].get_has_boat(USER):
                                            left_adjacents['content'].append('HIT')
                                        else:
                                            left_adjacents['content'].append('WATER')
                                else:
                                    left_adjacents['coords'].append(None)
                                    left_adjacents['names'].append('OUT-OF-BOARD')
                                    left_adjacents['content'].append('OUT')

                                if 0 <= row - N <= 9:
                                    up_adjacents['coords'].append(coord_objects[row - N][column])
                                    up_adjacents['names'].append(coord_objects[row - N][column].get_name())
                                    if coord_objects[row - N][column].get_is_revealed(USER):
                                        if coord_objects[row - N][column].get_has_boat(USER):
                                            up_adjacents['content'].append('HIT')
                                        else:
                                            up_adjacents['content'].append('WATER')
                                else:
                                    up_adjacents['coords'].append(None)
                                    up_adjacents['names'].append('OUT-OF-BOARD')
                                    up_adjacents['content'].append('OUT')

                                if 0 <= row + N <= 9:
                                    down_adjacents['coords'].append(coord_objects[row + N][column])
                                    down_adjacents['names'].append(coord_objects[row + N][column].get_name())
                                    if coord_objects[row + N][column].get_is_revealed(USER):
                                        if coord_objects[row + N][column].get_has_boat(USER):
                                            down_adjacents['content'].append('HIT')
                                        else:
                                            down_adjacents['content'].append('WATER')
                                else:
                                    down_adjacents['coords'].append(None)
                                    down_adjacents['names'].append('OUT-OF-BOARD')
                                    down_adjacents['content'].append('OUT')

                            # Checking if boat of lenght i can be discarded
                            for dictionary in all_adjacents:

                                if len(dictionary['content']) == i + 2 \
                                        and dictionary['content'].count('HIT') == i \
                                        and (dictionary['content'][0] in ('WATER', 'OUT')) \
                                        and (dictionary['content'][i + 1] in ('WATER', 'OUT')):

                                    nuke.tprint(
                                        '\n\nUsed coord {} for discarding boat of lenght {}\n'
                                        '--------------------------------------'
                                        .format(element.get_name(), i))
                                    nuke.tprint('DIRECTION: {}\nNAMES: {}\nCONTENTS: {}'
                                                .format(dictionary['ID'], dictionary['names'], dictionary['content']))

                                    for b in range(1, i + 1):
                                        discard_surrounding(dictionary['coords'][b])
                                        nuke.tprint('-' + dictionary['names'][b] + ' and its adjacents have been discarded')

                                    nuke.tprint('\n{} BOAT OF LENGHT {} is discarded'.format('X' * i, i))
                                    boatDict['{}_boat'.format(i)] -= 1
                                    nuke.tprint('REMAINING BOATS: {}\n'.format(boatDict))

                else:
                    calculate_adjacent(element)


def discard_water():

    for row in coord_objects:
        for element in row:

            if element.get_is_revealed(USER) and (not element.get_has_boat(USER)):
                element.set_is_discarded(USER)

            row = element.get_row()
            column = element.get_column()

            # Defining all 4 adjacents of given coord
            right_adjacent = None
            left_adjacent = None
            up_adjacent = None
            down_adjacent = None

            if 0 <= column + 1 <= 9:
                right_adjacent = coord_objects[row][column + 1]

            if 0 <= column - 1 <= 9:
                left_adjacent = coord_objects[row][column - 1]

            if 0 <= row - 1 <= 9:
                up_adjacent = coord_objects[row - 1][column]

            if 0 <= row + 1 <= 9:
                down_adjacent = coord_objects[row + 1][column]

            if ((right_adjacent is not None and right_adjacent.get_is_revealed(USER)
                 and (not right_adjacent.get_has_boat(USER))) or right_adjacent is None) \
                    and ((left_adjacent is not None and left_adjacent.get_is_revealed(USER)
                          and (not left_adjacent.get_has_boat(USER))) or left_adjacent is None) \
                    and ((up_adjacent is not None and up_adjacent.get_is_revealed(USER)
                          and (not up_adjacent.get_has_boat(USER))) or up_adjacent is None) \
                    and ((down_adjacent is not None and down_adjacent.get_is_revealed(USER)
                          and (not down_adjacent.get_has_boat(USER))) or down_adjacent is None):

                element.set_is_discarded(USER)


def print_available_coords():

    nuke.tprint('\nAVAILABLE COORDS:\n-----------------')
    available_coords = ''

    for row in coord_objects:
        for element in row:

            if not element.get_is_discarded(USER):
                available_coords += element.get_name() + ','

    nuke.tprint(available_coords)

def game_is_over():
    user_all_revealed = True
    com_all_revealed = True

    for row in coord_objects:
        for element in row:

            if element.get_has_boat(USER) and not element.get_is_revealed(USER):
                user_all_revealed = False

            if element.get_has_boat(COM) and not element.get_is_revealed(COM):
                com_all_revealed = False

    return user_all_revealed or com_all_revealed


def end_game():
    # Showing the winner
    userAllRevealed = True

    for row in coord_objects:
        for element in row:

            if element.get_has_boat(USER) and not element.get_is_revealed(USER):
                userAllRevealed = False

    if userAllRevealed:
        nuke.message('<b><font size=5>GAME OVER\n<font color = red>COM WINS')
    else:
        nuke.message('<b><font size=5>GAME OVER\n<font color = green>YOU WIN')

    # Scene restoration
    nuke.toNode('preferences')['DAGBackColor'].setValue(dagColor)

    # Deletion of nodes
    for node in nuke.allNodes():
        if "bShip" in node['name'].value() or node.Class() == 'NoOp':
            nuke.delete(node)

    nuke.tprint('\n\n---------------------\n+++++ GAME OVER +++++\n---------------------')


# -------------------------------- 'EXTRA' FUNCTIONS -------------------------------- #

def reveal_com_boats():
    for row in coord_objects:
        for element in row:

            if (not element.get_is_revealed(COM)) and (element.get_has_boat(COM)):
                element.show_nature(COM)


def reveal_all():
    for row in coord_objects:
        for element in row:

            # For user elements
            if not element.get_is_revealed(USER):
                if element.get_has_boat(USER) and not element.get_has_boat_showed(USER):
                    element.show_boat(USER)
                else:
                    element.take_fire(USER)

            # For COM elements
            if not element.get_is_revealed(COM):
                element.show_nature(COM)


def print_positions():
    text_user = ''
    text_com = ''

    for row in coord_objects:
        text_com += '\n'
        text_user += '\n'

        for element in row:

            if element.get_has_boat(USER):
                text_user += 'BO'
            else:
                text_user += '--'

            if element.get_has_boat(COM):
                text_com += 'BO'
            else:
                text_com += '--'

    nuke.tprint('\n\nCOM BOATS\n' + text_com + '\n\nUSER BOATS\n' + text_user)


# -------------------------------- GAMEPLAY -------------------------------- #
# -------------------------------------------------------------------------- #

# Start of game
# ------------------------------------------------------------

nuke.tprint('\n\n--- NEW GAME STARTED AT {} ---'.format(str(datetime.datetime.now())[:16]))

# Cleaning scene (supposed to be empty, just with a viewer node)
# ------------------------------------------------------------

for n in nuke.allNodes('Viewer'):
    nuke.delete(n)

# Main playing node
# ------------------------------------------------------------

nStickyMain = nuke.nodes.StickyNote(name='MAIN_bShip',
                                    label='',
                                    note_font='Arial Bold',
                                    note_font_size=40,
                                    tile_color=backColor,
                                    xpos=totalSize + 150,
                                    ypos=totalSize + user_com_distance - (2.2 * squareSize))

# Main button: will change through the game
kMainButton = nuke.PyScript_Knob('py_main_button', '<b><font size = 6>...starting')
nStickyMain.addKnob(kMainButton)

# Divider
kDivider = nuke.Text_Knob('divider', '')
nStickyMain.addKnob(kDivider)

# Information knob: tells the user how the gameplay develops
kInfo = nuke.Text_Knob('Z_info', '', "<b>Information")
nStickyMain.addKnob(kInfo)

nStickyMain['User'].setName('Gameplay')

# Framing the main node
for n in nuke.allNodes():
    n.setSelected(False)

nStickyMain.setSelected(True)
nuke.zoomToFitSelected()
nuke.show(nStickyMain)
nStickyMain.setSelected(False)

# Creation of board and coord objects
# ------------------------------------------------------------

board_creation()
coord_objects = coord_objects_creation()

# Setting the boats on the board
# ------------------------------------------------------------

showUserAllBoats = nuke.ask('<b><font size=4>Do you wish to see where your own boats are?')
set_board()

# Protecting the nodes from being moved
# ------------------------------------------------------------

for n in nuke.allNodes():

    if 'bShip' in n.name() or n.Class == 'NoOp':
        y = n['ypos'].value()
        x = n['xpos'].value()

        n['knobChanged'].setValue("nuke.thisNode()['xpos'].setValue({}) , nuke.thisNode()['ypos'].setValue({})"
                                  "".format(x, y))
