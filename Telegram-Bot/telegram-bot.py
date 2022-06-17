from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import exchange
 
# IMPORTANTE: inserire il token fornito dal BotFather nella seguente stringa
TOKEN="5230743453:AAGtLRSax96d_EV1F7uXQBLPirxaP6KSi84"
 
def extract_number(text):
     return text.split()[1].strip()
 
def convert_usd(update, context):
     usd=float(extract_number(update.message.text))
     eur=exchange.from_usd_to_eur(usd)
     print(f'Eseguita conversione da {usd} USD a {eur} EUR')
     update.message.reply_text(f'{eur} EUR')
 
def convert_eur(update, context):
     eur=float(extract_number(update.message.text))
     usd=exchange.from_eur_to_usd(eur)
     print(f'Eseguita conversione da {eur} EUR a {usd} USD')
     update.message.reply_text(f'{usd} USD')
 
def main():
   upd= Updater(TOKEN, use_context=True)
   disp=upd.dispatcher
 
   disp.add_handler(CommandHandler("usd", convert_usd))
   disp.add_handler(CommandHandler("eur", convert_eur))
 
   upd.start_polling()
 
   upd.idle()
 
if __name__=='__main__':
   main()