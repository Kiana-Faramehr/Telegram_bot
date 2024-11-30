from typing import Final
from telegram import Update,KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
from telegram.constants import ParseMode
import requests
from list import data

#///////
TOKEN: Final='7966714900:AAFxGbdeW4ijfsaszt1BTpbgs_8cRDZnpqY'
BOT_USERNAME: Final='@abroadin_apply_bot'

#//////////////

NAME, LAST_NAME, EMAIL, NUMBER =range(4)
user_info={'name':'','last_name':'','phone_number':'','email':''}
user_saved=[]
key=0

#///////////////////    Start

async def start(update: Update, contex: ContextTypes.DEFAULT_TYPE):
        
    #buttons
    keys=[  [KeyboardButton('👤 User Profile')],
            [KeyboardButton('❓ Help and Support'),KeyboardButton('💾 Saved Results')],
            [KeyboardButton('📋 View Profile'),KeyboardButton('🧑‍🏫 Search Supervisors')]]
    
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Hello! Welcome to the bot! 🌟We’re here to support you on your academic journey. Please choose an option from the main menu to get started! It’s recommended to complete your user profile first in the «User Profile» section. 😊",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    
#///////////////////    Help

async def help(update: Update, contex: ContextTypes.DEFAULT_TYPE):

    txt="""
Welcome to the Help and Support section of the bot!

Our mission is to make your journey to find academic opportunities and connect with potential supervisors as seamless as possible. Here's a quick guide to get you started:

🔍 Search Opportunities: Discover academic programs and positions tailored to your profile or start a new search based on your preferences.
👤 User Profile: Set up or update your personal information to get personalized recommendations.
📋 View/Edit Profile: Review or make changes to your existing profile to keep your information up-to-date.
🧑‍🏫 Search Supervisors: Find potential supervisors aligned with your research interests to advance your academic career.
💾 Saved Results: Access and manage the positions and supervisors you've saved for future reference.

We're here to support you in your academic journey and help you achieve your goals. If you have any questions or need further assistance, feel free to reach out."""

    button_list=[[InlineKeyboardButton('Contact Support',url='t.me/abroadin_support')]]
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
    global user_info
    global key
    key=2
    contex.user_data['name']=update.message.text
    user_info['name']=update.message.text
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your last name:")
    return LAST_NAME

async def last_name(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global user_info
    global key
    key=3
    contex.user_data['last_name']=update.message.text
    user_info['last_name']=update.message.text
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your phone number (with country code, e.g. +1234567890):")
    return NUMBER

async def phone_number(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    global user_info
    key=4
    contex.user_data['phone_number']=update.message.text
    if user_info['phone_number']=='':
        user_info['phone_number']=update.message.text
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your email:")
    return EMAIL

async def email(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    keys=[  [KeyboardButton('👤 User Profile')],
            [KeyboardButton('❓ Help and Support'),KeyboardButton('💾 Saved Results')],
            [KeyboardButton('📋 View Profile'),KeyboardButton('🧑‍🏫 Search Supervisors')]]
    global key
    global user_info
    if ".com" in update.message.text and "@" in update.message.text:
        contex.user_data['email']=update.message.text
        user_info['email']=update.message.text
        await contex.bot.send_message(chat_id=update.effective_chat.id,
            text="You have loged in successfully.",
            reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
        key=0   
        return ConversationHandler.END
    else:
        await phone_number(update,contex)

#////////////////////// View Profile

async def view(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global user_info
    await contex.bot.send_message(chat_id=update.effective_chat.id,
            text=f"Your Profile: \n👤 First Name: {user_info['name']}\n👤 Last Name: {user_info['last_name']}\n📱 Phone Number: {user_info['phone_number']}\n📧 Email: {user_info['email']}")

#//////////////////////////  Supervisor

async def supervisors(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    
    #buttons
    keys=[[KeyboardButton('Computer Science'),KeyboardButton('Main Menu')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="To see a list of supervisors, please enter your field of study.",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))

#///////////////    Majors

async def computer_science(update: Update, contex: ContextTypes.DEFAULT_TYPE):

    dt=data()
    for i in range(len(data())-1,-1,-1):
        button_list=[[InlineKeyboardButton('save',callback_data=f's{i}')]]
        await contex.bot.send_message(chat_id=update.effective_chat.id,
            text=dt[i],
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(button_list))
        

async def menu(update: Update, contex: ContextTypes.DEFAULT_TYPE):
        
    #buttons
    keys=[  [KeyboardButton('👤 User Profile')],
            [KeyboardButton('❓ Help and Support'),KeyboardButton('💾 Saved Results')],
            [KeyboardButton('📋 View Profile'),KeyboardButton('🧑‍🏫 Search Supervisors')]]
    
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Here is the main menu",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))


#//////////////      Controller

async def controller(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    if key==0:
        msg=update.effective_message.text
        if msg=="🧑‍🏫 Search Supervisors":
            await supervisors(update,contex)
        if msg.lower()=="computer science":
            await computer_science(update,contex)
        if msg=="👤 User Profile":
            await user(update,contex)
        if msg=="❓ Help and Support":
            await help(update,contex)
        if msg=="💾 Saved Results":
            await saved(update,contex)
        if msg=="Main Menu":
            await menu(update,contex)
        if msg=="📋 View Profile":
            await view(update,contex)
    elif key==1:
        await name(update,contex)
    elif key==2:
        await last_name(update,contex)
    elif key==3:
        await phone_number(update,contex)
    elif key==4:
        await email(update,contex)

#///////////////     saved

async def saved(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    await contex.bot.send_message(chat_id=update.effective_chat.id,
            text="Your saved results:")
    global user_saved
    if len(user_saved)==0:
        await contex.bot.send_message(chat_id=update.effective_chat.id,
            text="Your saved result list is empty")
    else:
        for i in range(len(user_saved)):
            button_list=[[InlineKeyboardButton('remove',callback_data=f'r{i}')]]
            await contex.bot.send_message(chat_id=update.effective_chat.id,
                text=user_saved[i],
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(button_list))

#////////////////// callback_query

async def callback_query_handler(update: Update, contex: ContextTypes.DEFAULT_TYPE):

    dt=data()
    query=update.callback_query
    call_back_data=query.data
    if call_back_data[0]=='s':
        call_back_data=call_back_data[1:len(call_back_data)]
        user_saved.append(dt[int(call_back_data)])
    elif call_back_data[0]=='r':
        call_back_data=call_back_data[1:len(call_back_data)]
        user_saved.pop(int(call_back_data))
        await saved(update,contex)
    await query.answer()
    await query.message(text="Saved")


 #//////////////////////////   

if __name__=='__main__':
    print("starting bot...")
    app = Application.builder().token(TOKEN).build()


    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('computer_science', computer_science))
    app.add_handler(CommandHandler('Supervisor', supervisors))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('view_profile', view))
    app.add_handler(CommandHandler('saved_results', saved))
    app.add_handler(CommandHandler('main_menu', menu))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) ,  controller))
    app.add_handler(CallbackQueryHandler(callback_query_handler))

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('user', user)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, last_name)],
            NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_number)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
        },
        fallbacks=[],
    )
    app.add_handler(conversation_handler)


    print('polling...')
    app.run_polling()