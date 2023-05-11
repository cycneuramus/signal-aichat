import logging
import os
import re
import signal
import sys
from collections import deque

import anyio
from EdgeGPT import Chatbot, ConversationStyle
from semaphore import Bot

import openai


class ChatHistory:
    def __init__(self, msg_limit):
        self.stack = deque(maxlen=msg_limit)

    def append(self, msg):
        return self.stack.append(msg)

    def get_as_list(self):
        return list(self.stack)


class BingAPI:
    def __init__(self, cookie_path, conversation_style):
        self.conversation_style = conversation_style
        self.chat = Chatbot(cookie_path=cookie_path)

    @staticmethod
    def _cleanup_footnote_marks(response):
        response_clean = re.sub(r"\[\^(\d+)\^\]", r"[\1]", response)
        return response_clean

    @staticmethod
    def _parse_footnotes(response):
        sources_raw = response["item"]["messages"][1]["sourceAttributions"]
        name = "providerDisplayName"
        url = "seeMoreUrl"

        sources = ""
        for i, source in enumerate(sources_raw, start=1):
            if name in source.keys() and url in source.keys():
                sources += f"[{i}]: {source[name]}: {source[url]}\n"
            else:
                continue

        return sources

    async def send(self, text):
        data = await self.chat.ask(prompt=text)
        sources = self._parse_footnotes(data)
        response_raw = data["item"]["messages"][1]["text"]
        response_clean = self._cleanup_footnote_marks(response_raw)

        if sources:
            return f"{response_clean}\n\n{sources}"
        else:
            return response_clean


class OpenAIAPI:
    def __init__(
        self, api_key, api_base, model="gpt-3.5-turbo", max_history=5, max_tokens=1024
    ):
        self.model = model
        self.history = ChatHistory(max_history)
        self.max_tokens = max_tokens
        openai.api_key = api_key
        openai.api_base = api_base

    async def send(self, text):
        new_message = {"role": "user", "content": text}
        self.history.append(new_message)
        messages = self.history.get_as_list()

        response = openai.ChatCompletion.create(
            model=self.model, messages=messages, max_tokens=self.max_tokens
        )

        self.history.append(response.choices[0].message)
        response = response.choices[0].message.content
        return response


async def ai(ctx):
    msg = ctx.message
    text = msg.get_body()

    await msg.mark_read()

    if "bing" not in ctx.data:
        ctx.data["bing"] = BingAPI(
            cookie_path="./cookies.json",
            conversation_style=ConversationStyle.balanced,
        )

    if "gpt" not in ctx.data:
        api_key = os.getenv("OPENAI_API_KEY")
        api_base = os.getenv("OPENAI_API_BASE") or "https://api.openai.com/v1"
        ctx.data["gpt"] = OpenAIAPI(api_key=api_key, api_base=api_base)

    if "llama" not in ctx.data:
        api_key = "this_can_be_anything"
        api_base = os.getenv("LLAMA_API_BASE")
        ctx.data["llama"] = OpenAIAPI(api_key=api_key, api_base=api_base)

    if "default_model" not in ctx.data:
        default_model = os.getenv("DEFAULT_MODEL")
        if default_model is not None:
            default_model = f"!{default_model.lower()}"
        ctx.data["default_model"] = default_model

    bing = ctx.data["bing"]
    gpt = ctx.data["gpt"]
    llama = ctx.data["llama"]
    default_model = ctx.data["default_model"]

    triggers = {"!bing": bing.send, "!gpt": gpt.send, "!llama": llama.send}

    response = ""
    for t in triggers:
        if t in text:
            await msg.typing_started()
            prompt = text[len(t) :].strip()
            response = await triggers[t](prompt)
            break
    else:
        if default_model is not None and any(default_model in t for t in triggers):
            await msg.typing_started()
            response = await triggers[default_model](text)

    if response:
        await msg.typing_stopped()
        quote = (
            msg.get_group_id() is not None
        )  # quote prompt msg in potentially busy group chats
        await msg.reply(response, quote=quote)


async def main():
    async with Bot(
        os.getenv("SIGNAL_PHONE_NUMBER"),
        socket_path="/signald/signald.sock",
        logging_level=logging.INFO,
    ) as bot:
        bot.register_handler("", ai)
        await bot.start()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    anyio.run(main)
