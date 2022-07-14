# Trucks and Packages - a REST API supported by Google Cloud Platform (GCP)

## Description

The Trucks and Packages API allows users to act as managers of their own shipping and delivery service, by managing delivery trucks and the packages assigned to them. Truck Managers are first requested to authenticate themselves in order to receive an individualized token, which can then be used to create truck and package resources, view those resources, assign and unassign packages to specific trucks, and remove truck and package resources when they are no longer needed.

### Technologies Used

1. Python
2. Flask & Jinja2
3. Auth0 (for authentication and supplies JWT for authorization)
4. Google Cloud Platform (PaaS for deployment)
5. Google Cloud Datastore
6. Gunicorn (Web Server Gateway Interface)
7. Postman (for testing)

### Challenges and Future Changes

The stakeholder requirements indicated the Google Cloud Datastore was the required persistence mechanism for the project. While this document-based style of persistence makes it easy to transform the document objects into JSON objects and they provide horizontal scaling, we ran into the infamous N + 1 query problem during implementation of this project. Although the project currently has very little users, if the user population were to increase with a parallel increase in truck and package resources, we would need to determine if it's possible to mitigate the N + 1 query problem with the Google Cloud Datastore or look into a different persistence solution entirely. In the meantime a workaround was implemented where if one object had a relation to another object, the first object will simply store the second object's ID as a string within a data structure. Then only specific services would be responsible for whether or not the related objects would also be pulled when a query is made for the original object.

Future changes would also include pytest supported unit tests for the inner domain and services core of the application.