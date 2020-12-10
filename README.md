# Casting Agency Project

This project is simple api for Actors and Movies to be used for the front end software of a fictitious casting agency. The goal of this project is two fold:

1. To create a great easy to use API that handles request efficiently and error gracefully.
2. To apply and show my skills as a Full Stack Developer by accomplishing goal 1.

All code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development

You will need `python`, `pip`, and `postgresql` installed in your local machine in order to run this project.

## Database Setup

With Postgres running, restore a database using the casting_db.pgsql file provided. From the backend folder in terminal run:

```
psql casting_db < casting_db.pgsql
```

#### Backend

If you don't have `pipenv` installed yet you can do so by running the following command `pip install pipenv`

We use `pipenv` as our virtual environment and dependency manager of choice but you are welcomed to use your preferred one.

From the backend folder run `pipenv shell`. This will create a new virtual environment and install all the needed dependencies listed in the Pipfile.

To run the application run the following commands in your environment :

```
export FLASK_APP=src/api.py
flask run
```

The application will run on `http://127.0.0.1:5000/`

### Testing

In order to run the test you will need to run the following commands from the `/src` folder:

```
dropdb casting_db_test //ommit when running for the first time
createdb casting_db_test
psql casting_db_test < casting_db.pgsql
python test_api.py
```

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
- 403 Forbidden
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

- Creates a new actor using the submitted name, DOB (date of birth), gender (male, female, or other), and movies (list of id(s) of movies to add the user too).
- The request body should be a JSON object and come in the following schema:

  ```
  {
      "name": {"type": "string"},
      "DOB": {"type": "string"}, // Date must be in iso format: "YYYY-MM-DD"
      "gender": {"type": "string"}, // Must be either 'male', 'female', or 'other'
      "movies": ["type": "integer"], // List of IDs of movies to add (optional)
  }
  ```

  - Note: all fields are required except "movies" or else an error response will be returned

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

- Patches the actor matching the id provided. As POST, it takes the following data: name, DOB (date of birth), gender (male, female, or other), and movies (list of id(s) of movies to add the user too).
- The request body should be a JSON object and come in the following schema:

  ```
  {
      "name": {"type": "string"},
      "DOB": {"type": "string"}, // Date must be in iso format: "YYYY-MM-DD"
      "gender": {"type": "string"}, // Must be either 'male', 'female', or 'other'
      "movies": ["type": "integer"], // List of IDs of movies to add (optional)
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

#### DELETE `/actors/{int:question_id}`

- Deletes the actor matching the id provided else returns a 404 error. Returns the `actor_id` of the deleted question.

- Request:
  ```
  curl -X DELETE http://127.0.0.1:5000/actors/25
  ```
- Response:
  ```
  {
    "id": 25,
    "success": true
  }
  ```

## Deployment N/A

## Authors

Alejandro Guillamon

## Acknowledgements

The team at Udacity and Auth0
