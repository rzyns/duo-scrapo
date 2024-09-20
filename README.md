Extract vocabulary list from the Duolingo web app

## Requirements

1. [1Password cli](https://developer.1password.com/docs/cli/get-started)
1. [uv](https://github.com/astral-sh/uv?tab=readme-ov-file#installation)

## Setup

Note: this assumes that your Duolingo credentials are stored in
the default Private vault in an entry named "Duolingo", and are named
"username" and "password", respectively.

```shell
uv sync
```

## Running

*Use a different `--env-file` if necessary

```shell
op run --env-file .env -- uv run crawl
```
