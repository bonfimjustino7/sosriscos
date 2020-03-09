import json

from flask import Flask, render_template, abort, request, redirect
from config import Config
#from flask_mongoengine import MongoEngine
from firebase import firebase
import pygeoip

firebase = firebase.FirebaseApplication('https://sosriscos.firebaseio.com/', None)
app = Flask(__name__)
app.config.from_object(Config)
app.debug = True

#geo = pygeoip.GeoIP('GeoLiteCity.dat', pygeoip.MEMORY_CACHE)



@app.route("/")
def index():
    return render_template('index.html')


# @app.route("/<school_code>")
# def show_school(school_code):
#     school = schools_by_key.get(school_code)
#     if school:
#         return render_template('map.html', school=school)
#     else:
#         abort(404)

# @app.route('/localization')
# def my_localization():
#     client_id = request.remote_addr
#     geo_data = geo.record_by_addr('179.124.6.124')
#     return json.dumps(geo_data, indent=2) + '\n'

@app.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar_denunica():
    if request.method == 'POST':
        lugar = request.values.get('lugar')
        descricao = request.values.get('descricao')
        latitude = request.values.get('latitude')
        longitude = request.values.get('longitude')
        if lugar and descricao and latitude and longitude:
            result = firebase.post('/sosriscos', {'lugar': lugar, 'descricao': descricao, 'latitude': latitude, 'longitude':longitude})
            print(result)
            return redirect('/points')

    return render_template('cadastrar.html')

@app.route('/points/create')
def create_point():
    result = firebase.post('/sosriscos', {'lat': -6.5780434, 'long': -39.2486159})
    return result

@app.route('/points')
def show_points():
    points = []
    result = firebase.get('sosriscos', '')
    for point in result.items():
        points.append(point[1])

    return render_template('points_example.html', points=points)