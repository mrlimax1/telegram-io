from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from typing import List


def get_sites_kb(
        sites: List[str]
) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True
    )
    for site in sites:
        kb.add(
            KeyboardButton(site)
        )
    return kb


def get_response_data_kb(
        site_name: str
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            'Отметить отвеченной', callback_data=f"set_answer_{site_name}"
        )
    )


def get_site_data_kb(
        response_id: int
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Просмотренные", callback_data=f"response_watched_{response_id}")
    ).add(
        InlineKeyboardButton("Непросмотренные", callback_data=f"response_unwatched_{response_id}")
    ).add(
        InlineKeyboardButton("Отвеченные", callback_data=f"response_answered_{response_id}")
    )
