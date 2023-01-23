# Menu api

#### Description

This is the implementation of the api for accessing the menu. It contains all of CRUD operations for access with menu db.

Progect based on Python and used frameworks `FastAPI` and `SQLAlchemy`. It used PostgreSQL as DMS.


#### Lanch

To run project:
 - go to `src`
 - get virtual enviroment using requirements from `requirements.txt`
 - take command `uvicorn main:app`

DB settigs based on `settings.env`. Default values:

    host: 'localhost',
    port: '5433',
    username: 'postgres',
    password: ''


#### Launch with Docker

###### To run project on Docker container:
 - go to `Docker` directory
 - tace command `docker-compose up --build`

###### To run tests:
 - go to 'Docker/tests' directory
 - build Docker container using `docker build .` command
 - run Docker container using `docker run <container_id>` command