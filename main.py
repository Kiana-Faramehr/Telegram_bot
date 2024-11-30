from typing import Final
from telegram import Update,KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from telegram.constants import ParseMode
import requests
from list import data

#///////
TOKEN: Final='7966714900:AAFxGbdeW4ijfsaszt1BTpbgs_8cRDZnpqY'
BOT_USERNAME: Final='@abroadin_apply_bot'

#//////////////

NAME, LAST_NAME, EMAIL =range(3)
user_data=[]
key=0

#///////////////////    Start

async def start(update: Update, contex: ContextTypes.DEFAULT_TYPE):
        
    #buttons
    keys=[  [KeyboardButton('👤 User Profile')],
            [KeyboardButton('❓ Help and Support'),KeyboardButton('💾 Saved Results')],
            [KeyboardButton('📋 View/Edit Profile'),KeyboardButton('🧑‍🏫 Search Supervisors')]]
    
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Hello! Welcome to the bot! 🌟We’re here to support you on your academic journey. Please choose an option from the main menu to get started! It’s recommended to complete your user profile first in the «User Profile» section. 😊",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    
#///////////////////    Help

async def help(update: Update, contex: ContextTypes.DEFAULT_TYPE):

    txt="""
Dear Aryan, Welcome to the Help and Support section of the bot!

Our mission is to make your journey to find academic opportunities and connect with potential supervisors as seamless as possible. Here's a quick guide to get you started:

🔍 Search Opportunities: Discover academic programs and positions tailored to your profile or start a new search based on your preferences.
👤 User Profile: Set up or update your personal information to get personalized recommendations.
📋 View/Edit Profile: Review or make changes to your existing profile to keep your information up-to-date.
🧑‍🏫 Search Supervisors: Find potential supervisors aligned with your research interests to advance your academic career.
💾 Saved Results: Access and manage the positions and supervisors you've saved for future reference.

We're here to support you in your academic journey and help you achieve your goals. If you have any questions or need further assistance, feel free to reach out."""

    button_list=[[InlineKeyboardButton('Contact Support',url='t.me/aryan_fr1')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
            text=txt,
            reply_markup=InlineKeyboardMarkup(button_list))

#////////////////////   User

async def user(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    key=1
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your first name:")
    return NAME

async def name(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    key=2
    contex.user_data['name']=update.message.text
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your last name:")
    return LAST_NAME

async def last_name(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    key=3
    contex.user_data['last name']=update.message.text
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your email:")
    return EMAIL

async def email(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    key=0
    contex.user_data['email']=update.message.text
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text=f"You have loged in successfully. You are {contex.user_data['name']} {contex.user_data['last name']} and your email is {contex.user_data['email']}")
    return ConversationHandler.END

#//////////////////////////  Supervisor

async def supervisors(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    
    #buttons
    keys=[[KeyboardButton('Computer Science')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Dear l, To see a list of supervisors, please enter a keyword related to your research interest or field of study",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))

#///////////////    Majors

async def computer_science(update: Update, contex: ContextTypes.DEFAULT_TYPE):

    button_list=[[InlineKeyboardButton('save',url='t.me/aryan_fr1')]]
    dt=data()
    for i in range(len(data())):
        await contex.bot.send_message(chat_id=update.effective_chat.id,
            text=dt[i],
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(button_list))


async def custom(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    if key==0:
        msg=update.effective_message.text
        if msg=="🧑‍🏫 Search Supervisors":
            await supervisors(update,contex)
        if msg=="Computer Science":
            await computer_science(update,contex)
        if msg=="👤 User Profile":
            await user(update,contex)
        if msg=="❓ Help and Support":
            await help(update,contex)
    elif key==1:
        await name(update,contex)
    elif key==2:
        await last_name(update,contex)
    elif key==3:
        await email(update,contex)

#////////////////////////////

if __name__=='__main__':
    print("starting bot...")
    app = Application.builder().token(TOKEN).build()


    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('computer_science', computer_science))
    app.add_handler(CommandHandler('Supervisor', supervisors))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) ,  custom))

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('user', user)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, last_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
        },
        fallbacks=[],
    )
    app.add_handler(conversation_handler)


    print('polling...')
    app.run_polling(poll_interval=3)