# 🕰️⚡ `dynaprompt` 🕰️⚡

A conversation between a chatbot and user currently looks like
```
User:       <prompt>
Chatbot:    <response>
User:       <prompt>
Chatbot:    <response>
```
Key things to notice:
1. The interaction is initiated by the user.
2. Both participants send only a single message at a time.
3. The chatbot only ever responds immediately after being addressed by the user. 

`dynaprompt` is a Python package that breaks aspects 1 and 3 of this paradigm via a message scheduler that sits between the User and Chatbot, like
```
User --- DynaPrompt --- Chatbot
```
As a message scheduler, its functionality is very simple: the user and chatbot can use it to schedule messages. A scheduled message has three attributes:
* Recipient
* Timestamp
* Message

Example use-cases:
* chatbot schedules multiple messages for the immediate future, allowing it to send more than one message at a time
* chatbot schedules initiating or continuing a conversation with a user at a later date and time
* user schedules impromptu or recurring conversations with the chatbot

## Features

@TODO

## User Quickstart

Install the package with
```
pip install git+https://github.com/stochastictalk/dynaprompt
```

```
@TODO quickstart example
```


## Developer Quickstart

- 📜 Docs: `sphinx`
- 🧰 Linting: `ruff`
- ⚫ Autoformatting: `black`
- 🧪 Testing: `pytest`

First clone this repository, set it as your working directory, and make sure you have [Poetry installed](https://python-poetry.org/docs/).

Activate the package virtual environment by running `poetry shell`. 

Install development dependencies by running `poetry install -E dev`.


### 🧰  Enable linting and autoformatting

Install the pre-commit hooks by running `pre-commit install`. The pre-commit hooks will run each time you try to make a commit. You can edit their configuration in `pyproject.toml`.

### 🧪 Testing  

Run the tests by calling `pytest`. Add and modify tests under `tests/`.

### 📜 Docs

To compile the documentation, run
```
cd docs
make html
```
Host the resulting doc HTMLs using Python's webserver:
```
python -m http.server 3527 -d ../build/sphinx/html
``` 
Open a web browser on the host and go to `localhost:3527`. You should see the docs.

