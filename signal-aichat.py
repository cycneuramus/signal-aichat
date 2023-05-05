import logging
import os
import re
import signal
import sys

import anyio
import openai
from EdgeGPT import Chatbot, ConversationStyle
from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from semaphore import Bot, ChatContext


def terminate(signal, frame):
    print("Exiting...")
    sys.exit(0)


async def bing(prompt, ctx):
    bing = ctx.data["bing"]
    data = await bing.ask(
        prompt=prompt, conversation_style=ConversationStyle.balanced
    )
    response = data["item"]["messages"][1]["text"]
    return re.sub(
        r"\s?\[\^[0-9]+\^]", "", response
    )  # Strip footnote stubs such as [^1^] # TODO include footnotes instead


async def gpt(prompt, ctx):
    gpt = ctx.data["gpt"]
    return gpt.predict(input=prompt)


async def llama(prompt, ctx):  # TODO remember chat context
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

    if not "bing" in ctx.data:
        ctx.data["bing"] = Chatbot(cookie_path="./cookies.json")

    if not "gpt" in ctx.data:
        api_key = os.getenv("OPENAI_API_KEY")

        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=api_key,
            model_kwargs={"max_tokens": 512},
        )
        ctx.data["gpt"] = ConversationChain(llm=llm)

    triggers = {"!bing": bing, "!gpt": gpt, "!llama": llama}
    default_model = os.getenv("DEFAULT_MODEL")

    if default_model is not None:
        default_model = default_model.lower()

    response = ""
    for t in triggers:
        if t in text:
            await msg.typing_started()
            func = triggers[t]
            prompt = text[len(t) :].strip()
            response = await func(prompt, ctx)
            break
    else:
        if default_model is not None and any(
            default_model in t for t in triggers
        ):
            await msg.typing_started()
            response = await triggers[default_model](text, ctx)

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
    signal.signal(signal.SIGTERM, terminate)
    anyio.run(main)
