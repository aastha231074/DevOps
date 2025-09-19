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

Here are links to my projects on Docker Hub:
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
docker tag my-app:v1 aastha1904/my-app:v1
```

### Container Management

**`docker run <image_name>`**: Creates and starts a new container from an image.

**`docker run -itd <image_name>`**: The `-it` (interactive) and `-d` (detached) flags are often used together to attach your local terminal to the container's standard input and output, allowing you to interact with it.

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

**Note**: Docker has updated their Compose tool. The modern approach is to use `docker compose` (without a hyphen) instead of `docker-compose` (with a hyphen). The new `docker compose` command is a plugin built into modern Docker installations and is the recommended way going forward.

**`docker compose up`**: Builds, creates, and starts all services defined in the docker-compose.yaml file. Use the `-d` flag to run in detached mode (in the background).

**`docker compose down`**: Stops and removes all containers, networks, and volumes created by `docker compose up`.

**`docker compose ps`**: Lists all running services in the current compose project.

**`docker compose logs`**: Shows logs from all services. You can specify a service name to see logs for just that service.

**`docker compose build`**: Builds or rebuilds services that have a `build` configuration.

**`docker compose pull`**: Pulls the latest versions of images for services that use pre-built images.

**`docker compose exec <service_name> <command>`**: Runs a command inside a running service container.

*Legacy Note*: The older `docker-compose` (with hyphen) command still works if you have the standalone Docker Compose tool installed, but Docker recommends using the newer `docker compose` (without hyphen) plugi

## Docker Volumes: Persistent Data Storage

Docker containers are designed to be ephemeral. When a container is removed, any data created inside it is also removed. To persist data, you use **Volumes**.

A volume is a file system that is hosted by Docker. It exists independently of the container's life cycle. This means data in a volume can be shared between containers and will not be lost when a container is removed.

### Why use volumes?

- **Persistence**: To ensure data like database files, user uploads, or logs are not lost when the container is stopped or removed.
- **Sharing Data**: To share data easily between multiple containers.

The example docker-compose.yaml above uses a named volume (`db-data`), which is the preferred way to persist data.

## Docker Networking: Container Communication

Docker networking is fundamental to how containers communicate with each other and the outside world. Understanding different network types and their security implications is crucial for building secure, scalable applications.

### 1. Bridge Network (Default) - Understanding the Problems

When Docker is installed, it automatically creates a **default bridge network** called `bridge`. All containers without a --network specified, are attached to the default bridge network. This can be a risk, as unrelated stacks/services/containers are then able to communicate.

#### Problems with the Default Bridge:
- **Security Risk**: All containers can communicate with each other by default
- **No Automatic DNS Resolution**: Containers can't communicate using container names
- **Shared Network Space**: All containers share the same network segment
- **No Built-in Service Discovery**: Manual IP management required

```bash
# See the default bridge network
docker network ls

# Inspect the default bridge network
docker network inspect bridge
```

#### Example of the Default Bridge Problem:

```bash
# Start two unrelated containers
docker run -d --name web-app nginx
docker run -d --name database postgres:13

# Both containers are on the same network and can communicate
# This is a security concern!
docker exec web-app ping database  # This works, but shouldn't!
```

### 2. Exposing Ports: Making Services Accessible

Use the --publish or -p flag to make a port available to services outside the bridge network. This creates a firewall rule in the host, mapping a container port to a port on the Docker host to the outside world.

#### Port Mapping Syntax:
```bash
# Basic port mapping
docker run -p <host_port>:<container_port> <image>

# Example: Map host port 8080 to container port 80
docker run -d -p 8080:80 nginx

# Map to all interfaces
docker run -d -p 0.0.0.0:8080:80 nginx

# Map only to localhost (more secure)
docker run -d -p 127.0.0.1:8080:80 nginx

# Let Docker choose the host port automatically
docker run -d -P nginx  # Uses random available port
```

#### Security Considerations:
Publishing container ports is insecure by default. Always be mindful of what you're exposing:

```bash
# BAD: Exposes database to the world
docker run -d -p 5432:5432 postgres:13

# BETTER: Only expose to localhost
docker run -d -p 127.0.0.1:5432:5432 postgres:13

# BEST: Don't expose database ports, use container networking
docker run -d --network app-network postgres:13
```

### 3. User-Defined Bridge Networks: The Preferred Approach

User-defined bridges provide better isolation and Using a user-defined network provides a scoped network in which only designated containers can communicate.

#### Why User-Defined Networks Are Preferred:

1. **Better Isolation**: Use custom bridge networks to isolate and apply network policies to specific containers
2. **Automatic DNS Resolution**: Container names work as hostnames
3. **Improved Security**: Only connected containers can communicate
4. **Fine-grained Control**: Separate networks for different application tiers

#### Creating and Using Custom Networks:

```bash
# Create a custom bridge network
docker network create my-app-network

# Create with custom subnet
docker network create --subnet=172.20.0.0/16 my-custom-network

# Create with custom driver options
docker network create --driver bridge --subnet=172.21.0.0/16 --gateway=172.21.0.1 production-network
```

#### Practical Example:

```bash
# Create separate networks for different application tiers
docker network create frontend-network
docker network create backend-network
docker network create database-network

# Run containers on appropriate networks
docker run -d --name web --network frontend-network nginx
docker run -d --name api --network backend-network my-api:latest
docker run -d --name db --network database-network postgres:13

