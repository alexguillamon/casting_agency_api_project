# Casting Agency Project

This project is simple api for Actors and Movies to be used for the front end software of a fictitious casting agency. The goal of this project is two fold:

1. To create a great easy to use API that handles request efficiently and error gracefully.
2. To apply and show my skills as a Full Stack Developer by accomplishing goal 1.

All code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development

You will need `python`, `pip`, and `postgresql` installed in your local machine in order to run this project.

## Environment

If you don't have `pipenv` installed yet you can do so by running the following command `pip install pipenv`

We use `pipenv` as our virtual environment and dependency manager of choice but you are welcomed to use your preferred one.

From the backend folder run `pipenv shell`. This will create a new virtual environment and install all the needed dependencies listed in the Pipfile.

### Environment Variables

In `settings.py` you will find an empty .env file named `.env.empty`. Fill the empty variables with the respective data and change the file name to `.env`.

## Authentication and Authorization

This API requires authentication and authorization through JWT. This is implemented using Auth0.

The following are the different permissions and the different access they have to the endpoints:

- Casting Assistant:

  - /actors `GET`
  - /movies `GET`

- Casting Director:

  - All permissions a Casting Assistant has and…
  - /actors `POST`, `PATCH` and `DELETE`
  - /movies `PATCH`

- Executive Producer:
  - All permissions a Casting Director has and…
  - /movies `POST` and `DELETE`

To receive the needed tokens to run the tests, please contact me.

## Testing

In order to run the test you will need to run the following commands from the `/src` folder:

```
python test_api.py
```

## Database Setup

With Postgres running, restore a database using the casting_db.pgsql file provided. From the backend folder in terminal run:

```
psql casting_db < casting_db.pgsql
```

## Running the API

After the instructions above have been folowed, you can run the application as follows:

```
export FLASK_APP=api.py
flask run
```

The application will run on `http://127.0.0.1:5000/`

## Deployment

This application is deployed with Heroku to this url: https://casting-agency-api.herokuapp.com/

To deploy changes to the production make a pull request to production if accepted it will be committed and the deploy will start.

## API Reference

### Getting Started

