import json


def load_user_data(file_path):
    with open(file_path, 'r') as file:
        user_data = json.load(file)
    return user_data


def recommend_movies(username, user_data, movie_data):
    for user in user_data["users"]:
        if user["username"] == username:
            watched_movies = user["watched_movies"]
            watched_movies.sort(key=lambda x: x["rating"], reverse=True)

            if watched_movies:
                highest_rated_movie = watched_movies[0]
                highest_rated_genre = get_genre_for_movie(highest_rated_movie["name"], movie_data)

                recommended_movies = get_movies_by_genre(highest_rated_genre, user_data, highest_rated_movie["name"], movie_data)

                print(f"Recommendations for {username}:")
                for movie in recommended_movies:
                    print(f"{movie['name']} ({movie['genre']})")

                return

    print(f"User {username} not found.")


def get_genre_for_movie(movie_name, movie_data):
    for movie in movie_data["movies"]:
        if movie["name"] == movie_name:
            return movie["genre"]


def get_movies_by_genre(genre, user_data, exclude_movie_name, movie_data):
    recommended_movies = []

    # Get all movies of the same genre as the highest-rated movie
    for movie in movie_data["movies"]:
        if movie["genre"] == genre and movie["name"] != exclude_movie_name:
            recommended_movies.append({"name": movie["name"], "genre": movie["genre"]})

    return recommended_movies





if __name__ == "__main__":
    user_data = load_user_data("users.json")
    movie_data = load_user_data("movies.json")

    username_input = input("Enter the username: ")
    recommend_movies(username_input, user_data, movie_data)
