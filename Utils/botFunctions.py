import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
    filters)


from Utils.messagesTexts import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def getYesNoInlineKeyboard(Y_callback, N_callback):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Да", callback_data=Y_callback),
            InlineKeyboardButton("Нет", callback_data=N_callback),
        ]
    ])
    return keyboard

#start conversation handler:
#-------------------------start command----------------------------
async def start(update: Update, context: CallbackContext) -> int:
    logging.info('User inside start function')
    id = update.message.from_user['id']

    if checkIfRegistredID(id=id):

        await update.message.reply_text(getStartIfRegisterText(id=id))
        return ConversationHandler.END
    else:

        keyboard = getYesNoInlineKeyboard(Y_callback='register', N_callback='ignoreRegistration')

        await update.message.reply_text(text=getStartIfNotRegisterText(), reply_markup=keyboard)
        return 1

#-------------------------registration start 2 stage----------------------------
async def promptNameForRegistration(update: Update, context: CallbackContext) -> int:
    logging.info('User inside startRegistration function')
    query = update.callback_query

    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    await query.edit_message_text(getRegistrationNamePromptText())
    return 2

async def registrationReject(update: Update, context: CallbackContext):
    logging.info('User rejected registration ends conversation')
    query = update.callback_query

    await query.answer()
    await query.edit_message_reply_markup(reply_markup = None)
    await query.edit_message_text(text = getRefusedRegistrationText())

    return ConversationHandler.END

#-------------------------registration start 3 stage----------------------------
async def nameConformation(update:Update, context: CallbackContext) -> int:
    logging.info('User entered name and now inside name_conformation function')
    name = update.message.text
    context.user_data['name'] = name
    if checkIfRegistredName(name):
        logging.info('User entered invalid name ')
        await update.message.reply_text(text = getNameRegistredText())

        return ConversationHandler.END
    else:
        logging.info('User entered registred name ')
        keyboard = getYesNoInlineKeyboard(Y_callback = 'confirmName', N_callback='rejectName')

        await update.message.reply_text(text = getNameApprovalText(name = name),
                                        reply_markup=keyboard)
        return 22

#-------------------------registration start 4 stage----------------------------
async def register(update: Update, context: CallbackContext) -> int:
    logging.info('User registred')
    query = update.callback_query
    id = query['message']['chat']['id']
    uname = query['message']['chat']['username']
    name = context.user_data['name']

    registerUser(id = id, uname = uname, name = name)
    await query.answer()
    await query.edit_message_text(text = getRegistrationConformationText(name = name,
                                                                         uname = uname,
                                                                         ),
                                  reply_markup = None)
    return ConversationHandler.END

#place_bet conversation handler:
#-------------------------place_bet begin----------------------------
async def place_bet(update: Update, context: CallbackContext) -> int:
    logging.info('User is in place bet function')

    await update.message.reply_text(text = getPromtBetPlaceText())
    return 31

#-------------------------promt bet approval begin----------------------------
async def promtBetApproval(update:Update, context: CallbackContext) -> int:
    bet_list = parseBet(update.message.text)
    text = getBetApprovalText(bet_list)
    bet = parseBet(update.message.text)
    keyboard = getYesNoInlineKeyboard(Y_callback='confirmBet', N_callback='rejectBet')
    context.user_data['bet'] = bet
    await update.message.reply_text(text = text, reply_markup=keyboard)
    return 32

#-------------------------bet approved / rejected----------------------------
async def confirmBet(update: Update, context: CallbackContext):
    query = update.callback_query
    id = query['message']['chat']['id']
    bet_list = context.user_data['bet']
    placeBet(id = id, bet_list = bet_list)
    await query.answer()
    await query.edit_message_text(text = getBetConformationText(bet_list = bet_list), reply_markup= None)
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""

    user = update.message.from_user
    logging.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(text = 'Разговор окончен', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def getStartHandler():
    conv_handler_register = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            1: [CallbackQueryHandler(promptNameForRegistration, pattern = 'register'),
                CallbackQueryHandler(registrationReject, pattern = 'ignoreRegistration')],
            2: [MessageHandler(filters.TEXT,callback = nameConformation)],
            22: [CallbackQueryHandler(register, pattern='confirmName'),
                 CallbackQueryHandler(promptNameForRegistration, pattern = 'rejectName')]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return conv_handler_register

def getPlaceBetHandler():
    conv_handler_place_bet = ConversationHandler(
        entry_points=[CommandHandler('place_bet', place_bet)],
        states={
            31: [MessageHandler(filters.Regex(getRegex()), promtBetApproval),
                 MessageHandler(filters.Regex('^[A-z].*$'), place_bet)],
            32: [CallbackQueryHandler(confirmBet, pattern='confirmBet'),
                 CallbackQueryHandler(place_bet, pattern='rejectBet')
                 ]

        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return conv_handler_place_bet


def runBot():
    application = ApplicationBuilder().token(TOKEN).build()
    conv_handler_register = getStartHandler()
    conv_handler_place_bet = getPlaceBetHandler()
    application.add_handler(conv_handler_register)
    application.add_handler(conv_handler_place_bet)

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('cancel', cancel))
    application.run_polling()