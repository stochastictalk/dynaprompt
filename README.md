# 🕰️⚡ `dynaprompt` ⚡🕰️

⚠️ currently a WIP ⚠️

A conversation between a chatbot and user currently looks like
```
User:       <prompt>
Chatbot:    <response>
User:       <prompt>
Chatbot:    <response>
```
Notice:
1. The interaction is initiated by the user.
2. Both participants send only a single message at a time.
3. The chatbot only ever responds immediately after being addressed by the user. 
4. The interaction only contains two participants.

`dynaprompt` is a Python package that breaks aspects 1, 3, and 4 of this paradigm by providing 
* a `Conversation` class that allows multiple input sources and output devices to hook into a common message log
* a `PromptScheduler` input source that conversation participants can use to schedule messages to themselves and others


This message scheduler's functionality is very simple: the user and chatbot can use it to schedule messages (lol). A message is scheduled by sending an instruction message in the chat that has the format
```
dps <RECIPIENT> <TIME PROMPT>

<PROMPT>
```
- `<RECIPIENT>`: should be either `user` (alias `u`) or `chatbot` (alias `c`)
- `<TIME PROMPT>`: a message indicating when the message should be sent, e.g. `tomorrow evening`, `every day at 8am`, `15th March at 2pm`
- `<PROMPT>`: the message to be sent (can be multiline, no restrictions on content) e.g. `teach me about an unusual species of monkey`

Example use-cases:
* chatbot schedules multiple messages for the immediate future, allowing it to send more than one message at a time
* chatbot schedules initiating or continuing a conversation with a user at a later date and time
* user schedules impromptu or recurring conversations with the chatbot

## User Quickstart

Install the package with
```
pip install git+https://github.com/stochastictalk/dynaprompt
```

To run the example chatbot, create a `.env` file in your working directory that looks like this
```
OPENAI_API_KEY="<your api key>"
```
Then run `python example.py`, which executes the following:
```
from dynaprompt import Conversation
from dynaprompt.inputs import CLIInput, OpenAIChat
from dynaprompt.outputs import CLIOutput


if __name__ == "__main__":
    conversation = Conversation(
        iocallables=[CLIOutput(), OpenAIChat()],
        main_iocallable=CLIInput()
    )
    conversation()
```
This creates a chat session involving your CLI input and OpenAI's chat completion API, with the message history being rendered to the CLI.


https://user-images.githubusercontent.com/56552295/226182010-07d10869-716c-434a-b127-d77dc8548a46.mov




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

## Feature priority stack

1. Get to minimum functionality (scheduling and emitting prompts).
2. Incorporate into quickstart demo.
2. 
