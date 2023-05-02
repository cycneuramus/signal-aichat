__signal-aichat__ is an AI-powered chatbot for the Signal messenger app. It currently supports [Bing Chat](https://bing.com/chat), [ChatGPT](https://chat.openai.com/), and any local [LLM](https://en.wikipedia.org/wiki/Large_language_model) that works with [llama.cpp](https://github.com/ggerganov/llama.cpp)(Vicuna, Alpaca, Koala, et al.). 

<p>
	<img src="../screenshot.png" width=500 />
</p>

## Setup instructions

### 0. Clone this repo:

`git clone https://github.com/cycneuramus/signal-aichat`

---

### 1. `signald`

Start the container:
```
docker compose up -d signald
```

Drop into the container's shell:

```
docker exec -it signald /bin/bash
```

Once inside the container, either:

```
# link to an existing account:
$ signaldctl account link --device-name signal-aichat
```

or

```
# register a new account:
$ signaldctl account register [phone number]
```

For more information, see the [documentation](https://signald.org/articles/getting-started/) for `signald`.

__Once the account is setup, populate the `SIGNAL_PHONE_NUMBER` variable in the `.env` file.__

---

### 2. Bing Chat:

See the [EdgeGPT](https://github.com/acheong08/EdgeGPT] repository. TL;DR:

<details>
	<summary>
__Checking access__
	</summary>
- Install the latest version of Microsoft Edge
- Alternatively, you can use any browser and set the user-agent to look like you're using Edge (e.g., `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51`). You can do this easily with an extension like "User-Agent Switcher and Manager" for [Chrome](https://chrome.google.com/webstore/detail/user-agent-switcher-and-m/bhchdcejhohfmigjafbampogmaanbfkg) and [Firefox](https://addons.mozilla.org/en-US/firefox/addon/user-agent-string-switcher/).
- Open [bing.com/chat](https://bing.com/chat)
- If you see a chat feature, you are good to go
</details>

<details>
	<summary>
__Getting authentication__
	</summary>
- Install the cookie editor extension for [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- Go to `bing.com`
- Open the extension
- Click "Export" on the bottom right, then "Export as JSON" (this saves your cookies to the clipboard)
- Paste your cookies into a file named `cookies.json`
</details>

__Make sure to place the resulting `cookies.json` file in this repo directory.__

---

### 3. ChatGPT

+ In the `.env` file, populate the `OPENAI_API_KEY` variable with your API key

---

### 4. Llama models

+ Place your model weights in the `models` directory
+ In the `env` file, change the model in the `MODEL` path variable to match your model file

---

### 5. Deploy

`docker compose up -d`

And start chatting.
