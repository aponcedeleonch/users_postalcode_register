# App for registering users through their postal code.

The objective of the project was to build an endpoint to register users and their postal codes. The city of the users
can be inferred using their postal code. The endpoints needed to accept and respond in JSON format. To develop this
project I used Django REST framework.

Django REST framework is a highly scalable and popular framework meant to build JSON APIs. The advantage of it being
scalable is that once it is setup more endpoints can be added with relatively small effort. On the other hand, since
the framework is popular it makes it easy to find support on the internet for it and it is being constantly mantained.

For any questions please contact: aponcedeleonch@gmail.com

## Prerequirements.

1.  Developed and tested under [Python](https://www.python.org/).
    ```sh
    $ python --version
    Python 3.9.16
    ```

2.  This project uses [geonames](https://www.geonames.org/) API to lookup the cities of the users based on the postal
    code. There needs to be a registred user to use freely the geonames API. Follow the instructions to create a
    registered user from [here](https://www.geonames.org/export/web-services.html). Specify the created username in
    an `.env` file. This file needs to be located at the same lavel as the `manage.py`file. Sample `.env` file:
    ```sh
    GEONAMES_USERNAME=geoonames_username
    ```

## Installation.

1.  (Optional) Create a [virtual environment](https://docs.python.org/3/library/venv.html).
2.  Install the package.
    ```sh
    $ pip install -e .
    ```
    The last command will install all the required dependencies. Including [Django](https://www.djangoproject.com/) and
    [Django REST framework](https://www.django-rest-framework.org/).

3.  Once everything is installed run the Django migrations. This step will create the database and the required tables.
    ```sh
    $ python manage.py makemigrations
    $ python manage.py migrate
    ```

## Run the server.

Django comes with a small server for testing. To run the server:
```sh
$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 01, 2023 - 12:22:09
Django version 4.2, using settings 'users_postalcode_register.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Available endpoints.

Once the server is running the following endpoints are available.
-   `GET /users/`. Retrieve all the available users in the DB.
-   `POST /users/`. Create a new user using a JSON. Sample JSON:
    ```json
    {
        "username": "sherpa.ai",
        "postal_code": "01008"
    }
    ```
    The API will respond with a status code 201 and the created object if the request was successful. Example:
    ```json
    {
        "id": 1,
        "username": "sherpa.ai",
        "postal_code": "01008",
        "city": "Gasteiz / Vitoria"
    }
    ```
-   `GET /users/<id>/`. Retrieve a single user from the DB.
