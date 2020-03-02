from . import movie_bp
from .movie import TheMovieDB
from flask import jsonify, render_template, abort

themovie = TheMovieDB('1f54bd990f1cdfb230adb312546d765d')

@movie_bp.route('/upcoming', methods=['GET'])
@movie_bp.route('/upcoming/', methods=['GET'])
@movie_bp.route('/upcoming/<int:page>', methods=['GET'])
def upcoming(page=1):
    upcoming_list = themovie.get_upcoming_movies(page)
    return render_template('upcoming.html', title='Upcoming Movies', upcoming_list=upcoming_list) 

