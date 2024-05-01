# Recipe App API

This project is a RESTful API for managing recipes built using Python, Django, and Django Rest Framework (DRF), with a focus on Test-Driven Development (TDD).

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project's purpose is to learn advanced concepts of Django, with a main focus on backend development. For the database, we will be using PostgreSQL, along with the technologies Python, Django, and DRF.

## Features

still in development will be udpated after adding models and database configuration

### Docker Configuratoin(dockerfile)

```Dockerfile
FROM python:3.9-alpine3.13
```
- This line specifies the base image for your Docker container. In this case, you're using the `python:3.9-alpine3.13` image, which is a lightweight Python image based on Alpine Linux.

```Dockerfile
LABEL maintainer="anwarsayyad2631@gmail.com"
```
- This line adds metadata to the Docker image, specifying the maintainer's email address.

```Dockerfile
ENV PYTHONUNBUFFERED 1
```
- This line sets an environment variable `PYTHONUNBUFFERED` to `1`, which ensures that Python's standard output is unbuffered. This can help with logging and debugging.

```Dockerfile
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
```
- These lines copy the `requirements.txt` and `requirements.dev.txt` files from your host machine to the `/tmp` directory inside the Docker container. These files typically contain Python package dependencies for your project.

```Dockerfile
COPY ./app /app
```
- This line copies the contents of the `app` directory from your host machine to the `/app` directory inside the Docker container. This is where your Django application code will reside.

```Dockerfile
WORKDIR /app
```
- This line sets the working directory inside the Docker container to `/app`. Any subsequent commands will be executed from this directory.

```Dockerfile
EXPOSE 8000
```
- This line exposes port `8000` on the Docker container. It indicates that the container will listen for incoming connections on this port.

```Dockerfile
ARG DEV=false
```
- This line defines a build argument `DEV` with a default value of `false`. This argument can be overridden during the Docker image build process.

```Dockerfile
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
```
- This section of the Dockerfile contains several commands that are executed during the Docker image build process:
  - It creates a virtual environment in the `/py` directory, upgrades pip, installs dependencies from `requirements.txt`, installs additional dependencies from `requirements.dev.txt` if `DEV` is set to `true`, removes temporary files, and adds a non-root user `django-user` to the container for improved security.

```Dockerfile
ENV PATH="/py/bin:$PATH"
```
- This line sets the `PATH` environment variable to include the `/py/bin` directory, ensuring that commands installed within the virtual environment are accessible.

```Dockerfile
USER django-user
```
- This line sets the default user to `django-user`. Any subsequent commands in the Dockerfile will be executed as this user, providing an additional layer of security by running the container with reduced privileges.

### Docker-compose file
This Docker Compose configuration defines a service named `app` for running your Django application. Let's break down each part:

```yaml
services:
  app:
    build: 
      context: .
      args:
        - DEV=true
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    command: 
      sh -c "python manage.py runserver 0.0.0.0:8000"
```

- `services`: This is the top-level key for defining Docker services in your `docker-compose.yml` file.

- `app`: This is the name of the service.

- `build`: This section specifies how to build the Docker image for the service.
  - `context: .`: The build context is set to the current directory, which means Docker will use the current directory as the root of the build context.
  - `args: - DEV=true`: This passes a build argument `DEV=true` to the Dockerfile during the build process. This allows you to conditionally install development dependencies if needed.

- `ports`: This section specifies port mappings for the service.
  - `"8000:8000"`: This maps port `8000` of the host machine to port `8000` of the Docker container.

- `volumes`: This section mounts host paths or named volumes into the service.
  - `./app:/app`: This mounts the `./app` directory from the host machine to the `/app` directory inside the Docker container. This allows you to sync code changes between your host and the container.

- `command`: This section specifies the command to run when the container starts.
  - `sh -c "python manage.py runserver 0.0.0.0:8000"`: This command starts the Django development server, binding it to `0.0.0.0` so it's accessible from outside the container on port `8000`.


