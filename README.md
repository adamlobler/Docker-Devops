# DOCKER

- Docker is a tool to run applications in an isolated environment

- Advantages are similar running your application in a virtual machine but it runs containers that are not a full virtual machine

<img width="700" alt="screenshot 2018-10-27 at 12 53 57" src="https://user-images.githubusercontent.com/31661071/47603096-7184c700-d9e7-11e8-9cb0-e59dca5b4b44.png">


## Setup Docker
1. Install Docker on your local machine [Install tutorial (for Mac)](https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-for-mac)
2. Create a Dockerfile (Dockerfile = set of instructions of how Docker will build the container image)
3. Build an image from Dockerfile
4. Run Docker

### Dockerfile:
- Dockerfile has no extension
- Add it to your project root directory

The first instruction is what image we want to base our container on

`FROM python:3.6`

The enviroment variable ensures that the python output is set straight to the terminal with out buffering it first

`ENV PYTHONUNBUFFERED 1`

create root directory for our project in the container

`RUN mkdir /cogito_backend`

Set the working directory to this directory

`WORKDIR /cogito_backend`

Copy the current directory contents into the container

`ADD . /cogito_backend/`

Install any needed packages specified in requirements.txt

`RUN pip install -r requirements.txt`

`RUN pip install django-cors-headers`

### Run docker:

Build an image from this Dockerfile

`docker build -t cogito-backend .`

`docker run cogito-backend`

## Docker compose

For defining and running multi-container Docker applications.
(check if you have installed Docker composer `docker-compose -v`)

### docker-compose.yml

Version of Docker composer

`version: "3"`



`services:`

  `web:`

Tells Docker compose to build an image from the files in the project root directory

    `build: .`

The default command that will be executed when Docker runs the container image.

    `command: bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"`

Assigns a name for the container.

    `container_name: music_service`

Mounts the project root directory to the container.

    `volumes:`

      `- .:/music_service`

Expose the port we want to access the container

    `ports:`

      `- "8000:8000"`

### Build and run the conationer

`docker-compose up .`

If the build is successful you can access the container in the browser

`127.0.0.1:8000`

### Linkek:

[Learn Docker](https://www.youtube.com/watch?v=YFl2mCHdv24)

[VMs vs Docker containers](https://www.youtube.com/watch?v=TvnZTi_gaNc)

[Docker hub: python](https://hub.docker.com/_/python/)

[Dockerizing how to](https://medium.com/backticks-tildes/how-to-dockerize-a-django-application-a42df0cb0a99)

[Dockerize your Phyton Application tutorial](https://runnable.com/docker/python/dockerize-your-python-application)
