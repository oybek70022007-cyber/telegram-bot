import logging
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ConversationHandler
)
from config import TOKEN
from database import init_db
from handlers.admin import (
    admin_panel, admin_callback,
    add_test_start, add_test_code, add_test_title,
    add_test_expected, add_test_time, add_test_confirm,
    TITLE, CODE, EXPECTED, TIME, CONFIRM
)
from handlers.user import (
    start, show_tests, take_test,
    receive_message, test_callback, leaderboard
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    init_db()
    app = Application.builder().token(TOKEN).build()

    add_test_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_test_start, pattern="^admin_add_test$")],
        states={
            CODE:     [MessageHandler(filters.TEXT & ~filters.COMMAND, add_test_code)],
            TITLE:    [MessageHandler(filters.TEXT & ~filters.COMMAND, add_test_title)],
            EXPECTED: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_test_expected)],
            TIME:     [MessageHandler(filters.TEXT & ~filters.COMMAND, add_test_time)],
            CONFIRM:  [CallbackQueryHandler(add_test_confirm, pattern="^confirm_")],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
        per_message=False,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("tests", show_tests))
    app.add_handler(CommandHandler("top", leaderboard))
    app.add_handler(add_test_conv)
    app.add_handler(CallbackQueryHandler(admin_callback, pattern="^admin_"))
    app.add_handler(CallbackQueryHandler(take_test, pattern="^take_test_"))
    app.add_handler(CallbackQueryHandler(test_callback, pattern="^(check_test|cancel_test|retry_test_|user_leaderboard|my_results|back_start|show_tests_list)"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message))

    logger.info("Bot ishga tushdi! ✅")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
