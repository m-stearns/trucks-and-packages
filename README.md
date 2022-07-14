# Trucks and Packages - a REST API supported by Google Cloud Platform (GCP) and Auth0
## Description
The Trucks and Packages API allows users to act as managers of their own shipping and delivery service, by managing delivery trucks and the packages assigned to them. Truck Managers are first requested to authenticate themselves in order to receive an individualized token, which can then be used to create truck and package resources, view those resources, assign and unassign packages to specific trucks, and remove truck and package resources when they are no longer needed.

### Technologies Used
1. Python
2. Flask & Jinja2
3. Auth0 (for user authentication and supplies JWT for authorization)
4. Google Cloud Platform (PaaS for deployment)
5. Google Cloud Datastore
6. Gunicorn (Web Server Gateway Interface)
7. Postman (for testing)

### Challenges and Future Changes
The stakeholder requirements indicated the Google Cloud Datastore was the required persistence mechanism for the project. While this document-based style of persistence makes it easy to transform the document objects into JSON objects and they provide horizontal scaling, we ran into the infamous N + 1 query problem during implementation of this project. Although the project currently has very little users, if the user population were to increase with a parallel increase in truck and package resources, we would need to determine if it's possible to mitigate the N + 1 query problem with the Google Cloud Datastore or look into a different persistence solution entirely. In the meantime a workaround was implemented where if one object had a relation to another object, the first object will simply store the second object's ID as a string within a data structure rather than the object itself. As a result, only specific services would be responsible to determine whether or not the related objects would also be pulled when a query is made for the original object.

Future changes would also include pytest supported unit tests for the inner domain and services core of the application, as well as Docker containerization.

## Installation
### Prerequisites
You'll need the following services turned on before you can run this app locally:
1. A [Google Cloud Platform (GCP) project](https://console.cloud.google.com/projectselector2/home), including:
    - Google App Engine with Cloud Build API ([click here for a simple quickstart tutorial](https://cloud.google.com/appengine/docs/standard/python3/create-app)).
    - A Google Cloud Datastore tied to your GCP project
2. Your own [Auth0 authentication and authorization application](https://auth0.com/), with the following items set:
    - Application URIs (*Note: these are specific to only your development environment*):
        - Callback URL: `http://localhost:8080/auth/callback`
        - Logout URL: `http://localhost:8080`
    - An username-password authentication database connected to your Auth0 app
### Local Development
1. Clone the repository: `git clone https://github.com/MikeyBS1987/trucks-and-packages.git`
2. Create a clean python virtual environment: `python -m venv venv`
3. Activate the virtual environment: `.\venv\Scripts\activate`
4. Update `pip` in the virtual environment: `python -m pip install --upgrade pip`
5. Install the package requirements: `python -m pip install -r requirements.txt`
6. Inside the root directory, install the package into your virtual environment (with editable mode turned on) with the following command: `python -m pip install -e .`
7. Create a `.env` file that contains the following keys and values:
```
FLASK_RUN_PORT=8080
FLASK_ENV=development
AUTH0_DOMAIN={{ your Auth0 domain URL }}
AUTH0_CLIENT_ID={{ your Auth0 client ID }}
AUTH0_CLIENT_SECRET={{ your Auth0 client secret }}
```
8. To keep the client-side sessions secure, we'll need to generate a secret key and store it in `.env`, so it can be imported by our flask application. [As recommended by the Flask documentation](https://flask.palletsprojects.com/en/2.1.x/config/), in your command line type the following command: `python -c 'import secrets; print(secrets.token_hex())`. Copy the secret key from your command line and enter the following into `.env`: `SECRET_KEY={{ your secret key}}`
8. In `.\trucksandpackages\__init__.py`, make sure the Flask app's configuration is set to use the Development configuration: `app.config.from_object(config.DevelopmentConfig())`
9. Turn on the flask application: `python -m flask run`
10. The application by default runs at the following URL, just type this into your browser and you'll be taken to the home page: `http://localhost:8080`

## How to Use Trucks and Packages API
In order to use the API, you'll need to first register a new account. In the home page, click on "create an account", which is where you'll be routed to an Auth0 user authentication feature. Create your account by providing a valid email address and password. After logging in, you will be routed back to the home page with a rendered JWT Bearer token and your unique ID. You'll need the JWT Bearer token placed into the Authorization header of your HTTP requests in order to access many of the endpoints of the API.

From there, you can perform the following actions against the Truck and Package resources in the API, including but not limited to:

- Creating trucks -> `POST /trucks`
- Viewing a specific truck -> `GET /trucks/:truck_id`
- Creating packages -> `POST /packages`
- Viewing a specific package -> `GET /packages/:package_id`
- Assign a package to a truck -> `PUT /trucks/:truck_id/packages/:package_id`
- Remove a package from a truck -> `DELETE /trucks/:truck_id/packages/:package_id`

*Note: Each resource must be prefixed with the application URL; for local development use* `http://localhost:8080`

Creation of truck and package resources are specific to the owner (you), meaning no other users will be able to manipulate the trucks and packages you create.

To create your first resource, try running a `POST` request against `http://localhost:8080/trucks` with the following JSON:

```
{
    "type": "Box truck",
    "length": 20,
    "axles": 2
}
```

Upon successful creation of the resource, you should see the following returned JSON with a status of `201 Created`:

```
{
    "id": 1234,
    "type": "Box truck",
    "length": 20,
    "axles": 2,
    "packages": [],
    "owner": "auth0|84hff7e3han0u3yans0474h3",
    "self": "https://xyz.appspot.com/trucks/1234"
}
```

### Truck Data Model Spec
- id (Integer): The id of the Truck. Datastore automatically generates it.
- type (String): Type of the Truck. E.g., Flatbed, Dry Van, Box, Tanker, etc.
- length (Integer): The length of the Truck in feet.
- axles (Integer): The number of axles on the Truck.
- owner (String): The id of the TruckManager that owns this Truck.
- packages (String[]): Stores all package_ids assigned to the specific Truck.

### Package Data Model Spec
- id (Integer): The id of the Truck. Datastore automatically generates it.
- shipping_type (String): The type of shipping for the package. E.g., ground, same-day, overnight, etc.
- weight (Decimal): The weight of the package in lbs.
- shipping_date (Date): The date the package was shipped (MM/DD/YYYY).
- carrier (String): The truck_id that the package is assigned to.

## Credits
The architecture implementation for this project was inspired by [Architecture Patterns with Python](https://www.cosmicpython.com/) by Harry Percival and Bob Gregory. The concepts of Domain modeling, Repository pattern, a Service layer, and the Unit of Work pattern can all be found within the implementation of this project. You can read this great book for free at [https://cosmicpython.com](https://www.cosmicpython.com/) thanks to the Creative Commons License CC-BY-NC-ND.

## License
This project is licensed under the GNU General Public License v3.0.