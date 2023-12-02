import logging
import time

from aiogram import F, Router, html, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, URLInputFile
from openai import AsyncOpenAI

from funcs import chat
from funcs.chat import ask_chat, generate_image
from states import ChatState

router = Router()
error_message = "Извините, произошла ошибка. Попробуйте еще раз 😔"


kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💬 Чат", callback_data="chat"),
            InlineKeyboardButton(text="🤖 Чат v4", callback_data="chat_4"),
            InlineKeyboardButton(text="🌁 Картинка", callback_data="image"),
        ]
    ]
)


@router.message(Command("chat"))
async def ans_chat(message: types.Message):
    await message.answer("Выбери тип:", reply_markup=kb)


@router.callback_query(F.data == "chat")
async def chat_call(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChatState.chat)
    await call.message.edit_text(
        text="💬 *Выбран режим текста GPT 3\.5*\n" "Введите запрос:\n ",
        parse_mode="MarkdownV2",
        reply_markup=kb,
    )


@router.callback_query(F.data == "chat_4")
async def chat_call(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChatState.chat4)
    await call.message.edit_text(
        text="🤖 *Выбран режим текста GPT 4*\n" "Введите запрос:\n ",
        parse_mode="MarkdownV2",
        reply_markup=kb,
    )


@router.callback_query(F.data == "image")
async def image_call(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChatState.image)
    await call.message.edit_text(
        text="🌁 *Выбран режим картинки*\n" "Введите описание:\n ",
        parse_mode="MarkdownV2",
        reply_markup=kb,
    )


@router.message(ChatState.chat)
async def gpt(message: types.Message):
    msg = await message.answer("Подождите...", parse_mode="Markdown")
    msg_id = msg.message_id
    chat_id = message.chat.id
    try:
        ans = await ask_chat(text=message.text, model="gpt-3.5-turbo")
        await message.bot.edit_message_text(
            text=ans,
            message_id=msg_id,
            chat_id=chat_id,
            parse_mode="Markdown",
        )
    except:
        await message.answer(error_message)


# @router.message(ChatState.chat4)
# async def gpt(message: types.Message):
#     ms = await message.answer("Подождите...", parse_mode="Markdown")
#     msg_id = ms.message_id

#     stream = await client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {
#                 "role": "user",
#                 "content": message.text,
#             },
#         ],
#         stream=True,
#     )

#     l = ""
#     async for part in stream:
#         if part.choices[0].finish_reason == "stop":
#             break
#         if part.choices[0].delta.content == "":
#             continue
#         res = part.choices[0].delta.content
#         l += res
#         if ("." or ":") in res:
#             try:
#                 await message.bot.edit_message_text(
#                     text=l,
#                     message_id=msg_id,
#                     chat_id=message.chat.id,
#                     parse_mode="Markdown",
#                 )
#             except:
#                 logging.warning(f"Failed to edit text: {res}")
#         else:
#             print("Continue")


@router.message(ChatState.chat4)
async def gpt(message: types.Message):
    msg = await message.answer("Подождите...", parse_mode="Markdown")
    msg_id = msg.message_id
    chat_id = message.chat.id
    try:
        ans = await ask_chat(text=message.text, model="gpt-4-1106-preview")
        await message.bot.edit_message_text(
            text=ans,
            message_id=msg_id,
            chat_id=chat_id,
            parse_mode="Markdown",
        )
    except:
        await message.answer(error_message)


# image description handler
@router.message(ChatState.image)
async def image_gpt(message: types.Message):
    await message.answer("Подождите...")
    try:
        url = await generate_image(text=message.text)
        await message.answer_photo(photo=URLInputFile(url=url, filename="image.png"))
    except:
        await message.answer(error_message)


# Raise when no chat type is chosen
@router.message()
async def type_not_chosen(message: types.Message):
    await message.answer("Выберите режим, нажав /chat")
