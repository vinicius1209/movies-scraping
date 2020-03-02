import requests
import shutil
import json
import os
from os.path import join, dirname, realpath

class TheMovieDB():

    def __init__(self, api_key):
        self.api_key = api_key
        self.movie_list = []
        self.genre_dict = {}
        self.total_pages = None
        self.total_results = None
        self.search_list = []
        self.search_total_pages = None
        self.search_total_results = None
        self.upload_folder = join(dirname(realpath(__file__)), 'static/img/')

    def get_upcoming_movies(self, page):
        try:
            r = requests.get('https://api.themoviedb.org/3/movie/upcoming?api_key={}&page={}'.format(self.api_key, page))
            if r.status_code == 200:
                
                movies_json = r.json()
                # update page and results
                self.total_pages = movies_json["total_pages"]
                self.total_results = movies_json["total_results"]
                self.movie_list = []
                self.genre_dict = self.get_genre_dict()

                for movie in movies_json["results"]:
                    
                    g_list = []

                    for g in movie["genre_ids"]:
                        g_list.append(self.genre_dict[g])

                    # Check if img path is null
                    poster_path = ("null.jpg" if movie["poster_path"] is None else str(movie["poster_path"])[1:])

                    self.movie_list.append(Movie(
                        movie["id"],
                        movie["original_title"],
                        poster_path,
                        g_list,
                        movie["release_date"],
                        movie["overview"],
                        movie["popularity"]
                    ))
                    self.create_poster_img(poster_path)

                return self.movie_list
            
        except ConnectionError as c:
            return "Connection Error: {}".format(c)
        except Timeout as t:
            return "Timeout Error: {}".format(t)

    def create_poster_img(self, path):
        try:
            r = requests.get('https://image.tmdb.org/t/p/original/{}'.format(path), stream=True)
            if r.status_code == 200:
                try:
                    poster_img = open(self.upload_folder + path, 'wb')
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, poster_img)
                    poster_img.close()
                except Exception as e:
                    return e
        except ConnectionError as c:
            return "Connection Error: {}".format(c)
        except Timeout as t:
            return "Timeout Error: {}".format(t)
    
    def get_genre_dict(self):
        try:
            r = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key={}'.format(self.api_key))
            if r.status_code == 200:
                genre_json = r.json()
                
                # update genre dict
                for genre in genre_json["genres"]:
                    self.genre_dict[genre["id"]] = genre["name"]
                
                return self.genre_dict

        except ConnectionError as c:
            return "Connection Error: {}".format(c)
        except Timeout as t:
            return "Timeout Error: {}".format(t)

    def get_upcoming_movies_by_search(self, page, search_query):
        try:
            r = requests.get('https://api.themoviedb.org/3/search/movie?api_key={}&page={}&query={}'.format(self.api_key, page, search_query))
            if r.status_code == 200:
                search_json = r.json()
                self.search_list = []
                self.search_total_pages = search_json["total_pages"]
                self.search_total_results = search_json["total_results"]
                self.genre_dict = self.get_genre_dict()

                for movie in search_json["results"]:
                    
                    g_list = []

                    for g in movie["genre_ids"]:
                        g_list.append(self.genre_dict[g])

                    # Check if img path is null
                    poster_path = ("null.jpg" if movie["poster_path"] is None else str(movie["poster_path"])[1:])

                    self.search_list.append(Movie(
                        movie["id"],
                        movie["original_title"],
                        poster_path,
                        g_list,
                        movie["release_date"],
                        movie["overview"],
                        movie["popularity"]
                    ))
                    self.create_poster_img(poster_path)

                return self.search_list

        except ConnectionError as c:
            return "Connection Error: {}".format(c)
        except Timeout as t:
            return "Timeout Error: {}".format(t)


class Movie(object):
    
    def __init__(self, id, name, poster, genre, release_date, overview, popularity):
        self.id = id
        self.name = name
        self.poster = poster
        self.genre = genre
        self.release_date = release_date
        self.overview = overview
        self.popularity = popularity

