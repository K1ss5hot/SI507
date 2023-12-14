from collections import defaultdict, deque
from cache_gen import *


class Graph:
    def __init__(self):
        self.adjacency_list = defaultdict(set)

    def add_edge(self, node1, node2):
        self.adjacency_list[node1].add(node2)
        self.adjacency_list[node2].add(node1)

def build_graph(movies):
    graph = Graph()
    genre_map = defaultdict(set)

    for movie in movies:
        for genre in movie['genre_ids']:
            genre_map[genre].add(movie['id'])

    for genre_movies in genre_map.values():
        for movie1 in genre_movies:
            for movie2 in genre_movies:
                if movie1 != movie2:
                    graph.add_edge(movie1, movie2)

    return graph


def bfs_top(graph, movies, top_n, rubric):
    visited, all_movies = set(), []
    movie_dict = {movie['id']: movie for movie in movies}

    for movie_id in movie_dict:
        if movie_id not in visited:
            queue = deque([movie_id])
            visited.add(movie_id)

            while queue:
                current_id = queue.popleft()
                current_movie = movie_dict[current_id]
                all_movies.append(current_movie)

                for adj_id in graph.adjacency_list[current_id]:
                    if adj_id not in visited:
                        queue.append(adj_id)
                        visited.add(adj_id)

    # Sort all movies by vote_average and select the top n
    all_movies.sort(key=lambda x: x[rubric], reverse=True)
    return all_movies[:top_n]


def bfs_top_rated_by_genre(graph, movies, top_n, genre_id):
    visited, genre_specific_movies = set(), []
    movie_dict = {movie['id']: movie for movie in movies}

    for movie_id in movie_dict:
        if movie_id not in visited:
            queue = deque([movie_id])
            visited.add(movie_id)

            while queue:
                current_id = queue.popleft()
                current_movie = movie_dict[current_id]

                # Check if the current movie belongs to the specified genre
                if genre_id in current_movie['genre_ids']:
                    genre_specific_movies.append(current_movie)

                for adj_id in graph.adjacency_list[current_id]:
                    if adj_id not in visited:
                        queue.append(adj_id)
                        visited.add(adj_id)

    # Sort movies in the specified genre by vote_average and select the top n
    genre_specific_movies.sort(key=lambda x: x['vote_average'], reverse=True)
    return genre_specific_movies[:top_n]


def bfs_top_rated_by_year(graph, movies, top_n, release_year):
    visited, year_movies = set(), []
    movie_dict = {movie['id']: movie for movie in movies}

    # Filter movies by the specified release year
    filtered_movies = {mid: mv for mid, mv in movie_dict.items() if mv['release_date'].startswith(str(release_year))}

    for movie_id in filtered_movies:
        if movie_id not in visited:
            queue = deque([movie_id])
            visited.add(movie_id)

            while queue:
                current_id = queue.popleft()
                current_movie = movie_dict[current_id]
                year_movies.append(current_movie)

                for adj_id in graph.adjacency_list[current_id]:
                    if adj_id in filtered_movies and adj_id not in visited:
                        queue.append(adj_id)
                        visited.add(adj_id)

    # Sort movies in the specified year by vote_average and select the top n
    year_movies.sort(key=lambda x: x['vote_average'], reverse=True)
    return year_movies[:top_n]


def main():

    print("\nWelcome! How are you doing today? :)")
    print("I can help with you with the following aspects:\n"
          "A: Get you the week trending movie list\n"
          "B: Get you the top rated movie list of all kinds\n"
          "C: Get you the top rated movie list based on genres\n"
          "D: Get you the top rated movie list based on release data\n")


    while True:
        choice = input("\nPlease choose one from above (A,B,C,D):")
        if choice.lower() == "a":
            print("\nI will provide the TOP 10 popular movies in this week with their basic info")
            content = open_cache(CACHE_TREND_WEEK)
            movie_graph = build_graph(content["results"])
            top_10_movies = bfs_top(movie_graph, content["results"], 10, "popularity")
            for element in top_10_movies:
                print("\n")
                print(f"Popularity: {element['popularity']}\n"
                      f"Title: {element['title']}\n"
                      f"Release Data: {element['release_date']}\n"
                      f"Overview: {element['overview']}\n")

        if choice.lower() == "b":
            print("\nI will provide the top rated movies of all time and kinds")
            number = int(input("Please enter how many movies in the list you want to show? "))
            content = open_cache(CACHE_RATED)
            movie_graph = build_graph(content["results"])
            top_movies = bfs_top(movie_graph, content["results"], number, "vote_average")
            print(f"Here are your TOP {number} movies of all time and kinds:")
            for element in top_movies:
                print("\n")
                print(f"Rate: {element['vote_average']}\n"
                      f"Rate_count: {element['vote_count']}\n"
                      f"Title: {element['title']}\n"
                      f"Release Data: {element['release_date']}\n"
                      f"Overview: {element['overview']}\n")


        if choice.lower() == "c":
            print("\nI will provide the top rated movies based on genres you provided")
            print("Below are the avaliable genres in my database: \n")
            genre = open_cache(CACHE_GENRES)
            content = open_cache(CACHE_RATED)
            for element in genre["genres"]:
                print(element["name"])

            genre_name = input("Please choose the genre you want: ")
            number = int(input("Please enter how many movies in the list you want to show? "))
            for element in genre["genres"]:
                if genre_name.lower() == element["name"].lower():
                    genre_id = element["id"]
                    break
            movie_graph = build_graph(content["results"])
            top_movies = bfs_top_rated_by_genre(movie_graph, content["results"], number, genre_id)
            for element in top_movies:
                print("\n")
                print(f"Rate: {element['vote_average']}\n"
                      f"Rate_count: {element['vote_count']}\n"
                      f"Genre: {genre_name}\n"
                      f"Title: {element['title']}\n"
                      f"Release Data: {element['release_date']}\n"
                      f"Overview: {element['overview']}\n")

        if choice.lower() == "d":
            print("\nI will provide the top rated movies based on release year")
            year = input("Please enter the year of movies you want to look for: ")
            number = int(input("Please enter how many movies in the list you want to show? "))
            content = open_cache(CACHE_RATED)
            movie_graph = build_graph(content["results"])
            top_movies = bfs_top_rated_by_year(movie_graph, content["results"], number, year)
            for element in top_movies:
                print("\n")
                print(f"Rate: {element['vote_average']}\n"
                      f"Rate_count: {element['vote_count']}\n"
                      f"Genre: {element['release_date'][:4]}\n"
                      f"Title: {element['title']}\n"
                      f"Release Data: {element['release_date']}\n"
                      f"Overview: {element['overview']}\n")


        if choice.lower() not in ['a', 'b', 'c', 'd']:
            print("Sorry. You have entered the wrong thing")

        ans = input("\nYou want to continue or exit? (y for continue; n for exit): ")
        if ans.lower() == 'y':
            continue
        if ans.lower() == 'n':
            print("THANK YOU !\n" "HAVE A GOOD DAY!\n")
            break

if __name__ == "__main__":
    main()