### Git hub actions configruations

1. **Create a Docker Hub Access Token**:
   - Go to the Docker Hub website and sign in to your account.
   - Navigate to your account settings and find the "Security" or "Access Tokens" section.
   - Generate a new access token with the necessary permissions (typically, write access is required to push Docker images).
   - Copy the generated access token.

2. **Add Docker Hub Access Token as a GitHub Secret**:
   - In your GitHub repository, go to "Settings" -> "Secrets" -> "New repository secret".
   - Name the secret something descriptive, like `DOCKERHUB_TOKEN`.
   - Paste the Docker Hub access token you generated as the value for the secret.
   - Click "Add secret" to save it.

3. **Use GitHub Actions to Log in to Docker**:
   - In your GitHub repository, create or modify a GitHub Actions workflow file (e.g., `.github/workflows/docker.yml`).
   - Use the `docker/login-action` action to log in to Docker Hub using the secret you created:
     ```yaml
     name: Docker Build and Push
     on:
       push:
         branches:
           - main
     jobs:
       build:
         runs-on: ubuntu-latest
         steps:
           - name: Checkout code
             uses: actions/checkout@v2
           - name: Login to Docker Hub
             uses: docker/login-action@v1
             with:
               username: ${{ secrets.DOCKERHUB_USERNAME }}
               password: ${{ secrets.DOCKERHUB_TOKEN }}
     ```
   - Replace `DOCKERHUB_USERNAME` with your Docker Hub username.
   - Ensure that the secret name (`DOCKERHUB_TOKEN`) matches the name you used when creating the secret in GitHub.

   

4. **Push Your Changes and Observe GitHub Actions**:
   - Commit and push your changes to trigger the GitHub Actions workflow.
   - Check the Actions tab in your GitHub repository to see the progress of the workflow.
   - You should see a step for logging in to Docker Hub, using the access token from the GitHub secret.

By following these steps, your GitHub Actions workflow will be able to securely log in to Docker Hub using the access token stored as a GitHub secret. This allows you to automate Docker builds and deployments as part of your CI/CD pipeline. You can then update your README.md to include instructions for setting up the Docker Hub access token as a secret and using it in your GitHub Actions workflow.

```yaml
name: Checks
```
- This sets the name of the GitHub Actions workflow to "Checks".

```yaml
on: [push]
```
- This specifies that the workflow should be triggered on every push event to the repository.

```yaml
jobs:
  test-lint:
    name: test and Lint
    runs-on: ubuntu-20.04
    steps:
```
- This defines a job named "test-lint" that runs on an Ubuntu 20.04 environment.

```yaml
      - name: Login to Docker hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USER }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```
- This step logs in to Docker Hub using the `docker/login-action` action. It retrieves the Docker Hub username and access token from GitHub secrets named `DOCKERHUB_USER` and `DOCKERHUB_TOKEN`, respectively.

```yaml
      - name: Checkout
        uses: actions/checkout@v2
```
- This step checks out the code from the repository using the `actions/checkout` action.

```yaml
      - name: Test
        run: docker-compose run --rm app sh -c "python manage.py test"
```
- This step runs the tests for your Django application using the `python manage.py test` command within a Docker container managed by Docker Compose.

```yaml
      - name: Lint
        run: docker-compose run --rm app sh -c "flake8"
```
- This step performs linting using Flake8 within a Docker container managed by Docker Compose.

This GitHub Actions workflow automates the process of running tests and linting checks for your Django application whenever there's a push to the repository. It uses Docker to manage the environment, ensuring consistency across different setups. Make sure to set up the necessary secrets in your GitHub repository for Docker Hub authentication.

## Installation

To run the Recipe App API locally, you'll need Docker installed on your system. Follow these steps to install Docker:

