from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes 


TOKEN: Final='7966714900:AAFxGbdeW4ijfsaszt1BTpbgs_8cRDZnpqY'
BOT_USERNAME: Final='@abroadin_apply_bot'


#Commands
async def start_command(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Welcome to the bot! 🌟We’re here to support you on your academic journey. Please choose an option from the main menu to get started! It’s recommended to complete your user profile first in the «User Profile» section. 😊')

async def help_command(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Help and Support section of the bot!\n\nOur mission is to make your journey to find academic opportunities and connect with potential supervisors as seamless as possible. Here's a quick guide to get you started:\n\n🔍 Search Opportunities: Discover academic programs and positions tailored to your profile or start a new search based on your preferences.\n👤 User Profile: Set up or update your personal information to get personalized recommendations.\n📋 View/Edit Profile: Review or make changes to your existing profile to keep your information up-to-date.\n🧑‍🏫 Search Supervisors: Find potential supervisors aligned with your research interests to advance your academic career.\n💾 Saved Results: Access and manage the positions and supervisors you've saved for future reference.")

async def custom_command(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("this is a custom command")


if __name__=='__main__':
    print("starting bot...")
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))


    print('polling...')
    app.run_polling(poll_interval=5)

