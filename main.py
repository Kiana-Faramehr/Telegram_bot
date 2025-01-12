from typing import Final
from telegram import Update,KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
from telegram.constants import ParseMode
import requests
from Canada import data

#///////
TOKEN: Final='7966714900:AAFxGbdeW4ijfsaszt1BTpbgs_8cRDZnpqY'
BOT_USERNAME: Final='@abroadin_apply_bot'

#//////////////

NAME, LAST_NAME, EMAIL, NUMBER =range(4)
COUNTRY,MAJOR=range(2)
ED_NAME=range(1)
ED_LAST=range(1)
ED_NUMBER=range(1)
ED_EMAIL=range(1)
user_info={'name':'','last_name':'','phone_number':'','email':''}
data_saved=[]             #saved supervisors
data_info=[]              #user information(name,....)
data_id={}                #user chat id and number

key=0

#///////////////////    Start

async def start(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_id=data_id):
    if update.effective_chat.id in data_id.keys():

        print("yes")

    else:
        l=len(data_id)
        data_id.update({update.effective_chat.id:l})
        data_info.append({'name':'☆Not Entered☆','last_name':'☆Not Entered☆','phone_number':'☆Not Entered☆','email':'☆Not Entered☆'})
        data_saved.append([])
        
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
    keys=[[KeyboardButton('❌ Cancel')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your first name:",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    return NAME

async def name(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_info=data_info,data_id=data_id):
    global key
    key=2
    keys=[[KeyboardButton('❌ Cancel')]]
    contex.user_data['name']=update.message.text
    data_info[data_id[update.effective_chat.id]]['name']=update.message.text
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your last name:",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    return LAST_NAME

async def last_name(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_info=data_info,data_id=data_id):
    global key
    key=3
    keys=[[KeyboardButton('❌ Cancel')]]
    contex.user_data['last_name']=update.message.text
    data_info[data_id[update.effective_chat.id]]['last_name']=update.message.text
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your phone number (with country code, e.g. 1234567890):",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    return NUMBER

async def phone_number(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_info=data_info,data_id=data_id):
    global key
    key=4
    keys=[[KeyboardButton('❌ Cancel')]]
    contex.user_data['phone_number']=update.message.text
    if update.message.text.isnumeric():
        data_info[data_id[update.effective_chat.id]]['phone_number']=update.message.text
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your email:",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    return EMAIL

async def email(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_info=data_info,data_id=data_id):
    global key
    keys=[  [KeyboardButton('👤 User Profile')],
            [KeyboardButton('❓ Help and Support'),KeyboardButton('💾 Saved Results')],
            [KeyboardButton('📋 View Profile'),KeyboardButton('🧑‍🏫 Search Supervisors')]]

    if "." in update.message.text and "@" in update.message.text:
        contex.user_data['email']=update.message.text
        data_info[data_id[update.effective_chat.id]]['email']=update.message.text
        await contex.bot.send_message(chat_id=update.effective_chat.id,
            text="You have loged in successfully.",
            reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
        key=0
        return ConversationHandler.END
    else:
        await phone_number(update,contex)

#//////////
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE,data_info=data_info,data_id=data_id):
    global key
    keys=[  [KeyboardButton('👤 User Profile')],
            [KeyboardButton('❓ Help and Support'),KeyboardButton('💾 Saved Results')],
            [KeyboardButton('📋 View Profile'),KeyboardButton('🧑‍🏫 Search Supervisors')]]
    key=0
    await context.bot.send_message(chat_id=update.effective_chat.id,
            text="Cancelled.",
            reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    return ConversationHandler.END


#////////////////////// View Profile

async def view(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_info=data_info,data_id=data_id):
    button_list=[[InlineKeyboardButton('Edit First Name',callback_data='name')],[InlineKeyboardButton('Edit Last Name',callback_data='last')],[InlineKeyboardButton('Edit Number',callback_data='number')],[InlineKeyboardButton('Edit Email',callback_data='email')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text=f"Your Profile: \n👤 First Name: {data_info[data_id[update.effective_chat.id]]['name']}\n👤 Last Name: {data_info[data_id[update.effective_chat.id]]['last_name']}\n📱 Phone Number: {data_info[data_id[update.effective_chat.id]]['phone_number']}\n📧 Email: {data_info[data_id[update.effective_chat.id]]['email']}"
        ,parse_mode=ParseMode.HTML
        ,reply_markup=InlineKeyboardMarkup(button_list))
    

async def edit_name(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    key=7
    keys=[[KeyboardButton('❌ Cancel')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your first name:",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    return ED_NAME

async def get_name(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_info=data_info,data_id=data_id):
    global key
    key=0
    keys=[  [KeyboardButton('👤 User Profile')],
            [KeyboardButton('❓ Help and Support'),KeyboardButton('💾 Saved Results')],
            [KeyboardButton('📋 View Profile'),KeyboardButton('🧑‍🏫 Search Supervisors')]]
    contex.user_data['name']=update.message.text
    data_info[data_id[update.effective_chat.id]]['name']=update.message.text
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Your name has been updated.",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    
async def edit_lastname(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    key=8
    keys=[[KeyboardButton('❌ Cancel')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your last name:",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    return ED_LAST

async def get_last(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_info=data_info,data_id=data_id):
    global key
    key=0
    keys=[  [KeyboardButton('👤 User Profile')],
            [KeyboardButton('❓ Help and Support'),KeyboardButton('💾 Saved Results')],
            [KeyboardButton('📋 View Profile'),KeyboardButton('🧑‍🏫 Search Supervisors')]]
    contex.user_data['last_name']=update.message.text
    data_info[data_id[update.effective_chat.id]]['last_name']=update.message.text
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Your last name has been updated.",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    
async def edit_number(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    key=9
    keys=[[KeyboardButton('❌ Cancel')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your number:",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    return ED_NUMBER

async def get_number(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_info=data_info,data_id=data_id):
    global key
    key=0
    keys=[  [KeyboardButton('👤 User Profile')],
            [KeyboardButton('❓ Help and Support'),KeyboardButton('💾 Saved Results')],
            [KeyboardButton('📋 View Profile'),KeyboardButton('🧑‍🏫 Search Supervisors')]]
    contex.user_data['phone_number']=update.message.text
    if update.message.text.isnumeric():
        data_info[data_id[update.effective_chat.id]]['phone_number']=update.message.text
        await contex.bot.send_message(chat_id=update.effective_chat.id,
            text="Your number has been updated.",
            reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    else:
        await contex.bot.send_message(chat_id=update.effective_chat.id,
            text="please enter your number correctly.",
            reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
        await edit_number(update,contex)        
    
async def edit_email(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    key=10
    keys=[[KeyboardButton('❌ Cancel')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter your email:",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    return ED_NAME

async def get_email(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_info=data_info,data_id=data_id):
    global key
    key=0
    keys=[  [KeyboardButton('👤 User Profile')],
            [KeyboardButton('❓ Help and Support'),KeyboardButton('💾 Saved Results')],
            [KeyboardButton('📋 View Profile'),KeyboardButton('🧑‍🏫 Search Supervisors')]]
    if "." in update.message.text and "@" in update.message.text:
        contex.user_data['email']=update.message.text
        data_info[data_id[update.effective_chat.id]]['email']=update.message.text
        await contex.bot.send_message(chat_id=update.effective_chat.id,
            text="Your email has been updated.",
            reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    else:
        await contex.bot.send_message(chat_id=update.effective_chat.id,
            text="please enter your email correctly.",
            reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
        await edit_email(update,contex)

#//////////////////////////  Supervisor

def full_word(sentence,word):
    key=False
    list_j=[0]             #creating a list inwhich the location of spaces and punctuations are stored
    sentence='a'+sentence    #adding a letter to the sentence because in my loop I can not check first letter of the sentence(in coding word, it can not check sentence[0])
    l=len(sentence)
    for i in range(l):                      #In this loop, we store the location of spaces and punctuations in our list
        if sentence[i].isalnum()==False:    #Checking if a sentence[i] is any punctuations or spaces
            list_j.append(i)              #If it is, the loop will store it in our list       
        if i==l-1:                        #It also store the last letter of the sentence
            list_j.append(l)
    s=len(list_j)
    for i in range(s-1):                 #In this loop, the function check if the word is in our sentence or not
        for j in range(i+1,s):
            if (list_j[j]-list_j[i])>1 and (sentence[list_j[i]+1:list_j[j]]).casefold() ==word.casefold():   #this if will check if between our two punctuations or spaces, there is a word or not and if it is, it will check if the word between these two punctuations is equall to our input word in the function or not. 
                key=True
                return key        #the function This function is case insensitive – meaning any combination of upper/lower case words are accepted as valid. If the word is equall to our input word in the function, the function will return True. Otherwise, it will return False.
    return key

def reduc_first_line(text):
    for i in range(len(text)):
        if text[i]=='\n':
            return text[i+1:]
        
async def supervisors(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    key=5
    #buttons
    #keys=[[KeyboardButton('Computer Science'),KeyboardButton('Main Menu')]]
    keys=[[KeyboardButton('🇨🇦Canada🇨🇦'),KeyboardButton('🇺🇸USA🇺🇸')],[KeyboardButton('🇦🇺Australia🇦🇺'),KeyboardButton('🇬🇧UK🇬🇧')],[KeyboardButton('❌ Cancel')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please select a country.",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True,one_time_keyboard=True))
    return COUNTRY

async def by_major(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    global key
    key=6
    contex.user_data['country']=update.message.text[2:-2]
    keys=[[KeyboardButton('❌ Cancel')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="To see a list of supervisors, please search your key world.( e.g. major or field of study or universitie's name )",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))
    return MAJOR

async def search(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_id=data_id,data_saved=data_saved):
    major=update.message.text
    global key
    key=0
    keys=[  [KeyboardButton('👤 User Profile')],
            [KeyboardButton('❓ Help and Support'),KeyboardButton('💾 Saved Results')],
            [KeyboardButton('📋 View Profile'),KeyboardButton('🧑‍🏫 Search Supervisors')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Searching...")   
    if contex.user_data['country']=='Canada':
        dt=data()
    for i in range(len(dt)):
        if full_word(dt[i],major):
            if dt[i] in data_saved[data_id[update.effective_chat.id]]:
                button_list=[[InlineKeyboardButton('Exists in your saved list. click to remove',callback_data=f'd{i}')]]
            else:
                button_list=[[InlineKeyboardButton('save',callback_data=f's{i}')]]
            await contex.bot.send_message(chat_id=update.effective_chat.id,
            text=reduc_first_line(dt[i]),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(button_list))
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Here is your search result",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))

    
async def by_country(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    keys=[[KeyboardButton('Canada'),KeyboardButton('Main Menu')]]
    await contex.bot.send_message(chat_id=update.effective_chat.id,
        text="Please enter the name of the country.",
        reply_markup=ReplyKeyboardMarkup(keys, resize_keyboard=True))

#///////////////    Majors

async def computer_science(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_id=data_id,data_saved=data_saved):

    dt=data()
    for i in range(len(data())):
        if dt[i] in data_saved[data_id[update.effective_chat.id]]:
            button_list=[[InlineKeyboardButton('Exists in your saved list. click to remove',callback_data=f'd{i}')]]
        else:
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
    msg=update.effective_message.text
    global key
    if key==0:
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
        if msg=="🏙By Country":
            await by_country(update,contex)
    elif key==1:
        if msg=='❌ Cancel':
            await cancel(update,contex)
        else:
            await name(update,contex)
    elif key==2:
        if msg=='❌ Cancel':
            await cancel(update,contex)
        else:
            await last_name(update,contex)
    elif key==3:
        if msg=='❌ Cancel':
            await cancel(update,contex)
        else:
            await phone_number(update,contex)
    elif key==4:
        if msg=='❌ Cancel':
            await cancel(update,contex)
        else:
            await email(update,contex)
    elif key==5:
        if msg=='❌ Cancel':
            await cancel(update,contex)
        else:
            await by_major(update,contex)
    elif key==6:
        if msg=='❌ Cancel':
            await cancel(update,contex)
        else:
            await search(update,contex)
    elif key==7:
        if msg=='❌ Cancel':
            await cancel(update,contex)
        else:
            await get_name(update,contex)
    elif key==8:
        if msg=='❌ Cancel':
            await cancel(update,contex)
        else:
            await get_last(update,contex)
    elif key==9:
        if msg=='❌ Cancel':
            await cancel(update,contex)
        else:
            await get_number(update,contex)
    elif key==10:
        if msg=='❌ Cancel':
            await cancel(update,contex)
        else:
            await get_email(update,contex)

#///////////////     saved

async def saved(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_info=data_info,data_id=data_id,data_saved=data_saved):
    await contex.bot.send_message(chat_id=update.effective_chat.id,
            text="Your saved results:")
    if len(data_saved[data_id[update.effective_chat.id]])==0:
        await contex.bot.send_message(chat_id=update.effective_chat.id,
            text="Your saved result list is empty")
    else:
        for i in range(len(data_saved[data_id[update.effective_chat.id]])):
            button_list=[[InlineKeyboardButton('remove',callback_data=f'r{i}')]]
            await contex.bot.send_message(chat_id=update.effective_chat.id,
                text=data_saved[data_id[update.effective_chat.id]][i],
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(button_list))

#////////////////// callback_query

async def callback_query_handler(update: Update, contex: ContextTypes.DEFAULT_TYPE,data_info=data_info,data_id=data_id,data_saved=data_saved):
    dt=data()
    query=update.callback_query
    call_back_data=query.data
    if call_back_data[0]=='s':
        call_back_data=call_back_data[1:len(call_back_data)]
        data_saved[data_id[update.effective_chat.id]].append(dt[int(call_back_data)])
        button_list=[[InlineKeyboardButton('Exists in your saved list. click to remove',callback_data=f'd{int(call_back_data)}')]]
        await query.edit_message_text(
            text=dt[int(call_back_data)],
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(button_list))

    elif call_back_data[0]=='r':
        call_back_data=call_back_data[1:len(call_back_data)]
        data_saved[data_id[update.effective_chat.id]].pop(int(call_back_data))
        await saved(update,contex)

    elif call_back_data[0]=='d':
        call_back_data=call_back_data[1:len(call_back_data)]
        data_saved[data_id[update.effective_chat.id]].remove(dt[int(call_back_data)])
        button_list=[[InlineKeyboardButton('save',callback_data=f's{int(call_back_data)}')]]
        await query.edit_message_text(
            text=dt[int(call_back_data)],
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(button_list))
    elif call_back_data=='name':
        await edit_name(update,contex)
    elif call_back_data=='last':
        await edit_lastname(update,contex)
    elif call_back_data=='number':
        await edit_number(update,contex)
    elif call_back_data=='email':
        await edit_email(update,contex)
    await query.answer()



 #//////////////////////////   

if __name__=='__main__':
    print("starting bot...")
    app = Application.builder().token(TOKEN).build()


    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('computer_science', computer_science))
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
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    conversation_handler2 = ConversationHandler(
        entry_points=[CommandHandler('Supervisor', supervisors)],
        states={
            COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, by_major)],
            MAJOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, search)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    conversation_handler3 = ConversationHandler(
        entry_points=[CommandHandler('edit_name', edit_name)],
        states={
            ED_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    conversation_handler4 = ConversationHandler(
        entry_points=[CommandHandler('edit_last_name', edit_lastname)],
        states={
            ED_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_last)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    conversation_handler5 = ConversationHandler(
        entry_points=[CommandHandler('edit_last_name', edit_number)],
        states={
            ED_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_number)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    conversation_handler6 = ConversationHandler(
        entry_points=[CommandHandler('edit_last_name',edit_email)],
        states={
            ED_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conversation_handler)
    app.add_handler(conversation_handler2)
    app.add_handler(conversation_handler3)
    app.add_handler(conversation_handler4)
    app.add_handler(conversation_handler5)
    app.add_handler(conversation_handler6)


    print('polling...')
    app.run_polling()