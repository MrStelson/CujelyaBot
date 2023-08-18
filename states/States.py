from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMQuestion(StatesGroup):
    question = State()
    # send = State()


class FSMResume(StatesGroup):
    resume = State()


class FSMAdminAddFeedback(StatesGroup):
    date = State()
    time = State()


class FSMAdminMailing(StatesGroup):
    mail = State()
    success = State()
