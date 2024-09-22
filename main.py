from telegram.ext import Updater
from controllers.bot_controller import setup_dispatcher

def main():
    updater = Updater('YOUR_TELEGRAM_BOT_TOKEN', use_context=True)
    dp = updater.dispatcher

    # Настроить диспетчер с хендлерами команд
    setup_dispatcher(dp)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()