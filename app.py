from flask import Flask, jsonify

from api import get_top_ten_artists

app = Flask(__name__)


@app.route('/api/artists/top-ten/', methods=['GET'])
def top_ten_artists():
    top_ten = get_top_ten_artists('blrobin2')
    return jsonify({"data": top_ten})
