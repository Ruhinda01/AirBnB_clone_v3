"""Create routes"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models.user import User
from models.review import Review



@app_views.route('/status', methods=["GET"], strict_slashes=False)
def status():
  """Checks the status of the api"""
  return jsonify({'status': 'OK'})

@app_views.route('/stats', methods=["GET"], strict_slashes=False)
def obj_count():
  """Retrieves the number of each objects by type"""
  classes = [Amenity, City, Place, Review, State, User]
  res = {}
  for cls_name in classes:
    obj = storage.count(cls_name)
    res[str(cls_name.__name__)] = obj
    
  return jsonify(res)
