from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_fsm_button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(
            text='Відмінити'
        )]],
    resize_keyboard=True
)

view_my_cards_button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(
            text='Переглянути мої картки'
        )]],
    resize_keyboard=True,
    one_time_keyboard=True
)