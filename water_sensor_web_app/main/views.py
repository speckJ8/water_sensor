from django.shortcuts import render, redirect
from django.http      import HttpResponse, Http404
from django.template  import loader
from django.conf      import settings

from django.contrib.auth            import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User
from django.forms.models            import model_to_dict

from django.core.exceptions         import FieldError

from datetime import datetime

import django.contrib.auth as auth
import json

from .models import *


def main (req) :
    """
    opens the main page or the presentation page if
    the user is not logged in
    """

    template = loader.get_template('main/intro.html')
    return HttpResponse(template.render({}, req))


def login (req) :
    """
    Returns the login page's html
    """

    template = loader.get_template('main/login.html')
    return HttpResponse(template.render({}, req))


def doLogin (req) :
    """
    This function does the actual login verification. It checks the credentials
    and returns error messages or the an ok and saves the user session.
    """

    username = req.POST['username']
    password = req.POST['password']

    # search for a user with the username
    try :
        User.objects.get(username=username)
    except User.DoesNotExist :
        # return username error
        print("[doLogin] invalid username")
        res = '{"state":"err", "err": "username"}'
        return HttpResponse(res)

    user = authenticate(username=username, password=password)
    # check password
    if user is not None :
        # save session
        auth.login(req, user)
        print("[doLogin] login succeded")
    else:
        # return password error
        print("[doLogin] invalid password")
        res = '{"state":"err", "err": "password"}'
        return HttpResponse(res)

    # go to the home page
    return HttpResponse('{"state": "ok"}')


@login_required(login_url='/login')
def doLogout (req) :
    auth.logout(req)
    return redirect('/login')


@login_required(login_url='/login')
def home (req) :
    """
    Returns the home page
    """

    template = loader.get_template('main/home.html')
    return HttpResponse(template.render({}, req))

@login_required(login_url='/login')
def map (req) :
    """
    Returns a page with a map with the locations of the reservoirs, pumps and the conections
    """

    reservoirs    = []
    pumps         = []
    resCons       = []
    pumpCons      = []

    try:
        res      = Reservoir.objects.all()
        pmps     = Pump.objects.all()
        pumpCons  = PumpConnection.objects.all().values(
            'pipingLength', 'maxFlow', 'reservoir__res_id', 'pump__pump_id')
        resCons = Connection.objects.all().values(
            'pipingLength', 'maxFlow', 'flowDirection',
            'con_id', 'reservoirA__res_id', 'reservoirB__res_id')

        for r in res :
            reservoirs.append({
                'id': r.res_id,
                'position': {'lat': r.latitude, 'lng': r.longitude},
                'address': r.addressName()
            })
        for p in pmps :
            pumps.append({
                'id': p.pump_id,
                'position': {'lat': p.latitude, 'lng': p.longitude},
                'address': p.addressName()
            })


    except Exception as e:
        print("[map] couldn't get data: {}".format(e))

    data = {
        'google_maps_key': settings.GOOGLE_MAPS_KEY,
        'reservoirs'     : json.dumps(reservoirs),
        'pumps'          : json.dumps(pumps),
        'reservoirCons'  : repr(resCons).replace("'", '"'), # change single quoting to double quoting
        'pumpCons'       : repr(pumpCons).replace("'", '"') # change single quoting to double quoting
    }

    template = loader.get_template('main/map.html')
    return HttpResponse(template.render(data, req))

@login_required(login_url='/login')
def reservoirList (req) :
    """
    Returns the page with the list of reservoirs
    """

    reservoirs = []
    islands    = []
    counties   = []
    try:
        reservoirs = Reservoir.objects.all()
        islands    = reservoirs.order_by().values_list('island', flat=True).distinct()
        counties   = reservoirs.order_by().values_list('county', flat=True).distinct()

        for r in reservoirs :
            r.setTemplateValues()
            # get the data from the last measurement from this reservoir
            try :
                r.lastMeasurement_ = Measurement.objects.filter(reservoir_id=r.res_id).latest('dateTime')
                r.waterVolume_     = lastMeasurement_.waterVolume()
            except Measurement.DoesNotExist :
                r.lastMeasurement_ = None
                r.waterVolume_ = 'Sem medições'

    except Exception as e:
        print("[reservoirList] couldn't get reservoir data: {}".format(e))

    template = loader.get_template('main/reservoirs_list.html')
    data = {
        'islands': islands,
        'counties': counties,
        'reservoirs': reservoirs
    }
    return HttpResponse(template.render(data, req))


@login_required(login_url='/login')
def reservoirDetailedInfo (req) :
    """
    Returns detailed information about the a reservoir and today's measurements
    """

    reservoirId = req.GET['id']
    try:
        reservoir = Reservoir.objects.get(res_id=reservoirId)
        reservoir.setTemplateValues()
        # get the data from the last measurement from this reservoir
        try :
            reservoir.lastMeasurement_ = Measurement.objects.filter(
                reservoir_id=reservoir.res_id).latest('dateTime')
            reservoir.waterVolume_     = '{:.2f}'.format(reservoir.lastMeasurement_.waterVolume())
        except Measurement.DoesNotExist :
            reservoir.lastMeasurement_ = None
            reservoir.waterVolume_ = 'Sem medições'
        inputs  = InputPoint.objects.filter(reservoir_id=reservoir.res_id).values()
        outputs = OutputPoint.objects.filter(reservoir_id=reservoir.res_id).values()
    except Reservoir.DoesNotExist as e:
        print('[reservoirDetailedInfo] data for reservoir {} not found: {}'.format(reservoirId, e))
        raise Htt404('Dados de reservatório não foram encontrados')

    data = {
        'reservoirState': reservoir, # will contain water level info, etc.
        'reservoir': json.dumps(model_to_dict(reservoir)), # won't contain current waterLevel, etc.
        'inputs': json.dumps(list(inputs)),
        'outputs': json.dumps(list(outputs)),
    }

    template = loader.get_template('main/reservoir_info.html')
    return HttpResponse(template.render(data, req))


@login_required(login_url='/login')
def measurementData (req) :
    data       = req.GET['data']
    dateFrom   = req.GET['dateFrom']
    dateUntil  = req.GET['dateUnitl']
    clusterBy  = req.GET['clusterBy']

    # return JSON values
    measurements = Measurement.get(data, clusterBy, dateFrom, dateUntil)
    return HttpResponse(json.dumps(list(measurements)))
