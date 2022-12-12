import logging
import datetime
import re
from helpers.Counter import Counter

from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, chat
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

logger = logging.getLogger(__name__)

# Чат группы исполнителей todo: вынести в конфиг, определять по имени чата
group_chat_id = -836374366

# Store bot screaming status
screaming = False

# Pre-assign menu text
FIRST_MENU = "<b>Menu 1</b>\n\nA beautiful menu with a shiny inline button."
SECOND_MENU = "<b>Menu 2</b>\n\nA better menu with even more shiny inline buttons."

# Pre-assign button text
NEXT_BUTTON = "Next"
BACK_BUTTON = "Back"
TUTORIAL_BUTTON = "Tutorial"

# номер заявки
BID_COUNTER = Counter()

# заявки пользователей
BID_USER_IDS = {}

# Build keyboards
FIRST_MENU_MARKUP = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(NEXT_BUTTON, callback_data=NEXT_BUTTON)
    ],
    [
        InlineKeyboardButton(NEXT_BUTTON, callback_data=NEXT_BUTTON)
    ]
])
SECOND_MENU_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton(BACK_BUTTON, callback_data=BACK_BUTTON)],
    [InlineKeyboardButton(TUTORIAL_BUTTON, url="https://core.telegram.org/bots/api")]
])


def create_bid_message(number, text, customer_info):
    bid = f'<b>Заявка #{number}</b>\n\n{text}\n\n{customer_info}'
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Взять заявку", callback_data='takebid'),
            InlineKeyboardButton("Отказаться", callback_data='cancelbid')
        ]
    ])
    bid_msg = {'text': bid, 'parse_mode': ParseMode.HTML, 'reply_markup': markup}
    return bid_msg


def get_gurrent_bid_number():
    today = datetime.datetime.today().strftime("%d%m%Y")
    return f'{today}_{BID_COUNTER.get_current_count()}'


def echo(update: Update, context: CallbackContext) -> None:
    """
    This function would be added to the dispatcher as a handler for messages coming from the Bot API
    """

    # Print to console
    logger.info(f'{update.message.from_user.first_name} wrote {update.message.text}')

    if update.message.chat.type != 'group':
        chat_id = group_chat_id
    else:
        chat_id = update.message.from_user.id
    bid_number = get_gurrent_bid_number()
    BID_USER_IDS[bid_number] = update.message.from_user.id
    bid_message = create_bid_message(bid_number, update.message.text, update.message.from_user.first_name)
    context.bot.send_message(
        chat_id,
        bid_message["text"],
        parse_mode=bid_message["parse_mode"],
        reply_markup=bid_message["reply_markup"]
    )
    context.bot.send_message(
        update.message.from_user.id,
        f'Сформирована заявка:\n\n {bid_message["text"]}',
        parse_mode=ParseMode.HTML
    )


def menu(update: Update, context: CallbackContext) -> None:
    """
    This handler sends a menu with the inline buttons we pre-assigned above
    """
    if update.message.chat.type == 'group':
        chat_id = update.message.chat.id
    else:
        chat_id = update.message.from_user.id
    context.bot.answer_web_app_query()

    context.bot.send_message(
        chat_id,
        FIRST_MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=FIRST_MENU_MARKUP
    )


def button_tap(update: Update, context: CallbackContext) -> None:
    """
    This handler processes the inline buttons on the menu
    todo:
    1. убрать кнопку принять заявку
    2. в сообщении отметить исполнителя
    3. удалять сообщения, для которых нельзя найти заказчика
    """
    data = update.callback_query.data
    text = update.callback_query.message.text
    bid_from_message = re.search(r'\d{8}_\d*', text)

    if not bid_from_message:
        update.callback_query.answer()
        return

    chat_id = BID_USER_IDS.get(bid_from_message[0])

    if not chat_id:
        update.callback_query.answer(
            text="Не удалось найти отправителя заявки",
            show_alert=True
        )
        return

    context.bot.send_message(
        chat_id,
        f'Ваша заявка #{bid_from_message[0]} взята в работу.',
        parse_mode=ParseMode.HTML
    )
    # Close the query to end the client-side loading animation
    update.callback_query.answer()

    # Update message content with corresponding menu section
    update.callback_query.message.edit_text(
        f'{text}\n\n Взял в работу: {update.callback_query.from_user.name}',
        ParseMode.HTML
    )


def main() -> None:
    # todo: вынести получение токена из параметров среды
    updater = Updater("5830450915:AAGagkxi8W5r0Myj4p0tgznb6lNSw4Akn4M")

    # Get the dispatcher to register handlers
    # Then, we register each handler and the conditions the update must meet to trigger it
    dispatcher = updater.dispatcher
    command_list = dict(
        menu=menu
    )
    for command in command_list:
        dispatcher.add_handler(CommandHandler(command, command_list[command]))

    # Register handler for inline buttons
    dispatcher.add_handler(CallbackQueryHandler(button_tap))

    # Echo any message that is not a command
    dispatcher.add_handler(MessageHandler(~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
