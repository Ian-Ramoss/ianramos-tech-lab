from datetime import datetime, timedelta, date
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import pytz
from apscheduler.schedulers.background import BackgroundScheduler

# ================= CONFIGURAÇÕES =================

TOKEN = "---" # Token do bot
CHAT_ID = "---"  # ID do chat onde o alerta será enviado (pode ser um grupo ou chat privado)
TIMEZONE = pytz.timezone("America/Sao_Paulo")

# Data base real (um dia que você sabe que foi Trabalho A)
BASE_DATE = date(2026, 1, 2)  # ajuste se necessário

DIAS_SEMANA_PT = {
    "Mon": "Seg",
    "Tue": "Ter",
    "Wed": "Qua",
    "Thu": "Qui",
    "Fri": "Sex",
    "Sat": "Sáb",
    "Sun": "Dom"
}


# ================= LÓGICA DA ESCALA =================

def get_shift_info(target_date: date):
    delta_days = (target_date - BASE_DATE).days
    cycle_pos = delta_days % 3

    if cycle_pos == 0:
        work = "A"
    elif cycle_pos == 1:
        work = "FOLGA"
    else:  # cycle_pos == 2
        work = "B"

    if work == "A":
        return {
            "tipo": "Trabalho A",
            "turno": "24h",
            "entrada": "09:00",
            "saida": "09:00 do dia seguinte"
        }
    elif work == "B":
        return {
            "tipo": "Trabalho B",
            "turno": "12h",
            "entrada": "08:00",
            "saida": "18:00"
        }
    else:
        return {
            "tipo": "Folga",
            "turno": "-",
            "entrada": "-",
            "saida": "-"
        }

# ================= FORMATADORES =================

def format_shift_message(target_date: date):
    info = get_shift_info(target_date)
    data_str = target_date.strftime("%d/%m/%Y (%A)")
    return (
        f"📅 {data_str}\n"
        f"📌 {info['tipo']} ({info['turno']})\n"
        f"⏰ Entrada: {info['entrada']}\n"
        f"🏁 Saída: {info['saida']}"
    )

# ================= COMANDOS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Sou seu bot de escala.\n\n"
        "Comandos disponíveis:\n"
        "/hoje\n"
        "/amanha\n"
        "/ontem\n"
        "/semana\n"
        "/mes\n"
        "/mes 3 2026  (exemplo: março de 2026)\n"
        "/ano\n"
    )

async def hoje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(TIMEZONE).date()
    await update.message.reply_text(format_shift_message(today))

async def amanha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tomorrow = datetime.now(TIMEZONE).date() + timedelta(days=1)
    await update.message.reply_text(format_shift_message(tomorrow))

async def ontem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    yesterday = datetime.now(TIMEZONE).date() - timedelta(days=1)
    await update.message.reply_text(format_shift_message(yesterday))

async def semana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(TIMEZONE).date()
    msg = "📆 Escala da semana:\n\n"
    
    for i in range(7):
        d = today + timedelta(days=i)
        info = get_shift_info(d)

        dia_en = d.strftime('%a')
        dia_pt = DIAS_SEMANA_PT[dia_en]
        msg += f"{dia_pt} {d.strftime('%d/%m')}→ {info['tipo']}\n"
        
    await update.message.reply_text(msg)

async def mes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    today = datetime.now(TIMEZONE).date()

    if len(args) == 2:
        month = int(args[0])
        year = int(args[1])
    else:
        month = today.month
        year = today.year

    first_day = date(year, month, 1)
    next_month = first_day.replace(day=28) + timedelta(days=4)
    last_day = next_month - timedelta(days=next_month.day)

    msg = f"🗓️ Escala de {first_day.strftime('%B/%Y')}:\n\n"
    d = first_day
    while d <= last_day:
        info = get_shift_info(d)

        dia_en = d.strftime('%a')
        dia_pt = DIAS_SEMANA_PT[dia_en]
        msg += f"{dia_pt} {d.strftime('%d/%m')} → {info['tipo']}\n"
        d += timedelta(days=1)

    await update.message.reply_text(msg)

async def ano(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(TIMEZONE).date()
    year = today.year
    msg = f"📊 Escala do ano {year}:\n\n"

    d = date(year, 1, 1)
    while d.year == year:
        info = get_shift_info(d)

        dia_en = d.strftime('%a')
        dia_pt = DIAS_SEMANA_PT[dia_en]
        msg += f"{dia_pt} {d.strftime('%d/%m')} → {info['tipo']}\n"
        d += timedelta(days=1)

    await update.message.reply_text(msg)

# ================= ALERTA AUTOMÁTICO =================

async def alerta_diario(app):
    today = datetime.now(TIMEZONE).date()
    info_today = format_shift_message(today)
    info_tomorrow = format_shift_message(today + timedelta(days=1))

    message = "🔔 Lembrete diário:\n\n" + info_today + "\n\n➡️ Amanhã:\n" + info_tomorrow
    await app.bot.send_message(chat_id=CHAT_ID, text=message)

# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hoje", hoje))
    app.add_handler(CommandHandler("amanha", amanha))
    app.add_handler(CommandHandler("ontem", ontem))
    app.add_handler(CommandHandler("semana", semana))
    app.add_handler(CommandHandler("mes", mes))
    app.add_handler(CommandHandler("ano", ano))

    scheduler = BackgroundScheduler(timezone=TIMEZONE)
    scheduler.add_job(lambda: app.create_task(alerta_diario(app)), "cron", hour=7, minute=0)
    scheduler.start()

    print("🤖 Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
