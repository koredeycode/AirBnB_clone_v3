from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """return the status of the server"""
    return (jsonify({"status": "OK"}))


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def object_count():
    """retrieves the number of each objects by type"""
    classes = {
                "amenities": Amenity, "cities": City,
                "places": Place, "reviews": Review,
                "states": State, "users": User
                }

    objects = {}
    for name, cls in classes.items():
        objects[name] = storage.count(cls)

    return (jsonify(objects))
