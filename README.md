# GitHub Explorer Agent

An AI Agent that can answer questions about GitHub repositories for a user or an organization.

## Run

1.  Copy the example environment file and fill in the necessary values.
    ```shell
    cp .env.example .env 
    source .env
    ```

1.  Run the agent.
    ```shell
    uv run -m explorer
    ```

## Test

```shell
uv run -m unittest
```
