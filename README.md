# chatgpt-api-by-browser-python
(Updated wip) script that runs on users' browsers through the Tampermonkey script and converts the web version of ChatGPT operations into an API interface

(The code here is 95% written by ChatGPT itself).

## WIP

The script here is for testing purpose only. it currently does not work nicely as I'm switching to a proper API setup instead. The code is uploaded for references only.

The difficuly to handle memory makes it not very suitable for agentic use cases, so I'm not planning to finish this as least for now.

You may refer to original repo for mostly how it works: https://github.com/zsodur/chatgpt-api-by-browser-script

## Setup

**browser side**:

1. Install userscript in the repo with tampermonkey
2. In order to connect to the websocket backend, use some plugin that disables Content-Security-Policy (CSP), like [this one](`https://chromewebstore.google.com/detail/disable-content-security/ieelmcmcagommplceebfedjlakkhpden?pli=1)

(Currently there's no UI for it. To check connection status, press `F12` and see console messages).

**backend side**:

1. clone the repo:

```bash
git clone https://github.com/arot-devs/chatgpt-api-by-browser-python
cd chatgpt-api-by-browser-python
```

2. install requirements:
```
pip install aiohttp websockets asyncio requests
```

3. run the server:
```bash
python gpt_server3.py
```

If the extension has been installed and you're on a chatgpt page (`https://chatgpt.com/*`), upon running the server you should see something like this ("Browser connected via WebSocket"):

<img width="779" alt="image" src="https://github.com/user-attachments/assets/b1bfb38a-8316-40b2-b72a-aae7860f02ae" />


## Usage

A example script for retrieving results is given in the repo as well:

```bash
python gpt_client.py
```

