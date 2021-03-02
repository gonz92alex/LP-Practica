# importing Telegram API
import pickle
import sys
import traceback

from respondedor import EnquestaResposta
from respuestas import Respuestas
from telegram import ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


# defining callback function for the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat.id,
                             text="Hello world!")


# defining callback function for the /start command
def author(update, context):
    author_str = '{name}\n{mail}'.format(
        name='Author Name',
        mail='author@example.com'
    )
    context.bot.send_message(chat_id=update.message.chat.id, text=author_str)


def help(update, context):
    help_str = open('help.txt', 'rb').read().decode('UTF8').strip()
    context.bot.send_message(chat_id=update.message.chat.id, text=help_str)


def answer(update, context):
    global enq
    chat_id = update.message.chat.id
    respuesta = int(update.message.text)
    if chat_id in enq:
        encuesta = enq[chat_id]
        item = encuesta.responde(respuesta)
        if item:
            imprime_item(item, chat_id, encuesta.get_id(), context)
        else:
            salida = 'Muchas gracias por contestar'
            context.bot.send_message(chat_id=update.message.chat.id, text=salida)
        global resultados
        enc_id = encuesta.get_id()
        if enc_id in resultados:
            resultado = resultados[enc_id]
            resultado.add_respuesta(encuesta.get_last_respuesta())
            resultados[enc_id] = resultado
        else:
            resultado = Respuestas(enc_id)
            resultado.add_resultados(encuesta)
            resultados[enc_id] = resultado
        pickle.dump(resultados, open('../data/resultados.p', 'wb'))
    else:
        salida = 'No se ha seleccionado enquesta'
        context.bot.send_message(chat_id=update.message.chat.id, text=salida)


def imprime_item(item, chat_id, encuesta, context):
    preg = item.get_pregunta()
    resp = item.get_resposta()
    pregunta = '{id}>{pregunta}\n{respuestas}'.format(
        id=encuesta,
        pregunta=preg.get_pregunta(),
        respuestas=resp.get_respostes_str()
    )
    context.bot.send_message(chat_id=chat_id, text=pregunta)


def quiz(update, context):
    global dades
    global enq
    chat_id = update.message.chat.id
    encuesta = context.args[0]
    text = 'Encuesta: {id}'.format(id=encuesta)
    context.bot.send_message(chat_id=chat_id, text=text)
    enq[chat_id] = EnquestaResposta(dades[encuesta])
    item = enq[chat_id].get_item()
    if item:
        imprime_item(item, chat_id, encuesta, context)
    else:
        context.bot.send_message(chat_id=chat_id, text='Error, pregunta not found')


def report(update, context):
    global enq
    global resultados
    chat_id = update.message.chat.id
    if chat_id in enq:
        encuesta = enq[chat_id]
        enc_id = encuesta.get_id()
        if enc_id in resultados:
            res_encuesta = resultados[enc_id]
            reporte = res_encuesta.report()
            context.bot.send_message(chat_id=update.message.chat.id,
                                     text=reporte,
                                     parse_mode=ParseMode.MARKDOWN)
    else:
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text='No hay encuesta seleccionada')


def bar(update, context):
    try:
        global enq
        global resultados
        chat_id = update.message.chat.id
        pregunta = context.args[0]
        if pregunta:
            if chat_id in enq:
                encuesta = enq[chat_id]
                enc_id = encuesta.get_id()
                if enc_id in resultados:
                    res_encuesta = resultados[enc_id]
                    path = res_encuesta.get_bar(pregunta)
                    context.bot.send_photo(chat_id=update.message.chat.id,
                                           photo=open(path, 'rb'))
                else:
                    context.bot.send_message(chat_id=update.message.chat.id,
                                             text='No hay respuestas de la encuesta')
            else:
                context.bot.send_message(chat_id=update.message.chat.id,
                                         text='No hay encuesta seleccionada')
        else:
            context.bot.send_message(chat_id=update.message.chat.id,
                                     text='No se ha seleccionado una pregunta')
    except Exception:
        traceback.print_exc()


def pie(update, context):
    try:
        global enq
        global resultados
        chat_id = update.message.chat.id
        pregunta = context.args[0]
        if pregunta:
            if chat_id in enq:
                encuesta = enq[chat_id]
                enc_id = encuesta.get_id()
                if enc_id in resultados:
                    res_encuesta = resultados[enc_id]
                    path = res_encuesta.get_pie(pregunta)
                    context.bot.send_photo(chat_id=update.message.chat.id,
                                           photo=open(path, 'rb'))
                else:
                    context.bot.send_message(chat_id=update.message.chat.id,
                                             text='No hay respuestas de la encuesta')
            else:
                context.bot.send_message(chat_id=update.message.chat.id,
                                         text='No hay encuesta seleccionada')
        else:
            context.bot.send_message(chat_id=update.message.chat.id,
                                     text='No se ha seleccionado una pregunta')
    except Exception:
        traceback.print_exc()


enq = {}
# loading the access token from token.txt
TOKEN = open('token.txt').read().strip()
sys.path.append('../cl/')
resultados = pickle.load(open("../data/resultados.p", "rb")) or []
try:
    resultados = pickle.load(open("../data/resultados.p", "rb"))
except (FileExistsError, FileNotFoundError):
    resultados = {}
try:
    dades = pickle.load(open("../data/modelado.p", "rb"))
except (FileExistsError, FileNotFoundError):
    dades = {}
# call main Telegram obcjects
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
# handling callbacks functions to the commands
dispatcher.add_handler(CommandHandler('start', start))
# handling callbacks functions to the commands
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('report', report))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.regex('^[0-9]*$'), answer))
dispatcher.add_handler(CommandHandler('quiz', quiz, pass_args=True))
dispatcher.add_handler(CommandHandler('pie', pie, pass_args=True))
dispatcher.add_handler(CommandHandler('bar', bar, pass_args=True))
# starting the bot
updater.start_polling()
