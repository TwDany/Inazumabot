import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- CONFIGURAZIONE SERVER WEB (Per mantenere attivo il bot gratis su Render) ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Il bot di Inazuma Eleven è attivo e online!"

def run_web():
    # Render assegna una porta automatica tramite la variabile d'ambiente PORT
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

# Avvia il server web in background in modo che Render trovi la porta aperta
threading.Thread(target=run_web).start()


# --- CODICE DEL BOT TELEGRAM ---
TOKEN = "8835515472:AAE8Iys5siGYRj9-titnQJi14auxEWrrA-c"

# Funzione per il comando /start e /comandi
async def mostra_comandi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ecco la lista dei comandi disponibili:\n"
        "/comandi - Mostra questa lista\n"
        "/tiergk - Tier list dei Portieri\n"
        "/tierdf - Tier list dei Difensori\n"
        "/tiermf - Tier list dei Centrocampisti\n"
        "/tierfw - Tier list degli Attaccanti\n"
        "/sito - Link utile per Inazuma Eleven"
    )

# Funzione generica per inviare le immagini delle tier list
async def invia_tierlist(update: Update, context: ContextTypes.DEFAULT_TYPE, nome_file: str, ruolo: str):
    if os.path.exists(nome_file):
        with open(nome_file, 'rb') as foto:
            await update.message.reply_photo(photo=foto, caption=f"Ecco la tier list dei {ruolo}!")
    else:
        await update.message.reply_text(
            f"Attenzione: Non ho trovato il file '{nome_file}' nella cartella del bot."
        )

# Funzioni specifiche per ogni comando tier list
async def tiergk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await invia_tierlist(update, context, "portiere.jpg", "Portieri")

async def tierdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await invia_tierlist(update, context, "difensori.jpg", "Difensori")

async def tiermf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await invia_tierlist(update, context, "centrocampisti.jpg", "Centrocampisti")

async def tierfw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await invia_tierlist(update, context, "attaccanti.jpg", "Attaccanti")

# Funzione per il comando /sito
async def invia_sito(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ecco il link utile per il gioco di Inazuma:\n"
        "https://iecrosshub.github.io/inazuma-eleven-cross-hub/index.html"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Registrazione di tutti i comandi richiesti
    app.add_handler(CommandHandler("start", mostra_comandi))
    app.add_handler(CommandHandler("comandi", mostra_comandi))
    app.add_handler(CommandHandler("tiergk", tiergk))
    app.add_handler(CommandHandler("tierdf", tierdf))
    app.add_handler(CommandHandler("tiermf", tiermf))
    app.add_handler(CommandHandler("tierfw", tierfw))
    app.add_handler(CommandHandler("sito", invia_sito))

    print("Il bot è online e in ascolto...")
    app.run_polling()

if __name__ == '__main__':
    main()
