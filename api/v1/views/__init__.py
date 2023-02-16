#!/usr/bin/python3
"""import the views and the blueprint"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
<<<<<<< HEAD
from api.v1.views.index import *
<<<<<<< HEAD
=======
=======
>>>>>>> fd28931a0ae5c832736c1264b99dd4a7f3392cca

from api.v1.views.index import *
from api.v1.views.states import *
