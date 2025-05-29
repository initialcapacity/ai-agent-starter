# Repository Discovery Agent

An AI agent that can answer questions about GitHub repositories for a user or an organization.

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

1.  Build container
    ```shell
    uv pip compile pyproject.toml -o requirements.txt
    docker build -t repository-discovery .
    ```

1.  Run with docker
    ```shell
    docker run -p 5050:5050 --env-file .env.docker repository-discovery
    ```

# Exercise

## Create a tool

Use the [GitHub API documentation](https://docs.github.com/en/rest) and add a new tool.

1.  In the [GithubClient](./discovery/github_support/github_client.py), define a method that calls the GitHub API
    endpoint you've chosen.
1.  Add a function to [github_tools](./discovery/repository_agent/github_tools.py) that calls your new method in the
    GitHub client.
    Return a JSON string of the data returned by the method.
1.  Add a Python docstring to your function that describes how OpenAI should use the function.
1.  Add the `@tool()` decorator to the function.
1.  Register the new tool by adding it to the list of tools that are returned by the `github_tools` method.

Run the application and see if you can have OpenAI use your tool to fetch data.

## Add a test for the new tool

Now make sure the agent integrates properly with OpenAI to use your tool.
This test will use the LLM and take more time to run.
The focus of the test should be to check that the agent uses the correct tool to answer the question, but we have
limited ability to check that the response is correct.

1.  Define a `test_` method  in [test_repository_agent.py](./tests/repository_agent/test_repository_agent.py) that will
    cover the new tool that was added.
1.  Decorate the test method with the `@slow` decorator.
1.  Add the `@responses.activate` decorator to the method to enable stubbing the API call.
1.  Stub the API that your tool uses.
1.  Send a question to the agent and assert the correct tools are called
1.  Next assert the response by spot checking for relevant word(s).
