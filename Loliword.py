from telegram import Update, InputFile
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
import os
from datetime import datetime
import sys

# === FIX para Python 3.13 ===
if sys.version_info >= (3, 13):
    import types
    sys.modules['imghdr'] = types.SimpleNamespace(what=lambda *args, **kwargs: 'jpeg')

# === CONFIGURACIÓN ===
TOKEN = '8108375229:AAHPN_ATR_y0EPC9f9pfHMVPLgYFV5gZWzE'
ID_GRUPO = -1002726351464
CARPETA_TEMPORAL = '/tmp/loliword'

os.makedirs(CARPETA_TEMPORAL, exist_ok=True)

# === /start ===
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Puedes enviarme fotos o videos y los reenviaré al grupo como archivo, de forma anónima.")

# === ARCHIVOS ===
def manejar_archivo(update: Update, context: CallbackContext):
    archivo = update.message.photo[-1] if update.message.photo else update.message.video
    tipo = 'jpg' if update.message.photo else 'mp4'

    if archivo is None:
        update.message.reply_text("❌ No se detectó una imagen o video.")
        return

    nombre_archivo = f"archivo_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.{tipo}"
    ruta_local = os.path.join(CARPETA_TEMPORAL, nombre_archivo)

    archivo.get_file().download(ruta_local)

    try:
        with open(ruta_local, 'rb') as f:
            context.bot.send_document(
                chat_id=ID_GRUPO,
                filename=nombre_archivo,
                document=InputFile(f),
                disable_content_type_detection=True
            )
        os.remove(ruta_local)
        update.message.reply_text("✅ Archivo enviado al grupo correctamente.")
    except Exception as e:
        update.message.reply_text("❌ Error al enviar el archivo.")

# === FLASK PARA RENDER + UPTIME ROBOT ===
from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "✅ Bot activo"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def mantener_vivo():
    hilo = threading.Thread(target=run_flask)
    hilo.start()

# === INICIO ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo | Filters.video, manejar_archivo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    mantener_vivo()
    main()








