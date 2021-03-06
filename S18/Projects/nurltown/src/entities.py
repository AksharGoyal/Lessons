"""
entities.py
Module containing class declarations for the entities that may populate the game
"""

# Importing external modules.
import pygame as pg             # The Pygame module
import config as cfg            # The configuration file containing parameters about the game
import itertools as itt         # Functions creating iterators for efficient looping
import numpy as np              # Module for scientific computing with Python
import math                     # Module for general-purpose mathematical functions

class Entity(pg.sprite.Sprite):
    """
    A base class for an entity in Nurltown
    """

    def __init__(self, image, init_x = 0, init_y = 0):
        """
        Constructor function for the Entity class
        :param image: The image which will be rendered to represent the entity
        :type image: pygame.Surface
        :param init_x: x coordinate of the initial position in the game
        :type init_x: float
        :param init_y: y coordinate of the initial position in the game
        :type init_y: float
        """

        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)

        # Set the sprite for the entity. Save a copy of the original image as a reference
        self.original_image = image
        self.image = image

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

        # Set the initial position
        self.rect.x = init_x
        self.rect.y = init_y

        # Set up a generator to yield subsequent pygame.Surfaces that will make up the shuffling
        # animation of the Entitb
        self.shuffle_cycle = self.generate_shuffle_frames(cfg.NURLET_SHUFFLE_ANGLE)

    def generate_shuffle_frames(self, max_deflection):
        """
        Function to create an iterator for the rotation angle per frame of the shuffling animation of the entity
        :param max_deflection: The maximum angle to which the entity's image rotates
        :type max_deflection: float
        :return: An iterator which yields the deflection angle of the subsequent frame in the shuffling animation
        :rtype: iterator
        """
        half_set = list(np.linspace(-1*max_deflection, max_deflection, 20))
        full_set =  half_set[::-1]+ half_set
        return itt.cycle(full_set)

    def distance_to(self, other):
        """
        Function to find distance to another entity using the Cartesian distane formula derived
        from the Pythagorean Theorem
        :param other: The other entity to which the distance is calculated
        :type other: Entity
        :return: The distance from this Entity object to 'other'
        :rtype: float
        """
        my = self.rect
        its = other.rect
        dist = math.sqrt((its.x - my.x)**2 + (its.y - my.y)**2)
        return dist

    def unit_vector_to(self, other):
        """
        Yields the unit vector from this Entity object to another Entity
        :param other: The other entity to which the unit vector points
        :type other: Entity
        :return: The unit vector from this Entity object to 'other'
        :rtype: tuple[float]
        """
        my = self.rect
        its = other.rect
        dist = self.distance_to(other)
        xhat = (its.x - my.x)/dist
        yhat = (its.y - my.y)/dist
        return xhat, yhat

    def shuffle_sprite(self):
        """
        Rotates the image of the entity by a set angle, representing the next frame of the shuffling animation
        """
        self.image = pg.transform.rotate(self.original_image, next(self.shuffle_cycle))

    def move(self, x, y):
        """
        Moves the entity from its current position by a supplied amount in the x and y directions
        :param x: Amount to move the entity along the x axis
        :type x: float
        :param y: Amount to move the entity along the y axis
        :type y: float
        """
        self.shuffle_sprite()                   # Progress the shuffling animation
        self.rect.move_ip(x, y)                 # Move the bounding box of the entity


class Nurlet(Entity):
    """
    Class representing the inhabitant of Nurltown.
    """
    def __init__(self, init_x = 0, init_y = 0):
        """
        Constructor function for the Nurlet class
        :param init_x: x coordinate of the initial position in the game
        :type init_x: float
        :param init_y: y coordinate of the initial position in the game
        :type init_y: float
        """

        # Load the image to represent the entity
        sprite = pg.image.load("assets/sprites/nurlet.png")
        # sprite = pg.image.load("supreme_leader3.png")

        # Call the parent class constructor
        super(Nurlet, self).__init__(sprite, init_x, init_y)

        # Set the movement speed
        self.speed = cfg.NURLET_SPEED

    def update(self, food):
        """
        Function to update the state of the Nurlet. This update phase determines whether the Nurlet
        moves, eats, attacks, or defends, based on its surroundings and the rest of the game state
        :param food: A group of food entities that currently exist in the game
        :type food: pygame.sprite.Group
        """
        self.seek_closest(food)
        self.eat_nearby(food)

    def seek_closest(self, group):
        """
        The Nurlet finds the closest entity in the supplied group and moves towards it
        :param group: A group of entities that currently exist in the game
        :type group: pygame.sprite.Group
        """

        # Initialize variables for closest food
        closest_distance = math.inf
        closest_entity = None


        # Find the closest entity
        for entity in group:
            dist = self.distance_to(entity)
            if dist < closest_distance:
                closest_distance = dist
                closest_entity = entity

        # Move towards the closest food at maximum speed
        x, y = [self.speed * i for i in self.unit_vector_to(closest_entity)]
        self.move(x, y)

    def eat_nearby(self, food):
        """
        Eat any food entities within the reach (bounding boxes colliding) of the Nurlet
        :param food: A group of food entities that currently exist in the game
        :type food: pygame.sprite.Group
        """
        pg.sprite.spritecollide(self, food, True)




class Food(Entity):
    """
    Class representing a morsel of food found within Nurltown
    """
    def __init__(self, init_x = 0, init_y = 0):
        """
        Constructor function for the Food class
        :param init_x: x coordinate of the initial position in the game
        :type init_x: float
        :param init_y: y coordinate of the initial position in the game
        :type init_y: float
        """

        # Load the image to represent the entity
        sprite = pg.image.load("assets/sprites/red_jelly.png")
        # sprite = pg.image.load("kimbap copy.png")

        # Call the parent class constructor
        super(Food, self).__init__(sprite, init_x, init_y)

