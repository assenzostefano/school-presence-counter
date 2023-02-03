from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import datetime
import gspread
import telebot
import schedule
import os

load_dotenv()
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_BOT = os.getenv('OWNER_BOT')

bot = telebot.TeleBot(BOT_TOKEN)
scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
    ]

credentials = ServiceAccountCredentials.from_json_keyfile_name("token.json", scopes) #access the json key you downloaded earlier 
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open_by_key(SPREADSHEET_ID) #open sheet

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, I am a bot')

@bot.message_handler(commands=['assente'])
def assente(pm):
    try:
        sent_msg = bot.send_message(pm.chat.id, "Invio messaggio di assenza...")
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y")
        for i in range(1, 10):
            if sheet.get_worksheet(0).cell(i,1).value == now:
                sheet.get_worksheet(0).update_cell(i, 2, "0")
            else:
                continue

        bot.send_message(pm.chat.id, "Sei stato segnato assente")
    except:
        bot.send_message(pm.chat.id, "Si è verificato un errore, riprova più tardi")

@bot.message_handler(commands=['assente_spec'])
def assente_spec(pm):
    sent_msg = bot.send_message(pm.chat.id, "Invio messaggio di assenza...")
    bot.send_message(pm.chat.id, "Scrivi la data in formato gg/mm/aaaa")
    bot.register_next_step_handler(sent_msg, assente_spec_next)

def assente_spec_next(pm):
    try:
        for i in range(1, 10):
            if sheet.get_worksheet(0).cell(i,1).value == pm.text:
                sheet.get_worksheet(0).update_cell(i, 2, "0")
            else:
                continue

        bot.send_message(pm.chat.id, "Sei stato segnato assente")
    except:
        bot.send_message(pm.chat.id, "Si è verificato un errore, riprova più tardi")

def presenza_giornaliera():
    try:
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y")
        print(now)
        datetime_obj = datetime.datetime.strptime(now, "%d/%m/%Y").strftime("%d %m %Y")
        convert_date_to_day = datetime.datetime.strptime(datetime_obj, '%d %m %Y').strftime('%A')
        if convert_date_to_day == "Saturday" or convert_date_to_day == "Sunday":
            for i in range(1, 10):
                if sheet.get_worksheet(0).cell(i,1).value == None:
                    sheet.get_worksheet(0).update_cell(i, 2, "0")
                    sheet.get_worksheet(0).update_cell(i, 1, now)
                    bot.send_message(OWNER_BOT, "Oggi è sabato o domenica, non è necessario segnare la presenza")
                    break
                else:
                    continue
        else:
            for i in range(1, 10):
                if sheet.get_worksheet(0).cell(i,2).value == None:
                    sheet.get_worksheet(0).update_cell(i, 2, "360")
                    sheet.get_worksheet(0).update_cell(i, 1, now)
                    break
                else:
                    continue

            bot.send_message(OWNER_BOT, "Presenza giornaliera segnata")
    except:
        bot.send_message(OWNER_BOT, "Si è verificato un errore, riprova più tardi")

schedule.every().day.at("07:50").do(presenza_giornaliera)

while True:
    schedule.run_pending()
    bot.polling()