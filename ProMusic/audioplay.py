# Copyright (C) 2021 DeCoDe

from os import path
import DeCoDe.converter
from callsmusic import callsmusic, queues
from config import (
    AUD_IMG,
    BOT_USERNAME,
    DURATION_LIMIT,
    GROUP_SUPPORT,
    QUE_IMG,
    UPDATES_CHANNEL,
)
from ProMusic.play import convert_seconds
from helpers.filters import command, other_filters
from helpers.gets import get_file_name
from pyrogram import Client
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@Client.on_message(command(["stream", f"stream@{BOT_USERNAME}"]) & other_filters)
async def stream(_, message: Message):
    costumer = message.from_user.mention
    lel = await message.reply_text("ð **processing** sound...")

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="â¨ GÊá´á´á´", url=f"https://t.me/{GROUP_SUPPORT}"
                ),
                InlineKeyboardButton(
                    text="ð» CÊá´É´É´á´Ê", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    audio = message.reply_to_message.audio if message.reply_to_message else None
    if not audio:
        return await lel.edit("ð­ **please reply to a telegram audio file**")
    if round(audio.duration / 60) > DURATION_LIMIT:
        return await lel.edit(
            f"â **music with duration more than** `{DURATION_LIMIT}` **minutes, can't play !**"
        )

    title = audio.title
    file_name = get_file_name(audio)
    duration = convert_seconds(audio.duration)
    file_path = await converter.convert(
        (await message.reply_to_message.download(file_name))
        if not path.isfile(path.join("downloads", file_name))
        else file_name
    )
    chat_id = message.chat.id
    ACTV_CALLS = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))    
    if chat_id in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
            photo=f"{QUE_IMG}",
            caption=f"ð¡ **Track added to queue Â»** `{position}`\n\nð· **Name:** {title[:50]}\nâ± **Duration:** `{duration}`\nð§ **Request by:** {costumer}",
            reply_markup=keyboard,
        )
    else:
        await callsmusic.pytgcalls.join_group_call(
            chat_id, 
            InputStream(
                InputAudioStream(
                    file_path,
                ),
            ),
        )
        await message.reply_photo(
            photo=f"{AUD_IMG}",
            caption=f"ð· **Name:** {title[:50]}\nâ± **Duration:** `{duration}`\nð¡ **Status:** `Playing`\n"
            + f"ð§ **Request by:** {costumer}",
            reply_markup=keyboard,
        )

    return await lel.delete() 
