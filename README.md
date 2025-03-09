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

## Authentication

### GitHub Token

The application authenticates users with a GitHub auth token, by default.
A user enters their GitHub token into the login screen, and all calls to GitHub are made with the user's token.

### GitHub OAuth

The application can optionally use GitHub OAuth to authenticate users.
To do so, [create a GitHub OAuth app](https://github.com/settings/applications/new), then set the following environment
variables:

```shell
export GITHUB_OAUTH_ENABLED=true
export GITHUB_CLIENT_ID=your_client_id
export GITHUB_CLIENT_SECRET=your_client_secret
```

To restrict users to one or more domains, or one or more email addresses, set one of the following environment
variables.

```shell
export ALLOWED_DOMAINS=somedomain.example.com,anotherdomain.example.com
export ALLOWED_ADDRESSES=someone@example.com,another@example.com
```

Users are allowed to access the application if one of their verified email addresses on GitHub matches. 

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
