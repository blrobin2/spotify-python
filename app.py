from flask import Flask, jsonify, make_response, render_template

from api import Api
from helpers import to_csv_response

app = Flask(__name__)


@app.route('/api/top-ten/<username>')
def top_ten_artists_json(username):
    artists = Api(username).get_top_ten_artists()
    return jsonify({'data': artists})


@app.route('/csv/top-ten/<username>')
def top_ten_artists_csv(username):
    artists = Api(username).get_top_ten_artists()
    return to_csv_response(artists, 'top-ten')


@app.route('/top-ten/<username>')
def top_ten_artists(username):
    return render_template(
        'top-ten.html',
        username=username
    )
