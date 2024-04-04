from aiogram.fsm.state import StatesGroup, State


class ShopCardStates(StatesGroup):
    waiting_shop_name = State()
    waiting_shop_card = State()


class ConfirmDeleteState(StatesGroup):
    waiting_confirmation = State()
