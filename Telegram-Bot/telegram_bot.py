TOKEN = '5230743453:AAGtLRSax96d_EV1F7uXQBLPirxaP6KSi84'
BUCKET = '"IoT-sensor"'
MAX_GAS = 1000
MAX_TEMP = 30#°C

HOUR_REPORT = 10
MINUTE_REPORT = 00

BOOL_TEMPERATURE = False
BOOL_GAS = False

from telegram.ext import Updater, CommandHandler
import logging, datetime, pytz
from influx_query import *

#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def start(update, context):
    print('\start')
    update.message.reply_text('Welcome to the IoT-Alert-Bot')
    context.job_queue.run_repeating(alert_temperature, 5, context=update.message.chat_id)
    context.job_queue.run_repeating(alert_gas, 5, context=update.message.chat_id)
    context.job_queue.run_daily(daily_report,
                                datetime.time(hour=HOUR_REPORT, minute=MINUTE_REPORT, tzinfo=pytz.timezone('Europe/Rome')),
                                context=update.message.chat_id)

def daily_report(context):
    print('\\report')
    x = fun_report(BUCKET)
    context.bot.send_message(chat_id=context.job.context, text='DAILY REPORT\n\
    Aqi: {aqi} \n\
    Gas: {gas} \n\
    Humidity: {humidity} \n\
    Rssi: {rssi} \n\
    Temperature: {temperature}'.format(aqi=round(x[0], 2), gas=round(x[1], 2), humidity=round(x[2], 2), rssi=round(x[3], 2), temperature=round(x[4], 2)))

def report(update, context):
    print('\\report')
    x = fun_report(BUCKET)
    context.bot.send_message(chat_id=update.effective_chat.id, text='REPORT\n\
    Aqi: {aqi} \n\
    Gas: {gas} \n\
    Humidity: {humidity} \n\
    Rssi: {rssi} \n\
    Temperature: {temperature}'.format(aqi=round(x[0], 2), gas=round(x[1], 2), humidity=round(x[2], 2), rssi=round(x[3], 2), temperature=round(x[4], 2)))

def aqi(update, context):
    print('\\aqi')
    x = str(fun_sensor_filter(BUCKET,'"aqi"'))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Aqi: ' + x)

def gas(update, context):
    print('\\gas')
    x = str(fun_sensor_filter(BUCKET,'"gas"'))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Gas: ' + x)
    
def humidity(update, context):
    print('\\humidity')
    x = str(fun_sensor_filter(BUCKET,'"humidity"'))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Humidity: ' + x)
    
def rssi(update, context):
    print('\\rssi')
    x = str(fun_sensor_filter(BUCKET,'"rssi"'))
    context.bot.send_message(chat_id=update.effective_chat.id, text='RSSI: ' + x)
    
def temperature(update, context):
    print('\\temperature')
    x = str(fun_sensor_filter(BUCKET,'"temperature"'))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Temperature: ' + x + '°C')

def alert_temperature(context):
    global BOOL_TEMPERATURE
    x = fun_sensor_filter(BUCKET,'"temperature"')
    if(x >= MAX_TEMP and BOOL_TEMPERATURE == False):
        BOOL_TEMPERATURE = True
        print('\\alert_temperature_firing')
        context.bot.send_message(chat_id=context.job.context, text='ALERT FIRING\nTemperature: ' + str(round(x, 2)) + '°C')
    elif(x < MAX_TEMP and BOOL_TEMPERATURE == True):
        print('\\alert_temperature_ok')
        context.bot.send_message(chat_id=context.job.context, text='ALERT OK\nTemperature: ' + str(round(x, 2)) + '°C')
        BOOL_TEMPERATURE = False

def alert_gas(context):
    global BOOL_GAS
    x = fun_sensor_filter(BUCKET,'"gas"')
    if(x >= MAX_GAS and BOOL_GAS == False):
        print('\\alert_gas_firing')
        context.bot.send_message(chat_id=context.job.context, text='ALERT FIRING\nGas: ' + str(x))
        BOOL_GAS = True
    elif(x < MAX_GAS and BOOL_GAS == True):
        print('\\alert_gas_ok')
        context.bot.send_message(chat_id=context.job.context, text='ALERT OK\nGas: ' + str(x))
        BOOL_GAS = False



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater( TOKEN , use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start, pass_job_queue=True))
    updater.dispatcher.add_handler(CommandHandler('report', report))
    updater.dispatcher.add_handler(CommandHandler('aqi', aqi))
    updater.dispatcher.add_handler(CommandHandler('gas', gas))
    updater.dispatcher.add_handler(CommandHandler('humidity', humidity))
    updater.dispatcher.add_handler(CommandHandler('rssi', rssi))
    updater.dispatcher.add_handler(CommandHandler('temperature', temperature))

    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()