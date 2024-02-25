from aiogram.fsm.state import State, StatesGroup


class FSMQuestion(StatesGroup):
    question = State()


class FSMResume(StatesGroup):
    resume = State()


class FSMAdminAddFeedback(StatesGroup):
    date = State()
    time = State()


class FSMAdminMailing(StatesGroup):
    mail = State()
    success = State()
