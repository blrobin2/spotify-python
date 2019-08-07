from flask import Flask, render_template

from api import get_top_ten_artists

app = Flask(__name__)


@app.route('/top-ten/<username>', methods=['GET'])
def top_ten_artists(username):
    artists = get_top_ten_artists(username)
    return render_template(
        'top-ten.html',
        username=username,
        artists=artists
    )
