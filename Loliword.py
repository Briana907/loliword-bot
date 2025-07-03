# ========== FIX para Python 3.13 ==========
import sys
if sys.version_info >= (3, 13):
    import types
    sys.modules['imghdr'] = types.SimpleNamespace(what=lambda *args, **kwargs: 'jpeg')
# ==========================================

from flask import Flask
from threading import Thread

from telegram import Update, InputFile
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler

import os
from datetime import datetime

# === CONFIGURACIÓN ===
TOKEN = '8108375229:AAHPN_ATR_y0EPC9f9pfHMVPLgYFV5gZWzE'
ID_GRUPO = -1002726351464
CARPETA_TEMPORAL = 'tmp_files'
os.makedirs(CARPETA_TEMPORAL, exist_ok=True)

# === COMANDO /start ===
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Puedes enviarme fotos o videos y los reenviaré al grupo como archivo, de forma anónima.")

# === MANEJADOR DE ARCHIVOS ===
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
        print(f"✅ Enviado y eliminado: {nombre_archivo}")

    except Exception as e:
        print(f"❌ Error: {e}")
        update.message.reply_text("❌ Ocurrió un error al enviar tu archivo.")

# === INICIO DEL BOT ===
def iniciar_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo | Filters.video, manejar_archivo))

    print("🤖 Bot activo y esperando archivos...")
    updater.start_polling()
    updater.idle()

# === FLASK PARA RENDER/UPTIME ===
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot corriendo."

def mantener_vivo():
    app.run(host='0.0.0.0', port=8080)

# === MAIN ===
if __name__ == '__main__':
    Thread(target=mantener_vivo).start()
    iniciar_bot()










