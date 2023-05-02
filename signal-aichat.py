import logging
import os
import re
import signal
import sys

import anyio
import openai
from EdgeGPT import Chatbot, ConversationStyle
from semaphore import Bot, ChatContext


def terminate(signal, frame):
    print("Exiting...")
    sys.exit(0)


async def bing(prompt):
    bing = Chatbot(cookie_path="./cookies.json")
    data = await bing.ask(prompt=prompt, conversation_style=ConversationStyle.balanced)
    await bing.close()

    response = data["item"]["messages"][1]["text"]
    return re.sub(
        r"\s?\[\^[0-9]+\^]", "", response
    )  # Strip footnote stubs such as [^1^] # TODO include footnotes instead


async def gpt(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.choices[0].message.content



async def llama(prompt):
    openai.api_key = "this_can_be_anything"
    openai.api_base = os.getenv("LLAMA_API_BASE")

    response = openai.ChatCompletion.create(
        model="this_can_be_anything",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.choices[0].message.content


async def ai(ctx):
    msg = ctx.message
    text = msg.get_body()

    await msg.mark_read()
    await msg.typing_started()

    triggers = ["!bing", "!gpt", "!llama"]
    prompt = ""
    for t in triggers:
        if t in text:
            prompt = text[len(t) :].strip()
            break

    response = ""
    if "!bing" in text:
        response = await bing(prompt)
    if "!gpt" in text:
        response = await gpt(prompt)
    elif "!llama" in text:
        response = await llama(prompt)
    else:
        default_model = os.getenv("DEFAULT_MODEL").lower()
        if default_model == "bing":
            response = await bing(prompt)
        if default_model == "gpt":
            response = await gpt(prompt)
        if default_model == "llama":
            response = await llama(prompt)

    await msg.typing_stopped()

    quote = msg.get_group_id() is not None  # quote prompt msg in potentially busy group chats
    await msg.reply(response, quote=quote)


async def main():
    async with Bot(
        os.getenv("SIGNAL_PHONE_NUMBER"),
        socket_path="/signald/signald.sock",
        logging_level=logging.INFO,
    ) as bot:

        bot.register_handler(re.compile("!(bing|gpt|llama)"), ai)
        await bot.start()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, terminate)
    anyio.run(main)