# Connect API to both frontend and backend networks
docker network connect frontend-network api
```

### 4. Host Network: Direct Host Access

The host network driver removes network isolation between the container and Docker host. The container uses the host's networking directly.

```bash
# Run container with host networking
docker run -d --network host nginx

# This makes nginx accessible on the host's IP directly
# No port mapping needed, but less secure
```

**Use Cases:**
- High-performance applications requiring minimal network overhead
- Network monitoring tools
- Services that need access to host network interfaces

**Security Warning:** Host networking reduces isolation and should be used carefully.

### Network Management Commands

#### Listing and Inspecting Networks:
```bash
# List all networks
docker network ls

# Inspect network details
docker network inspect <network_name>

# See which containers are connected to a network
docker network inspect bridge | grep -A 5 "Containers"
```

#### Creating Networks:
```bash
# Basic network creation
docker network create <network_name>

# Create with specific driver
docker network create --driver bridge <network_name>

# Create with custom subnet
docker network create --subnet=192.168.1.0/24 --gateway=192.168.1.1 custom-net

# Create network with custom DNS
docker network create --dns=8.8.8.8 --dns=8.8.4.4 dns-custom-net
```

#### Connecting and Disconnecting Containers:
```bash
# Connect a running container to a network
docker network connect <network_name> <container_name>

# Connect with custom IP
docker network connect --ip 192.168.1.100 <network_name> <container_name>

# Disconnect a container from a network
docker network disconnect <network_name> <container_name>

# Force disconnect (if container is not responding)
docker network disconnect -f <network_name> <container_name>
```

#### Removing Networks:
```bash
# Remove a specific network
docker network rm <network_name>

# Remove multiple networks
docker network rm network1 network2 network3

# Remove all unused networks
docker network prune

# Force removal of all unused networks
docker network prune -f
```

### Network Isolation Testing: Pinging Between Containers

Understanding network isolation is crucial for security. Let's test communication between containers in different scenarios:

#### Testing Containers in the Same Network:

```bash
# Create a custom network
docker network create test-network

# Run two containers on the same network
docker run -dit --name container1 --network test-network alpine
docker run -dit --name container2 --network test-network alpine

# Test communication (this should work)
docker exec container1 ping container2
docker exec container1 ping -c 4 container2

# Test DNS resolution
docker exec container1 nslookup container2
```

#### Testing Containers in Different Networks:

```bash
# Create two separate networks
docker network create network-a
docker network create network-b

# Run containers on different networks
docker run -dit --name isolated1 --network network-a alpine
docker run -dit --name isolated2 --network network-b alpine

# Test communication (this should FAIL)
docker exec isolated1 ping isolated2  # This will fail - no route to host

# Verify isolation
docker exec isolated1 ping -c 2 isolated2
# Output: ping: bad address 'isolated2'
```

#### Testing Cross-Network Communication:

```bash
# Connect a container to multiple networks for controlled communication
docker network connect network-b isolated1

# Now isolated1 can communicate with both networks
docker exec isolated1 ping isolated2  # This now works
```

### Why Network Isolation Is Important

To limit the lateral movement of threats, employ network segmentation by categorizing containers by function or security level. For example, isolate database containers from web server containers.

#### Security Benefits:

1. **Principle of Least Privilege**: Containers can only communicate when explicitly allowed
2. **Breach Containment**: If one container is compromised, it can't easily access others
3. **Compliance**: Meet regulatory requirements for network segmentation
4. **Debugging**: Easier to troubleshoot network issues in isolated environments

#### Real-World Example:

```bash
# Create a three-tier application with proper isolation
docker network create public-network
docker network create app-network
docker network create db-network

# Frontend (accessible from internet)
docker run -d --name nginx --network public-network -p 80:80 nginx

# Backend API (connects frontend to database)
docker run -d --name api --network app-network my-api:latest

# Database (completely isolated)
docker run -d --name postgres --network db-network postgres:13

# Connect API to both app and database networks
docker network connect public-network api
docker network connect db-network api

# Result: nginx → api → postgres (controlled communication path)
# Database is never directly accessible from the public network
```

### Advanced Network Scenarios

#### Container-to-Container Communication Test Script:

```bash
#!/bin/bash
# network-test.sh - Test container network isolation

# Create test networks
docker network create web-tier
docker network create app-tier
docker network create data-tier

# Deploy containers
docker run -dit --name web --network web-tier alpine
docker run -dit --name app --network app-tier alpine  
docker run -dit --name db --network data-tier alpine

# Test isolation (should fail)
echo "Testing isolation (should fail):"
docker exec web ping -c 1 db 2>/dev/null && echo "❌ Security breach!" || echo "✅ Properly isolated"

# Connect app to multiple tiers (controlled access)
docker network connect web-tier app
docker network connect data-tier app

# Test controlled access (should work)
echo "Testing controlled access:"
docker exec app ping -c 1 web >/dev/null && echo "✅ Web tier accessible"
docker exec app ping -c 1 db >/dev/null && echo "✅ Database tier accessible"

# Cleanup
docker rm -f web app db
docker network rm web-tier app-tier data-tier
```

### Network Troubleshooting Commands

```bash
# Check container's network configuration
docker exec <container_name> ip addr show

# Check routing table
docker exec <container_name> ip route

# Test DNS resolution
docker exec <container_name> nslookup <target_container>

# Check network connectivity
docker exec <container_name> netstat -tuln

# Monitor network traffic
docker exec <container_name> tcpdump -i eth0

# Check which networks a container is connected to
docker inspect <container_name> | grep NetworkMode
```

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
