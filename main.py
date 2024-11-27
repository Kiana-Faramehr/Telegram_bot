from typing import Final
from telegram import Update,KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import requests


TOKEN: Final='7966714900:AAFxGbdeW4ijfsaszt1BTpbgs_8cRDZnpqY'
BOT_USERNAME: Final='@abroadin_apply_bot'


#Commands
async def start_command(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    await contex.bot.send_message(chat_id=update._effective_chat.id,text="Hello! Welcome to the bot! 🌟We’re here to support you on your academic journey. Please choose an option from the main menu to get started! It’s recommended to complete your user profile first in the «User Profile» section. 😊")

async def Supervisors(update: Update, contex: ContextTypes.DEFAULT_TYPE):

    button_list=[[InlineKeyboardButton('save',url='t.me/aryan_fr1')]]



    txt="""
👨‍🏫 Supervisor Information

• Supervisor: Dr N Zincir-Heywood

🎓 Details of Open Research Position

👤 Cyber Security and Resilience

🏅 Level: PhD
🌍 Country: Canada
🏛 University: Dalhousie University
🔬 Branch: Faculty of Computer Science

📝 Overview:
In this research project, we are going to work on monitoring and analysis of adversity and changes in the communication networks and services using machine learning and artificial intelligence approaches.

🏷 Tags:
• Artificial Intelligence
• Cyber Security
• Machine Learning
• Networks
• Computer Science

🔗 Online Profiles:
• <a href='https://ca.linkedin.com/in/nur-zincir-heywood-30a4456'>LinkedIn</a>

• <a href='https://scholar.google.com/citations?user=F9nG0F4AAAAJ&hl=zh-CN'>Google Scholar</a>

"""
    await contex.bot.send_message(chat_id=update.effective_chat.id,text=txt,parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup(button_list))

if __name__=='__main__':
    print("starting bot...")
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start', start_command))
    #app.add_handler(CommandHandler('help', help_command))
    #app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('Supervisor', Supervisors))


    print('polling...')
    app.run_polling(poll_interval=3)