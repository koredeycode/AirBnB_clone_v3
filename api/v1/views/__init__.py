#!/usr/bin/python3
"""import the views and the blueprint"""
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
<<<<<<< HEAD
=======

from api.v1.views.index import *
from api.v1.views.states import *
>>>>>>> b70585dfc3fe3954257fccd8178af95c8d5c47ce
