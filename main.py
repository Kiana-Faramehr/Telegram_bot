from typing import Final
from telegram import Update,KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import requests
from list import data

TOKEN: Final='7966714900:AAFxGbdeW4ijfsaszt1BTpbgs_8cRDZnpqY'
BOT_USERNAME: Final='@abroadin_apply_bot'


#Commands
async def start_command(update: Update, contex: ContextTypes.DEFAULT_TYPE):
        
    #buttons
    keys=[  [KeyboardButton('👤 User Profile')],
            [KeyboardButton('❓ Help and Support'),KeyboardButton('💾 Saved Results')],
            [KeyboardButton('📋 View/Edit Profile'),KeyboardButton('🧑‍🏫 Search Supervisors')]]
    
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Hello! Welcome to the bot! 🌟We’re here to support you on your academic journey. Please choose an option from the main menu to get started! It’s recommended to complete your user profile first in the «User Profile» section. 😊",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))

async def supervisors(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    
    #buttons
    keys=[[KeyboardButton('Computer Science')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Dear l, To see a list of supervisors, please enter a keyword related to your research interest or field of study",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))


async def computer_science(update: Update, contex: ContextTypes.DEFAULT_TYPE):

    button_list=[[InlineKeyboardButton('save',url='t.me/aryan_fr1')]]
    dt=data()
    for i in range(len(data())):
        await contex.bot.send_message(chat_id=update.effective_chat.id,
            text=dt[i],
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(button_list))


async def custom(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    msg=update.effective_message.text
    if msg=="🧑‍🏫 Search Supervisors":
        await supervisors(update,contex)
    elif msg=="Computer Science":
        await computer_science(update,contex)





if __name__=='__main__':
    print("starting bot...")
    app = Application.builder().token(TOKEN).build()


    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('computer_science', computer_science))
    app.add_handler(CommandHandler('Supervisor', supervisors))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) ,  custom))


    print('polling...')
    app.run_polling(poll_interval=3)