# Repository Discovery Agent

An AI Agent that can answer questions about GitHub repositories for a user or an organization.

## Run

1.  Copy the example environment file and fill in the necessary values.
    ```shell
    cp .env.example .env 
    source .env
    ```

1.  Run the app then visit [localhost:5050](http://localhost:5050).
    ```shell
    uv run -m discovery
    ```

## Test

1.  Run fast tests
    ```shell
    uv run -m unittest
    ```

1.  Run slow tests
    ```shell
    source .env
    RUN_SLOW_TESTS=true uv run -m unittest
    ```

## Build container

1. Build container
   ```shell
   uv pip compile pyproject.toml -o requirements.txt
   docker build -t repository-discovery .
   ```

1. Run with docker
   ```shell
   docker run -p 5050:5050 --env-file .env.docker repository-discovery
   ```   