- Base URL: At present this app is not deployed to a remote server and can only be run locally. The base url for the API is `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return the following error types when requests fail:

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error

### Endpoints

#### GET `/actors`

- Fetches a list actors. When fetching a list of actors the list will be paginated 100 at a time.
- Request Arguments:

  - Optional:

    ```
    ?page=<int:page_number>
    ```

- Request:

  ```
  curl http://127.0.0.1:5000/actors
  ```

  - Note: `page` argument will default to 1

  ```
  curl http://127.0.0.1:5000/actors?page=3
  ```

- Response:

  ```
  {
  "actors": [
    {
      "DOB": "Thu, 10 Dec 2020 00:00:00 GMT",
      "gender": "male",
      "id": 1,
      "movies": [
        {
          "id": 1,
          "release_date": "2020-12-10",
          "title": "The Movie"
        }
      ],
      "name": "jake"
    },
    {
      "DOB": "Thu, 10 Dec 2020 00:00:00 GMT",
      "gender": "female",
      "id": 2,
      "movies": [
        {
          "id": 2,
          "release_date": "2020-12-10",
          "title": "The Not Movie"
        }
      ],
      "name": "vic"
    },
    {
      "DOB": "Thu, 10 Dec 2020 00:00:00 GMT",
      "gender": "other",
      "id": 3,
      "movies": [
        {
          "id": 3,
          "release_date": "2020-12-10",
          "title": "The Third Movie"
        }
      ],
      "name": "ella"
    },
    {
      "DOB": "Thu, 10 Dec 2020 00:00:00 GMT",
      "gender": "male",
      "id": 4,
      "movies": [],
      "name": "pedro"
    }
  ],
  "page": 1,
  "page_count": 1,
  "success": true,
  "total_actors": 4
  }

  ```

#### POST `/actors`

- Creates a new actor using the submitted `name`, `DOB` (date of birth), `gender` (male, female, or other), and `movies` (list of id(s) of movies to add the user too).
- The request body should be a JSON object and come in the following schema:

  ```
  {
      "name": {"type": "string"},
      "DOB": {"type": "string"}, // Date must be in iso format: "YYYY-MM-DD"
      "gender": {"type": "string"}, // Must be either 'male', 'female', or 'other'
      "movies": [
        "type": "list",
        "children": "int"
      ], // List of IDs of movies (optional)
  }
  ```

  - Note: all fields are required except `movies` or else an error response will be returned

- Returns an JSON object:
  ```
  {
      "id": Int,
      "success": Boolean
  }
  ```
- Request:
  ```
  curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{"name":"alejandro", "DOB":"1990-12-12", "gender":"male"}'
  ```
- Response:

  ```
  {
      "id": 25,
      "success": true
  }
  ```

  #### PATCH `/actors/{int:actor_id}`

- Patches the actor matching the id provided. As POST, it takes the following data: `name`, `DOB` (date of birth), `gender` (male, female, or other), and `movies` (list of id(s) of movies to add the user too).
- The request body should be a JSON object and come in the following schema:

  ```
  {
      "name": {"type": "string"},
      "DOB": {"type": "string"}, // Date must be in iso format: "YYYY-MM-DD"
      "gender": {"type": "string"}, // Must be either 'male', 'female', or 'other'
      "movies": [
        "type": "list",
        "children": "int"
      ], // List of IDs of movies (optional)
  }
  ```

  - Note: all fields are optional as this is a PATCH request

- Returns an JSON object:
  ```
  {
      "success": Boolean
  }
  ```
- Request:
  ```
  curl http://127.0.0.1:5000/actors/1 -X PATCH -H "Content-Type: application/json" -d '{"name":"New Name", "movies":[1] }'
  ```
- Response:
  ```
  {
      "success": true
  }
  ```

#### DELETE `/actors/{int:actor_id}`

- Deletes the actor matching the id provided else returns a 404 error. Returns the `actor_id` of the deleted question.

- Request:
  ```
  curl -X DELETE http://127.0.0.1:5000/actors/25
  ```
- Response:
  ```
  {
    "success": true
  }
  ```

#### GET `/movies`

- Fetches a list movies. When fetching a list of movies the list will be paginated 100 at a time.
- Request Arguments:

  - Optional:

    ```
    ?page=<int:page_number>
    ```

- Request:

  ```
  curl http://127.0.0.1:5000/movies
  ```

  - Note: `page` argument will default to 1

  ```
  curl http://127.0.0.1:5000/movies?page=3
  ```

- Response:

  ```
  {
  "movies": [
    {
      "cast": [
        {
          "DOB": "2020-12-11",
          "gender": "Gender.male",
          "id": 1,
          "name": "jake"
        }
      ],
      "id": 1,
      "release_date": "Fri, 11 Dec 2020 00:00:00 GMT",
      "title": "The Movie"
    },
    {
      "cast": [
        {
          "DOB": "2020-12-11",
          "gender": "Gender.female",
          "id": 2,
          "name": "vic"
        }
      ],
      "id": 2,
      "release_date": "Fri, 11 Dec 2020 00:00:00 GMT",
      "title": "The Not Movie"
    },
    {
      "cast": [
        {
          "DOB": "2020-12-11",
          "gender": "Gender.other",
          "id": 3,
          "name": "ella"
        }
      ],
      "id": 3,
      "release_date": "Fri, 11 Dec 2020 00:00:00 GMT",
      "title": "The Third Movie"
    }
  ],
  "page": 1,
  "page_count": 1,
  "success": true,
  "total_movies": 3
  }

  ```

#### POST `/movies`

- Creates a new movie using the submitted `title`, `release_date`, and `cast` (list of id(s) of actors).
- The request body should be a JSON object and come in the following schema:

  ```
  {
      "title": {"type": "string"},
      "release_date": {"type": "string"}, // Date must be in iso format: "YYYY-MM-DD"
      "cast": [
        "type": "list",
        "children": "int"
      ], // List of IDs of actors (optional)
  }
  ```

  - Note: all fields are required except `cast` or else an error response will be returned

- Returns an JSON object:
  ```
  {
      "id": Int,
      "success": Boolean
  }
  ```
- Request:
  ```
  curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{"name":"alejandro", "DOB":"1990-12-12", "gender":"male"}'
  ```
- Response:

  ```
  {
      "id": 25,
      "success": true
  }
  ```

  #### PATCH `/movies/{int:movie_id}`

- Patches the movie matching the id provided. As POST, it takes the following data: `title`, `release_date`, and `cast` (list of id(s) of actors).
- The request body should be a JSON object and come in the following schema:

  ```
  {
      "name": {"type": "string"},
      "DOB": {"type": "string"}, // Date must be in iso format: "YYYY-MM-DD"
      "gender": {"type": "string"}, // Must be either 'male', 'female', or 'other'
      "cast": [
        "type": "list",
        "children": "int"
      ], // List of IDs of actors (optional)
  }
  ```

  - Note: all fields are optional as this is a PATCH request

- Returns an JSON object:
  ```
  {
      "success": Boolean
  }
  ```
- Request:
  ```
  curl http://127.0.0.1:5000/actors/1 -X PATCH -H "Content-Type: application/json" -d '{"name":"New Name", "movies":[1] }'
  ```
- Response:
  ```
  {
      "success": true
  }
  ```

#### DELETE `/movies/{int:movie_id}`

- Deletes the movie matching the id provided else returns a 404 error. Returns the `movie_id` of the deleted question.

- Request:
  ```
  curl -X DELETE http://127.0.0.1:5000/movies/25
  ```
- Response:
  ```
  {
    "success": true
  }
  ```

## Authentication and Authorization

This API requires authentication and authorization through JWT. This is implemented using Auth0.

The following are the different permissions and the different access they have to the endpoints:

- Casting Assistant:

  - /actors `GET`
  - /movies `GET`

- Casting Director:

  - All permissions a Casting Assistant has and…
  - /actors `POST`, `PATCH` and `DELETE`
  - /movies `PATCH`

- Executive Producer:
  - All permissions a Casting Director has and…
  - /movies `POST` and `DELETE`

## Authors

Alejandro Guillamon

## Acknowledgements

The team at Udacity and Auth0
