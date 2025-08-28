# Project Setup

Follow this guide to setup the project and begin using the eob-cli tool.

## Prerequisites:

1. Python version 3.12 is installed on your system.
1. Either _pip_ or _uv_ are installed on your system.
   - To install pip run `python3 -m ensurepip --upgrade`
   - To install uv follow this [guide](https://docs.astral.sh/uv/getting-started/installation/)
1. The repository has been cloned using `git clone https://github.com/oknott14/eob-cli`
1. Your cwd is the root directory of the project

## Initialize Virtual Environment

If using pip run:

```
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

For UV users, you can skip this step.

## Install Dependencies

pip: `pip install -r requirements.txt`
uv: 'uv sync`

## Setup the Environment

The eob-cli requires a few environment variables to be defined. These can be defined using a _.env_ file or by adding the environment variables directly to the terminal environment. The following variables must all be defined to use the cli app.

```
GOOGLE_API_KEY=<your_google_api_key>
```

Instructions for creating a Google API Key can be found [here](https://ai.google.dev/gemini-api/docs/api-key#set-api-env-var)

## Run the Application

See [cli](./cli.md)
