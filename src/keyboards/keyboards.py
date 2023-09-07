from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(KeyboardButton("Find Pal"))
kb_menu.add(KeyboardButton("Change sex"))

kb_choose_sex = InlineKeyboardMarkup(row_width=3)
kb_choose_sex.add(InlineKeyboardButton("M", callback_data='choose_sex_m'),
                  InlineKeyboardButton("F", callback_data='choose_sex_f'),
                  InlineKeyboardButton("?", callback_data='choose_sex_r'))

kb_edit_sex = InlineKeyboardMarkup(row_width=3)
kb_edit_sex.add(InlineKeyboardButton("M", callback_data='edit_sex_m'),
                InlineKeyboardButton("F", callback_data='edit_sex_f'),
                InlineKeyboardButton("?", callback_data='edit_sex_r'))

kb_find = ReplyKeyboardMarkup(resize_keyboard=True)
kb_find.add(KeyboardButton("Stop searching"))

kb_dialog = ReplyKeyboardMarkup(resize_keyboard=True)
kb_dialog.add(KeyboardButton("Stop dialog"))
kb_dialog.add(KeyboardButton("New pal"))


