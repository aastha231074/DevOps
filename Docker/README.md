# Docker Guide: From Containers to Compose

## 1. What is Docker?

Docker is a platform designed to make it easier to create, deploy, and run applications by using containers.

Imagine your application, along with all its dependencies, libraries, and settings, being sealed inside a standardized shipping container. You can then ship this container anywhere—to a developer's machine, a testing server, or a production environment—and be confident that your application will run exactly as intended, regardless of the underlying infrastructure.

This "shipping container" is what we call a **Docker Container**.

## 2. Core Concepts

### Containers

A container is a lightweight, isolated, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries, and settings.

Think of it as a virtualized, isolated environment where your application runs without interference from other processes on the host machine.

### Images

A Docker Image is a read-only template with instructions for creating a Docker container. It's the blueprint for your application's environment. When you run an image, it becomes a container.

You can get images from a public or private Container Registry, which is a repository for storing and distributing images. The most popular public registry is Docker Hub.

Here are links to your projects on Docker Hub:
- [ares-frontend](https://hub.docker.com/repository/docker/ahastha1904/ares-frontend)
- [ares-backend](https://hub.docker.com/repository/docker/ahastha1904/ares-backend)

## 3. Essential Docker Commands

### Image Management

**`docker pull <image_name>`**: Downloads an image from a registry.
```bash
docker pull ubuntu:20.04
```

**`docker images`**: Lists all the images on your local system.

**`docker rmi <image_id>`**: Removes one or more images.

**`docker tag <source_image> <target_image>`**: Creates a tag TARGET_IMAGE that refers to SOURCE_IMAGE. This is useful for renaming an image or preparing it for pushing to a registry.
```bash
docker tag my-app:v1 ahastha1904/my-app:v1
```

### Container Management

**`docker run <image_name>`**: Creates and starts a new container from an image.

**`docker run -it <image_name>`**: The `-i` (interactive) and `-t` (tty) flags are often used together to attach your local terminal to the container's standard input and output, allowing you to interact with it.

**`docker run -p <host_port>:<container_port> <image_name>`**: The `-p` (port mapping) flag maps a port on your local machine to a port inside the container, making the application accessible from the outside.
```bash
# Map port 7990 on the host to port 80 in the container
docker run -it -p 7990:80 my-web-app:latest
```

**`docker ps`**: Lists all running containers.

**`docker ps -a`**: Lists all containers, including those that have stopped.

**`docker start <container_id>`**: Starts a stopped container.

**`docker stop <container_id>`**: Gracefully stops a running container.

**`docker rm <container_id>`**: Removes one or more containers.

**`docker exec -it <container_id> <command>`**: Runs a command inside a running container. This is useful for debugging or performing administrative tasks without having to stop the container.
```bash
# Open a bash shell inside the container
docker exec -it a1b2c3d4e5f6 bash
```

**`docker logs <container_id>`**: Fetches the logs of a container.

**`docker inspect <container_id>`**: Returns a detailed JSON object containing low-level information about a container. This gives you information about the container itself (ports, network, volumes), not the application running inside it.

## 4. Building Your Own Image with a Dockerfile

A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image. It's the blueprint for building your custom image.

### Example Dockerfile

This is a simple example for a Python web application.

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "app.py"]
```

### Building and Running an Image from a Dockerfile

**`docker build -t <image_name> .`**: Builds a Docker image from a Dockerfile. The `-t` flag tags the image with a custom name. The `.` at the end specifies the build context (the current directory).

**`docker run <image_name>`**: Once the image is built, you can run it just like any other image.

### Dockerfile Best Practices: Multi-Stage Builds

A multi-stage build is a powerful feature that allows you to create much smaller, more secure final images by separating the build environment from the runtime environment.

The first stage can contain all the tools and dependencies needed to build your application, while the second, final stage only contains the compiled application and its minimal runtime dependencies.

```dockerfile
# Stage 1: Build the application
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Create the final, lightweight image
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 5. Cleaning Up Bloat: Dangling Images and Stopped Containers

Over time, your local Docker environment can become bloated with unused images and stopped containers.

**Dangling Images** are layers of images that are no longer tagged or referenced by any image. This happens when you rebuild an image with the same name and tag (e.g., `my-app:latest`) multiple times, and the old version becomes "untagged." These old versions still take up disk space.

**Stopped Containers** are containers that have been stopped but not removed from your system. They also consume disk space and resources.

Here's how to manage the bloat:

### Remove all stopped containers:
- **`docker ps -aq`**: This command gets the IDs of all stopped containers.
- **`docker rm $(docker ps -aq)`**: This command removes all containers returned by the previous command.

### Remove all dangling images:
**`docker image prune`**: This is a simple command to remove all unused images.

### The ultimate cleanup command:
**`docker system prune`**: This is a powerful command that removes all stopped containers, all dangling images, and all unused networks and build cache. Use `-a` to also remove all unused images (not just dangling ones).
```bash
docker system prune -a
```

## 6. Docker Compose: Orchestrating Multi-Container Applications

Docker Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application's services. Then, with a single command, you create and start all the services from your configuration.

### Why use Docker Compose?

- **Reproducibility**: It allows you to define your entire application stack in a single, version-controlled file, ensuring that everyone on your team uses the same environment.
- **Simplified Startup**: Instead of running multiple `docker run` commands with complex flags, you can start your entire application with one command.
- **Service Intercommunication**: Compose creates a network for your services, allowing them to communicate with each other using their service names.

### Example docker-compose.yaml

This example defines a simple web application with a backend and a database.

```yaml
version: '3.8'

services:
  # The web application service
  web:
    build: . # Build the image from the Dockerfile in the current directory
    ports:
      - "8000:8000" # Map host port 8000 to container port 8000
    depends_on:
      - db # Ensure the database service starts first
    volumes:
      - .:/code # Mount the current directory into the container for development
    environment:
      - DATABASE_URL=mongodb://db:27017/my_app # Environment variables for the application

  # The database service
  db:
    image: mongo:4.4 # Use the official mongo image from Docker Hub
    ports:
      - "27017:27017"
    volumes:
      - db-data:/data/db # Persist data in a named volume

volumes:
  db-data: # Define the named volume for the database data
```

### Compose Commands

**`docker-compose up`**: Builds, creates, and starts all services defined in the docker-compose.yaml file. Use the `-d` flag to run in detached mode (in the background).

**`docker-compose down`**: Stops and removes all containers, networks, and volumes created by `docker-compose up`.

## Docker Volumes: Persistent Data Storage

Docker containers are designed to be ephemeral. When a container is removed, any data created inside it is also removed. To persist data, you use **Volumes**.

A volume is a file system that is hosted by Docker. It exists independently of the container's life cycle. This means data in a volume can be shared between containers and will not be lost when a container is removed.

### Why use volumes?

- **Persistence**: To ensure data like database files, user uploads, or logs are not lost when the container is stopped or removed.
- **Sharing Data**: To share data easily between multiple containers.

The example docker-compose.yaml above uses a named volume (`db-data`), which is the preferred way to persist data.

## Docker Networking: Container Communication

By default, Docker creates a bridge network that allows containers to communicate with each other using their service names.

**`docker network ls`**: Lists all networks on your system.

**`docker network create <network_name>`**: Creates a new custom bridge network.

**`docker network connect <network_name> <container_name>`**: Connects a running container to a network.

## 7. Pushing to Docker Hub

Sharing your image with the world (or your team) is straightforward.

### Tag your image:
Tag your local image with your Docker Hub username and repository name.
```bash
docker tag my-app:v1 <your_docker_hub_username>/my-app:v1
```

### Log in to Docker Hub:
```bash
docker login
```

### Push your image:
```bash
docker push <your_docker_hub_username>/my-app:v1
```

### Log out:
```bash
docker logout
```