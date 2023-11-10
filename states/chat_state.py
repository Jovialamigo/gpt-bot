from aiogram.fsm.state import State, StatesGroup


class ChatState(StatesGroup):
    chat = State()
    chat4 = State()
    image = State()
