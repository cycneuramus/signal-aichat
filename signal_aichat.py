import logging
import os
import signal
import sys

import ai
import anyio
from semaphore import Bot


async def aichat(ctx):
    msg = ctx.message
    text = msg.get_body()

    disabled_models = os.getenv("DISABLED_MODELS", "").lower()
    default_model = os.getenv("DEFAULT_MODEL", "").lower()

    if "triggers" not in ctx.data:
        triggers = {}
        for model in ai.MODELS:
            if model not in ctx.data and model not in disabled_models:
                ctx.data[model] = ai.ChatModel(model)
                triggers[ctx.data[model].trigger] = ctx.data[model].api
        ctx.data["triggers"] = triggers
    else:
        triggers = ctx.data["triggers"]

    response = ""
    for trigger, api in triggers.items():
        if trigger in text and trigger.replace("!", "") not in disabled_models:
            try:
                await msg.mark_read()
                await msg.typing_started()
                prompt = text[len(trigger) :].strip()
                response = await api.send(prompt)
            except Exception as e:
                response = f"I encountered an error: {str(e)}"
            break
    else:
        if default_model and f"!{default_model}" in triggers.keys():
            try:
                await msg.mark_read()
                await msg.typing_started()
                api = ctx.data[default_model].api
                response = await api.send(text)
            except Exception as e:
                response = f"I encountered an error: {str(e)}"

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
        bot.register_handler("", aichat)
        await bot.start()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    anyio.run(main)
