from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMQuestion(StatesGroup):
    question = State()
    # send = State()


class FSMResume(StatesGroup):
    resume = State()


class FSMAddFeedback(StatesGroup):
    date = State()
    time = State()


class FSMDeleteFeedback(StatesGroup):
    feedback = State()


class FSMGetFeedback(StatesGroup):
    date = State()
    time = State()
    success = State()
