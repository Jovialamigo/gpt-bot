from aiogram import F, Router, html, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, URLInputFile

from funcs.chat import ask_chat, generate_image
from states import ChatState

router = Router()

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
    await message.answer("Подождите...")
    try:
        ans = await ask_chat(text=message.text, model="gpt-3.5-turbo")
        await message.answer(ans, parse_mode="Markdown")
    except:
        await message.answer("Sorry, an error occured. Try again.")


@router.message(ChatState.chat4)
async def gpt(message: types.Message):
    await message.answer("Подождите...")
    try:
        ans = await ask_chat(text=message.text, model="gpt-4")
        await message.answer(ans, parse_mode="Markdown")
    except:
        await message.answer("Sorry, an error occured. Try again.")


@router.message(ChatState.image)
async def image_gpt(message: types.Message):
    await message.answer("Подождите...")
    try:
        url = await generate_image(text=message.text)
        await message.answer_photo(photo=URLInputFile(url=url, filename="image.png"))
    except:
        await message.answer("Sorry, an error occured. Try again.")
