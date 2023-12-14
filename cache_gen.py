import requests
import json

CACHE_TREND_WEEK = "cache_week.json"
CACHE_GENRES = "cache_genre.json"
CACHE_RATED = "cache_rated.json"

def open_cache(CACHE):
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict, CACHE):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict, indent=4)
    fw = open(CACHE,"w")
    fw.write(dumped_json_cache)
    fw.close()


def search_API_OMDB():
    # set base URL and the API-specific parameters
    base_url = "http://www.omdbapi.com/"
    params = {
        "apikey": "c7a317d4",
        # "s": "James Bond",
        # "type":"movie"
        # "y":"2023"
    }
    response = requests.get(base_url, params=params)
    return response

def search_API_TMDB(url):
    # set base URL and the API-specific parameters
    base_url = url
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjNmE1OTU4MDQ0YzBmYmM5OWM2ZDZiYWFjYWE4YTk5MSIsInN1YiI6IjY1NzgwNjk0ZTkzZTk1MjE4ZWFiMTk0YSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.h1ag1tBS2Uzinnw6IAIMmqENAJ8uM4Idckt2_RUIHZg"
    }

    response = requests.get(base_url, headers=headers)
    return response

def cache(url, CACHE):
    results = search_API_TMDB(url)
    print(results.url)
    results_dic = results.json()
    save_cache(results_dic,CACHE)

def main():
    url_genre = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    cache(url_genre, CACHE_GENRES)

    url_popular = "https://api.themoviedb.org/3/trending/movie/week?language=en-US"
    cache(url_popular, CACHE_TREND_WEEK)

    results_rated = {"results":[]}
    for i in range(1,250):
        url_rated = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={i}"
        results_dic = search_API_TMDB(url_rated).json()
        results_rated["results"] = results_rated["results"] + results_dic["results"]

    save_cache(results_rated,CACHE_RATED)


if __name__ == "__main__":
    main()
