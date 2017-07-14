from django.db    import models
from django.conf  import settings
from os           import path
from enum         import Enum
from datetime     import datetime

from .models_conf import *

class Reservoir (models.Model) :
    """
    Water Reservoir
    """

    # directory with photos of the reservoirs
    RES_PICS_PATH = settings.BASE_DIR + "/main/static/main/img/reservoir_pics/"

    # the id of the reservoir
    res_id    = models.AutoField(primary_key=True)
    # the specific location of the reservoir
    latitude  = models.FloatField()
    longitude = models.FloatField()
    # island where the reservoir is located
    island    = models.CharField(max_length=MAX_STR_SIZE)
    # county(concelho) where the reservoir is located
    county  = models.CharField(max_length=MAX_STR_SIZE)
    # the town where the reservoir is located
    town      = models.CharField(max_length=MAX_STR_SIZE)
    ## these define the dimensions of the reservoir
    heigth = models.FloatField() # meters
    width  = models.FloatField() # meters
    length = models.FloatField() # meters

    nrPics = models.IntegerField(default=0)


    def totalCapacity (self) :
        """
        Calculates how much water the reservoir can hold (in cubic meters).

        Returns
        -------
        float
        """

        return self.heigth*self.width*self.length


    def addressName (self) :
        """
        Builds a printable address of the reservoir's location.

        Returns
        -------
        str
        """

        return "{}, {}, {}, @({}, {})".format(
                self.town, self.county, self.island, self.latitude, self.longitude)


    def mainPic (self) :
        """
        Returns a single picture from the directory of picttures of this reservoir.

        Returns
        -------
        string
            the path to the picture
        """

        mainPicName = Reservoir.RES_PICS_PATH + str(self.res_id) + '_0'
        # if file exists return the file name
        if path.isfile(mainPicName) :
            return '/static/main/img/reservoir_pics/' + str(self.res_id) + '_0'
        else:
            return '/static/main/img/reservoir_pics/stub'

    def setTemplateValues (self) :
        """
        Set the values to be used in a html page when this object is shown.
        """

        self.mainPic_         = self.mainPic()
        self.addressName_     = self.addressName()
        self.totalCapacity_   = self.totalCapacity()
