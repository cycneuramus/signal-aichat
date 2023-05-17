__signal-aichat__ is an AI-powered chatbot for the Signal messenger app. It currently supports:

- [Bing Chat](https://bing.com/chat) – `!bing`
- [ChatGPT](https://chat.openai.com/) – `!gpt`
- [Google Bard](https://bard.google.com) (*untested*) – `!bard`
- [HuggingChat](https://huggingface.co/chat/) (*does not support continuous conversations*) – `!hugchat`
- Any local [LLM](https://en.wikipedia.org/wiki/Large_language_model) that works with [llama.cpp](https://github.com/ggerganov/llama.cpp) (Vicuna, Alpaca, Koala, et al.) – `!llama`

---

<p>
 <img src="https://github.com/cycneuramus/signal-aichat/blob/master/.github/screenshot.png" width=500 />
</p>

## Setup instructions

### 0. Clone this repo

`git clone https://github.com/cycneuramus/signal-aichat`

---

### 1. `signald`

*Chatting with your own number via "Note to Self" does not work. This assumes you will be using a separate Signal account for the bot.*

Start the `signald` container:

```
docker compose up -d signald
```

Drop into the container's shell:

```
docker exec -it signal-aichat-signald /bin/bash
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

### 2. Google Bard

See the [Bard](https://github.com/acheong08/Bard) repository. TL;DR:

Go to https://bard.google.com/

- F12 for console
- Session: Go to Application -> Cookies -> `__Secure-1PSID`. Copy the value of that cookie.
- In `.env`, populate the `BARD_TOKEN` variable with the cookie value

---

### 3. Bing Chat

See the [EdgeGPT](https://github.com/acheong08/EdgeGPT) repository. TL;DR:

<details>
  <summary>

Checking access

  </summary>

- Install the latest version of Microsoft Edge
- Alternatively, you can use any browser and set the user-agent to look like you're using Edge (e.g., `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51`). You can do this easily with an extension like "User-Agent Switcher and Manager" for [Chrome](https://chrome.google.com/webstore/detail/user-agent-switcher-and-m/bhchdcejhohfmigjafbampogmaanbfkg) and [Firefox](https://addons.mozilla.org/en-US/firefox/addon/user-agent-string-switcher/).
- Open [bing.com/chat](https://bing.com/chat)
- If you see a chat feature, you are good to go

</details>

<details>
  <summary>

Getting authentication

  </summary>

- Install the cookie editor extension for [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- Go to `bing.com`
- Open the extension
- Click "Export" on the bottom right, then "Export as JSON" (this saves your cookies to the clipboard)
- Paste your cookies into a file named `bing.json`

</details>

__Make sure to add the exported JSON to the `config/bing.json` file in this repo directory.__

---

### 4. ChatGPT

- In the `.env` file, populate the `OPENAI_API_KEY` variable with your API key
- Optionally, populate the `OPENAI_API_BASE` variable to use a different endpoint (defaults to <https://api.openai.com/v1>)

---

### 5. HuggingChat

See the [HuggingChat API](https://github.com/Soulter/hugging-chat-api) repository. TL;DR:

- Install the `Cookie-Editor` extension for [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- Go to [HuggingChat](https://huggingface.co/chat) and **login**
- Open the extension
- Click `Export` on the bottom right, then `Export as JSON` (this saves your cookies to the clipboard)

__Make sure to add the exported JSON to the `config/hugchat.json` file in this repo directory.__

---
### 6. Llama models

- Place your model weights in the `models` directory
- In the `.env` file, change the model in the `MODEL` path variable to match your model file

---

### 7. Additional configuration

In `.env`:

- Models can be disabled by populating the `DISABLED_MODELS` variable
- To chat with a default model without explicitly having to trigger a bot response with `!<model>`, populate the `DEFAULT_MODEL` variable

Assuming `DEFAULT_MODEL=gpt`, for example, you'd be able to chat normally:

<p>
 <img src="https://github.com/cycneuramus/signal-aichat/blob/master/.github/default_model.png" width=500 />
</p>

---

### 8. Deploy

- `docker compose up -d`

And start chatting.
