from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.utils.executor import start_polling
from aiogram.dispatcher.filters import Text


from src.config import *
from src.services.database import *
from src.keyboards.keyboards import *

bot = Bot(token, parse_mode='HTML')
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_handler(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    if user is None:
        await set_user(user_id)
        await message.answer('Main menu', reply_markup=kb_menu)
    else:
        if user[3] == 'None':
            await message.answer('Main menu', reply_markup=kb_menu)


@dp.message_handler(Text(equals='Find Pal'))
async def choose_sex(message: Message):
    await message.answer('Choose sex of your pal', reply_markup=kb_choose_sex)


@dp.message_handler(Text(equals='Change sex'))
async def change_sex(message: Message):
    await message.answer('Choose your sex', reply_markup=kb_edit_sex)


@dp.message_handler(Text(equals='Stop dialog'))
async def stop_dialogue(message: Message):
    user_id = message.from_user.id
    partner = await stop_dialog(user_id)
    await message.answer("Dialog is end")
    await start_handler(message)
    await bot.send_message(partner, "Dialog is end")
    await bot.send_message(partner, "Main menu", reply_markup=kb_menu)


@dp.message_handler(Text(equals='Stop searching'))
async def stop_finding(message: Message):
    user_id = message.from_user.id
    await stop_find(user_id)
    await message.answer('Searching stopped')
    await start_handler(message)


@dp.message_handler(Text(equals='New pal'))
async def new_pal(message: Message):
    user_id = message.from_user.id
    partner = await stop_dialog(user_id)
    await message.answer('Dialog is stopped', reply_markup=ReplyKeyboardRemove())
    await message.answer('Choose sex of your pal', reply_markup=kb_choose_sex)
    await bot.send_message(partner, 'Dialog is stopped', reply_markup=ReplyKeyboardRemove())
    await bot.send_message(partner, 'Choose sex of your pal', reply_markup=kb_choose_sex)


@dp.callback_query_handler()
async def call_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    text = callback.data
    if text.startswith('edit_sex_'):
        sex = text.split('_')[2]
        await edit_sex(user_id, sex)
        await callback.answer(f'Sex changed successful to {sex}')
        await bot.delete_message(user_id, callback.message.message_id)
        await callback.message.answer("Main menu", reply_markup=kb_menu)
    elif text.startswith('choose_sex_'):
        sex = text.split('_')[2]
        if sex == 'r':
            await bot.delete_message(user_id, callback.message.message_id)
            msg = await callback.message.answer("Searching pal...", reply_markup=kb_find)
            await set_message(user_id, msg.message_id)
            resp = await find_sexless(user_id)
        else:
            await bot.delete_message(user_id, callback.message.message_id)
            msg = await callback.message.answer("Searching pal...", reply_markup=kb_find)
            await set_message(user_id, msg.message_id)
            resp = await find(user_id, sex)
        if resp is not None:
            await bot.delete_message(user_id, msg.message_id)
            await callback.message.answer("Your pal found, talk", reply_markup=kb_dialog)
            user = await get_user(resp)
            await bot.delete_message(resp, user[4])
            await bot.send_message(resp, text="Your pal found, talk", reply_markup=kb_dialog)


@dp.message_handler(content_types=types.ContentType.ANY)
async def dialog(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    if user[3] != 'None':
        if message.content_type == 'text':
            await bot.send_message(user[3], message.text)
        elif message.content_type == 'voice':
            voice_file_id = message.voice.file_id
            await bot.send_audio(user[3], voice_file_id)
        elif message.content_type == 'photo':
            photo_file_id = message.photo[-1].file_id
            await bot.send_photo(user[3], photo_file_id)
        elif message.content_type == 'video':
            video_file_id = message.video.file_id
            await bot.send_video(user[3], video_file_id)
        elif message.content_type == 'audio':
            audio_file_id = message.audio.file_id
            await bot.send_audio(user[3], audio_file_id)
        elif message.content_type == 'document':
            document_file_id = message.document.file_id
            await bot.send_document(user[3], document_file_id)
        elif message.content_type == 'sticker':
            sticker_file_id = message.sticker.file_id
            await bot.send_sticker(user[3], sticker_file_id)
        elif message.content_type == 'animation':
            animation_file_id = message.animation.file_id
            await bot.send_animation(user[3], animation_file_id)
        elif message.content_type == 'video_note':
            video_note_file_id = message.video_note.file_id
            await bot.send_video_note(user[3], video_note_file_id)
        elif message.content_type == 'location':
            await bot.send_location(user[3], message.location.latitude, message.location.longitude)
        elif message.content_type == 'contact':
            await bot.send_contact(user[3], message.contact.phone_number, message.contact.first_name)
        elif message.content_type == 'game':
            await bot.send_game(user[3], message.game.short_name)
        elif message.content_type == 'dice':
            await bot.send_dice(user[3], emoji=message.dice.emoji)
        elif message.content_type == 'venue':
            await bot.send_venue(user[3], message.venue.location.latitude, message.venue.location.longitude,
                                 message.venue.title, message.venue.address)
        elif message.content_type == 'voice_note':
            voice_note_file_id = message.voice_note.file_id
            await bot.send_voice(user[3], voice_note_file_id)


if __name__ == '__main__':
    start_polling(dispatcher=dp, skip_updates=True)
