from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, URLInputFile

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

kb2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💬 Чат", callback_data="chat"),
            InlineKeyboardButton(text="🤖 Чат v4", callback_data="chat_4"),
            InlineKeyboardButton(text="🌁 Картинка", callback_data="image"),
        ],
        [
            InlineKeyboardButton(text="✅ 1024x1024", callback_data="1024x1024"),
            InlineKeyboardButton(text="1024x1792", callback_data="1024x1792"),
            InlineKeyboardButton(text="1792x1024", callback_data="1792x1024"),
        ],
        [
            InlineKeyboardButton(text="✅ Standard", callback_data="standard"),
            InlineKeyboardButton(text="HD", callback_data="hd"),
        ],
    ]
)
size_list = (
    "1024x1024",
    "1024x1792",
    "1792x1024",
)
quality_list = (
    "standard",
    "hd",
)
size_dic = dict.fromkeys(size_list, False)
quality_dic = dict.fromkeys(quality_list, False)


def emoji_converter(value: bool) -> str:
    if value:
        res = "✅ "
    else:
        res = ""
    return res


@router.message(Command("chat"))
async def ans_chat(message: types.Message):
    await message.answer("Выбери тип:", reply_markup=kb)


@router.callback_query(F.data == "chat")
async def chat_call_4(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChatState.chat)
    await call.message.edit_text(
        text="💬 *Выбран режим текста GPT4o mini*\n" "Введите запрос:\n ",
        parse_mode="MarkdownV2",
        reply_markup=kb,
    )


@router.callback_query(F.data == "chat_4")
async def chat_call_3(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChatState.chat4)
    await call.message.edit_text(
        text="🤖 *Выбран режим текста GPT4o*\n" "Введите запрос:\n ",
        parse_mode="MarkdownV2",
        reply_markup=kb,
    )


@router.callback_query(F.data == "image")
async def image_call(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChatState.image)
    await state.set_data(quality_dic)
    await state.set_data(
        {
            "quality": "standard",
            "size": "1024x1024",
            "standard": True,
            "1024x1024": True,
        }
    )

    await call.message.edit_text(
        text="🌁 *Выбран режим картинки*\n" "Введите описание:\n ",
        parse_mode="MarkdownV2",
        reply_markup=kb2,
    )


@router.callback_query(
    F.data.in_(["standard", "hd", "1024x1024", "1024x1792", "1792x1024"])
)
async def quality_button(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data

    if call_data in ("standard", "hd"):
        await state.update_data({"quality": call_data})
        await state.update_data(
            {
                "standard": False,
                "hd": False,
            }
        )
        await state.update_data({call_data: True})

    if call_data in ("1024x1024", "1024x1792", "1792x1024"):
        await state.update_data({"size": call_data})
        await state.update_data(
            {
                "1024x1024": False,
                "1024x1792": False,
                "1792x1024": False,
            }
        )
        await state.update_data({call_data: True})

    data = await state.get_data()

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💬 Чат", callback_data="chat"),
                InlineKeyboardButton(text="🤖 Чат v4", callback_data="chat_4"),
                InlineKeyboardButton(text="🌁 Картинка", callback_data="image"),
            ],
            [
                InlineKeyboardButton(
                    text=f"{emoji_converter(data.get('1024x1024'))}1024x1024",
                    callback_data="1024x1024",
                ),
                InlineKeyboardButton(
                    text=f"{emoji_converter(data.get('1024x1792'))}1024x1792",
                    callback_data="1024x1792",
                ),
                InlineKeyboardButton(
                    text=f"{emoji_converter(data.get('1792x1024'))}1792x1024",
                    callback_data="1792x1024",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"{emoji_converter(data.get('standard'))}Standard",
                    callback_data="standard",
                ),
                InlineKeyboardButton(
                    text=f"{emoji_converter(data.get('hd'))}HD",
                    callback_data="hd",
                ),
            ],
        ]
    )

    await state.set_state(ChatState.image)
    await call.message.edit_text(
        text=(
            "🌁 *Выбран режим картинки*\nВведите описание:\n(по возможности старайтесь пользоваться обычным качеством)\n"
        ),
        parse_mode="MarkdownV2",
        reply_markup=kb,
    )


@router.message(ChatState.chat)
async def gpt(message: types.Message):
    msg = await message.answer("Подождите...", parse_mode="Markdown")
    msg_id = msg.message_id
    chat_id = message.chat.id
    try:
        ans, price = await ask_chat(text=message.text, model="gpt-4o-mini")
        await message.bot.edit_message_text(
            text=ans,
            message_id=msg_id,
            chat_id=chat_id,
            parse_mode="Markdown",
        )
    except:
        await message.answer(error_message)


@router.message(ChatState.chat4)
async def gpt4(message: types.Message):
    msg = await message.answer("Подождите...", parse_mode="Markdown")
    msg_id = msg.message_id
    chat_id = message.chat.id
    try:
        ans, price = await ask_chat(text=message.text, model="gpt-4o")
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
async def image_gpt(message: types.Message, state: FSMContext):
    await message.answer("Подождите...")
    data = await state.get_data()
    quality = data.get("quality")
    size = data.get("size")
    if not quality:
        quality = "standard"
    if not size:
        size = "1024x1024"
    try:
        url, price = await generate_image(text=message.text, quality=quality, size=size)
        await message.answer_photo(photo=URLInputFile(url=url, filename="image.png"))
    except:
        await message.answer(error_message)


# Raise when no chat type is chosen
@router.message()
async def type_not_chosen(message: types.Message):
    await message.answer("Выберите режим, нажав /chat")