1. **Download Docker:**
   - Visit the [Docker website](https://www.docker.com/get-started) to download Docker for your operating system.

2. **Install Docker:**
   - Follow the installation instructions provided on the Docker website for your specific operating system.

3. **Verify Installation:**
   - After installation, open a terminal or command prompt and run the following command to verify that Docker is installed correctly:
     ```
     docker --version
     ```

4. **Start Docker:**
   - Start the Docker application on your system.

5. **Clone the Repository:**
   - Clone the Recipe App API repository to your local machine using Git:
     ```
     git clone https://github.com/your_username/recipe-app-api.git
     cd recipe-app-api
     ```

6. **Set Up Docker Compose (Optional):**
   - If you haven't already, install Docker Compose by following the [official Docker Compose installation instructions](https://docs.docker.com/compose/install/).

7. **Run the Application:**
   - Once Docker is installed and running, you can start the Recipe App API by running the following command in the root directory of the project:
     ```
     docker-compose up
     ```

8. **Access the API:**
   - After the containers are up and running, you can access the Recipe App API at `http://localhost:8000/`.



## Usage

To run the Recipe App API using Docker, follow these steps:

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your_username/recipe-app-api.git
   cd recipe-app-api
   ```

2. **Start Docker Containers:**
   ```sh
   docker-compose up
   ```

3. **Access the API:**
   - After the containers are up and running, you can access the Recipe App API at `http://localhost:8000/`.



## Testing

Testing for the Recipe App API is conducted using Django unit tests. These tests ensure the correctness and reliability of the application's functionalities. To run the tests using Docker, follow these steps:

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your_username/recipe-app-api.git
   cd recipe-app-api
   ```

2. **Start Docker Containers:**
   ```sh
   docker-compose up
   ```

3. **Run Django Unit Tests:**
   - Once the containers are up and running, open a new terminal window/tab and run the following command to execute Django unit tests within a Docker container:
   ```sh
   docker-compose run --rm app sh -c "python manage.py test"
   ```
   This command will run all the unit tests for the Recipe App API, ensuring that individual components of your application are functioning correctly.

By running Django unit tests, you can validate the behavior of your application's logic and ensure that it meets the desired specifications.



## Contributing

We welcome contributions from the community to improve the Recipe App API. If you'd like to contribute, please follow these steps:

1. **Fork the Repository:**
   - Click the "Fork" button at the top right corner of this repository to create a copy of the project in your GitHub account.

2. **Clone the Forked Repository:**
   ```sh
   git clone https://github.com/your_username/recipe-app-api.git
   cd recipe-app-api
   ```

3. **Create a New Branch:**
   - Create a new branch to work on your changes:
   ```sh
   git checkout -b feature/my-feature
   ```

4. **Make Changes:**
   - Implement your changes, following the coding conventions and guidelines.

5. **Write Unit Tests:**
   - Write comprehensive unit tests to validate the functionality of your changes. Ensure that all existing tests pass and write new tests if necessary.

6. **Run Tests:**
   - Before committing your changes, run the unit tests locally to ensure that they pass:
   ```sh
   docker-compose run --rm app sh -c "python manage.py test"
   ```

7. **Commit Changes:**
   - Once your changes are ready, commit them with a descriptive commit message:
   ```sh
   git commit -am "Add feature: my feature"
   ```

8. **Push Changes:**
   - Push your changes to your forked repository:
   ```sh
   git push origin feature/my-feature
   ```

9. **Create Pull Request:**
   - Go to the GitHub page of your forked repository and click on the "New pull request" button.
   - Provide a descriptive title and detailed description for your pull request.
   - Ensure that the "base" branch is set to `main` and the "compare" branch is set to your feature branch (`feature/my-feature`).
   - Click on "Create pull request" to submit your changes for review.

10. **Review and Merge:**
    - Your pull request will be reviewed by the project maintainers. Once approved, it will be merged into the main branch.

Thank you for contributing to the Recipe App API! Your contributions help make the project better for everyone.


## License

The Recipe App API is licensed under the MIT License.

MIT License

Copyright (c) [2024] [Anwar Sayyad]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

