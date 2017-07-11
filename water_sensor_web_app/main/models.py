from django.db    import models
from django.utils import timezone
from django.conf  import settings
from os           import path
from enum         import Enum

# TODO: this file should be in a central location where both this app and the webserver could access it

# defines the maximum size of a string 
MAX_STR_SIZE = 256
# defines the maximum size of a directory or file path
MAX_PATH_SIZE = 500


class Reservoir (models.Model) :
    """
    Water Reservoir
    """

    # directory with photos of the reservoirs
    RES_PICS_PATH = settings.BASE_DIR + "/main/static/main/img/reservoir_pics/"    

    # the id of the reservoir
    res_id    = models.AutoField(primary_key=True)
    
    ## these define the dimensions of the reservoir
    heigth = models.FloatField() # meters
    width  = models.FloatField() # meters
    length = models.FloatField() # meters
    
    nrPics = models.IntegerField(default=0)
    
    def totalCapacity (self) :
        return self.heigth*self.width*self.length
        
    def waterVolume (self) :
        """
        To calculate the volume of water currently in the reservoir.
        """

        # get the latest measurment related to this reservoir
        try :
            latestMeasurement = Measurement.objects.filter(reservoir=self).latest('dateTime')
        except Measurement.DoesNotExist :
            return 'No measurements'

        return abs(self.heigth - latestMeasurement.waterLevel)*self.width*self.length

    def waterQuality (self) :
        """
        To calculate the current water quality
        """
        pass

    def addressName (self) :
        """
        Builds a printable address of the reservoir's location
        """

        return "{}, {}, {}, @({}, {})".format(
                self.town, self.county, self.island, self.latitude, self.longitude)
    

    def mainPic (self) :
        """
        Returns a single picture from the directory of picttures of this reservoir.
        """

        mainPicName = Reservoir.RES_PICS_PATH + str(self.res_id) + '_0'
        print("[mainPic] mainPicName =  {}".format(mainPicName))
        # if file exists return the file name
        if path.isfile(mainPicName) :
            return '/static/main/img/reservoir_pics/' + str(self.res_id) + '_0'
        else:
            return '/static/main/img/reservoir_pics/stub'

    def setTemplateValues (self) :
        """
        Set the values to be used in a html page when this object is shown
        """

        self.waterVolume_   = self.waterVolume()
        self.mainPic_       = self.mainPic()
        self.addressName_   = self.addressName()
        self.totalCapacity_ = self.totalCapacity()


class FlowPoint (models.Model) :
    """
    A flow point represents either an input or an output point
    of water into/out of a Reservoir
    """

    ## these are the values 'function' can take
    Type = Enum('Type', "input output")

    # the id of this object
    flPoint_id = models.AutoField(primary_key=True)
    # function is either input or output
    function  = models.CharField(max_length=6)
    # the reservoir it belongs to
    reservoir = models.ForeignKey(Reservoir, on_delete=models.CASCADE)
    # TODO: put the specific location in the reservoir of this flowpoint



class Measurement (models.Model) :
    """
    A periodic measurement of the water level and quality
    Water quality is given by it's pH and conductivity
    """

    # the id of this measurement
    mes_id       = models.AutoField(primary_key=True)
    # the reservoir this measurement belongs to
    reservoir    = models.ForeignKey(Reservoir)
    # date and time of reading
    dateTime = models.DateTimeField(default=timezone.now)
    # the heigth of the part of the reservoir that has no water
    waterLevel   = models.FloatField(default=-1)
    # pH of the water
    pH           = models.FloatField(default=-1)
    # conductivity of the water
    conductivity = models.FloatField(default=-1)
    # salinity of the water
    salinity     = models.FloatField(default=-1)
    # total disolved solids in the water
    tds          = models.FloatField(default=-1)

    def waterQuality (self) :
        """
        Returns a measure of water quality according to pH and conductivity
        """
        # TODO: implement
        pass
    

class Conection (models.Model) :
    """
    Represents a conecion between 2 reservoirs
    """

    # possible directons of water flow
    FlowDirection = Enum('Direction', "A_to_B, B_to_A, bidirectional")

    # id of this object
    con_id       = models.AutoField(primary_key=True)
    # the length of the piping in the conexion
    pipingLength = models.FloatField() # meters
    # maximum flow of water supported by this conexion
    maxFlow      = models.FloatField() # cubic meters / second
    # the reservoirs that are connected
    reservoirA   = models.ForeignKey(Reservoir, related_name='A_con')
    reservoirB   = models.ForeignKey(Reservoir, related_name='B_con')


class Pump (models.Model) :
    """
    Represents a water extraction an pumping site
    """

    # id of this pump
    pump_id = models.AutoField(primary_key=True)
    # the maximum daily water production capacity
    maxProdCapacity = models.FloatField()  # cubic meters / day
    # the maximum pumping capacity
    maxPumpingCapacity = models.FloatField() # cubic meters / second
    # the specific location of the pump
    latitude  = models.FloatField()
    longitude = models.FloatField()
    # island where the pump is located
    island    = models.CharField(max_length=MAX_STR_SIZE)
    # county(concelho) where the pump is located
    county  = models.CharField(max_length=MAX_STR_SIZE)
    # the town where the pump is located
    town      = models.CharField(max_length=MAX_STR_SIZE)


class PumpConection (models.Model) :
    """
    Represents the conection between a pump and a reservoir
    """

    # id of this conection
    pump_con_id  = models.AutoField(primary_key=True)
    # the length of the piping in the conexion
    pipingLength = models.FloatField() # meters
    # maximum flow of water supported by this conexion
    maxFlow      = models.FloatField() # cubic meters / second
    # the reservoir that are connected
    reservoir    = models.ForeignKey(Reservoir)
