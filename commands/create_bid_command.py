from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler


class CreateBidCommand:
    """docstring"""

    def __init__(self):
        """Constructor"""
        self.command_name = "create_bid"
        self.markup = InlineKeyboardMarkup([
    [InlineKeyboardButton(self.command_name, callback_data=self.command_name)]
])

    def create_bid_button_tap(self, update: Update, context: CallbackContext) -> None:
        """
        This handler processes the inline buttons on the menu
        """

        data = update.callback_query.data
        text = ''
        markup = None

        if data == self.command_name:
            text = SECOND_MENU
            markup = SECOND_MENU_MARKUP
        elif data == BACK_BUTTON:
            text = FIRST_MENU
            markup = FIRST_MENU_MARKUP

        # Close the query to end the client-side loading animation
        update.callback_query.answer()

        # Update message content with corresponding menu section
        update.callback_query.message.edit_text(
            text,
            ParseMode.HTML,
            reply_markup=markup
        )

    def create_bid(self, update: Update, context: CallbackContext) -> None:
        """
        This handler processes the inline buttons on the menu
        """

        data = update.callback_query.data
        text = ''
        markup = None

        if data == NEXT_BUTTON:
            text = SECOND_MENU
            markup = SECOND_MENU_MARKUP
        elif data == BACK_BUTTON:
            text = FIRST_MENU
            markup = FIRST_MENU_MARKUP

        # Close the query to end the client-side loading animation
        update.callback_query.answer()

        # Update message content with corresponding menu section
        update.callback_query.message.edit_text(
            text,
            ParseMode.HTML,
            reply_markup=markup
        )
        context.bot.send_message(
            update.message.from_user.id,
            FIRST_MENU,
            parse_mode=ParseMode.HTML,
            reply_markup=FIRST_MENU_MARKUP)




