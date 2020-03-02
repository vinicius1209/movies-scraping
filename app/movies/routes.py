from app import app
from . import movie_bp
from .movie import TheMovieDB
from .cache import Cache, CacheItem
from flask import render_template, request, redirect

# The Movie API
themovie = TheMovieDB('1f54bd990f1cdfb230adb312546d765d')
# Cache pages
cache = Cache(20, app.config['EXPIRE_MINUTE'])

@movie_bp.route('/', methods=['GET'])
@movie_bp.route('/upcoming', methods=['GET'])
@movie_bp.route('/upcoming/', methods=['GET'])
@movie_bp.route('/upcoming/<int:page>', methods=['GET'])
def upcoming(page=1):
    
    if "search" in request.args:

        search_query = request.args.get('search', '')
        upcoming_list = themovie.get_upcoming_movies_by_search(1, search_query)
        return render_template('upcoming.html', 
            title='Upcoming Movies', upcoming_list=upcoming_list, page=page, total_pages=themovie.search_total_pages) 

    if cache.get_item(page) is None:
             
        upcoming_list = themovie.get_upcoming_movies(page)

        if themovie.total_pages > cache.length:
            cache.length = themovie.total_pages

        upcoming_cache = CacheItem(page, upcoming_list)
        cache.insert(upcoming_cache)
    
    return render_template('upcoming.html', 
        title='Upcoming Movies', upcoming_list=cache.get_item(page).movie_list, page=page, total_pages=themovie.total_pages) 

