import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
    filters)
import telegram
import asyncio
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


async def editBetResultStart(update: Update, context: CallbackContext) -> int:

    user = update.message.from_user
    logging.info('User entered editBetResult function')
    await update.message.reply_text(text = getUserOpenedBetsListText(id = user.id))
    return 41

async def choseBetResultToEdit(update: Update, context: CallbackContext) -> int:

    user = update.message.from_user
    betUID = update.message.text
    logging.info('User inside chooseBetResultToEdit function')
    context.user_data['betUID'] = int(betUID)
    await update.message.reply_text(text = getEditBetResultTextIfBetExists(id = user['id'], betUID = betUID),
                                    reply_markup=getYesNoInlineKeyboard(Y_callback='editBetWin', N_callback='editBetLoss'))
    return 42

async def editBetWin(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    changeBetResult(id = query['message']['chat']['id'], betId = int(context.user_data['betUID']), result='Win')
    calculateUserBalance(id = query['message']['chat']['id'])
    updateUserBalance(id = query['message']['chat']['id'])
    await query.answer()
    await query.edit_message_text(text=getBetResultUpdatedText(),
                                  reply_markup=None)
    return ConversationHandler.END

async def editBetLoss(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    changeBetResult(id = query['message']['chat']['id'], betId = int(context.user_data['betUID']), result='Loss')
    calculateUserBalance(id = query['message']['chat']['id'])
    updateUserBalance(id = query['message']['chat']['id'])
    await query.answer()
    await query.edit_message_text(text=getBetResultUpdatedText(),
                                  reply_markup=None)
    return ConversationHandler.END

async def getUserBetsHistoryExcell(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user

    generateUserBetsHistoryXSL(id = user['id'])
    excel_file_path = getUserDataCSVPath(id = user['id'])
    excel_file = open(excel_file_path, 'rb')
    await context.bot.send_document(update.effective_chat.id, excel_file)
    return 51

async def getUserBalanceHistorExcell(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    updateUserBalance(id=update.message.from_user['id'])
    generateUserBalanceHistoryXSL(id = user['id'])
    excel_file_path = getUserBalancePath(id = user['id'])
    excel_file = open(excel_file_path, 'rb')
    await  context.bot.send_document(update.effective_chat.id, excel_file)
    return 52



async def helpFunction(update: Update, context: CallbackContext) -> int:

    await update.message.reply_text(text = getHelpText())
    return 61


async def promtSport(update: Update, context: CallbackContext) -> int:
    cor = context.bot.send_message(text = getPromtSportText(), chat_id = update.effective_chat.id)
    message = await cor
    context.user_data['previous_message_id'] = message['message_id']

    return 91

async def promtGame(update: Update, context: CallbackContext) -> int:
    sport = update.message.text
    context.user_data['bet_sport'] = sport
    cor = context.bot.edit_message_text(chat_id = update.effective_chat.id,
                                        message_id = context.user_data['previous_message_id'],
                                        text = getPromptGameText(sport = sport))
    message = await cor
    context.user_data['previous_message_id'] = message['message_id']
    await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=update.message.id)

    return 92

async def promtLeague(update: Update, context: CallbackContext) -> int:
    game = update.message.text
    context.user_data['bet_game'] = game

    cor = context.bot.edit_message_text(chat_id = update.effective_chat.id,
                                        message_id = context.user_data['previous_message_id'],
                                        text = getPromptLeagueText(sport = context.user_data['bet_sport'],
                                                                 game = game))
    message = await cor
    context.user_data['previous_message_id'] = message['message_id']
    await context.bot.deleteMessage(chat_id = update.effective_chat.id, message_id = update.message.id)

    return 93

async def promtBet(update: Update, context: CallbackContext) -> int:
    league = update.message.text
    context.user_data['bet_league'] = league

    cor = context.bot.edit_message_text(chat_id = update.effective_chat.id,
                                        message_id = context.user_data['previous_message_id'],
                                        text = getPromptBetText(sport = context.user_data['bet_sport'],
                                                                 game = context.user_data['bet_game'],
                                                                 league = league))
    message = await cor
    context.user_data['previous_message_id'] = message['message_id']
    await context.bot.deleteMessage(chat_id = update.effective_chat.id, message_id = update.message.id)

    return 94

async def promtCoff(update: Update, context: CallbackContext) -> int:

    bet = update.message.text
    context.user_data['bet_bet'] = bet
    cor = context.bot.edit_message_text(chat_id = update.effective_chat.id,
                                        message_id = context.user_data['previous_message_id'],
                                        text = getPromtCoffText(sport = context.user_data['bet_sport'],
                                                                game = context.user_data['bet_game'],
                                                                league = context.user_data['bet_league'],
                                                                bet = bet))
    message = await cor
    context.user_data['previous_message_id'] = message['message_id']
    await context.bot.deleteMessage(chat_id = update.effective_chat.id, message_id = update.message.id)

    return 95

async def promtAmount(update: Update, context: CallbackContext) -> int:

    try:
        coff = float(update.message.text)

        context.user_data['bet_coff'] = coff
        cor = context.bot.edit_message_text(chat_id = update.effective_chat.id,
                                            message_id = context.user_data['previous_message_id'],
                                            text = getPromtAmontText(sport = context.user_data['bet_sport'],
                                                                    game = context.user_data['bet_game'],
                                                                    bet = context.user_data['bet_bet'],
                                                                    league=context.user_data['bet_league'],
                                                                    coff = coff))
        message = await cor
        context.user_data['previous_message_id'] = message['message_id']
        await context.bot.deleteMessage(chat_id = update.effective_chat.id, message_id = update.message.id)

        return 96
    except ValueError:
        return 951

async def promptPercentOwn(update: Update, context: CallbackContext) -> int:

    try:
        amount = int(update.message.text)
        context.user_data['bet_amount'] = amount
        cor = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                        message_id=context.user_data['previous_message_id'],
                                        text=getPromtPercentText(sport=context.user_data['bet_sport'],
                                                               game=context.user_data['bet_game'],
                                                               bet=context.user_data['bet_bet'],
                                                               league=context.user_data['bet_league'],
                                                               coff=context.user_data['bet_coff'],
                                                               amount = amount))
        message = await cor
        context.user_data['previous_message_id'] = message['message_id']
        await context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.id)
        return 97
    except ValueError:
        return 961

async def promptDatePlaced(update: Update, context: CallbackContext) -> int:

    try:
        percent = float(update.message.text)
        context.user_data['bet_percent'] = percent
        cor = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                        message_id=context.user_data['previous_message_id'],
                                        text=getPromtDatePlacedText(sport=context.user_data['bet_sport'],
                                                               game=context.user_data['bet_game'],
                                                               bet=context.user_data['bet_bet'],
                                                               league=context.user_data['bet_league'],
                                                               coff=context.user_data['bet_coff'],
                                                               amount = context.user_data['bet_amount'],
                                                               percentOwn=percent))
        message = await cor
        context.user_data['previous_message_id'] = message['message_id']
        await context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.id)
        return 98
    except ValueError:
        return 971

async def promptDateGame(update: Update, context: CallbackContext) -> int:
    datePlaced = update.message.text
    context.user_data['bet_date_placed'] = datePlaced
    cor = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                    message_id=context.user_data['previous_message_id'],
                                    text=getPromtDateGameText(sport=context.user_data['bet_sport'],
                                                           game=context.user_data['bet_game'],
                                                           bet=context.user_data['bet_bet'],
                                                           league=context.user_data['bet_league'],
                                                           coff=context.user_data['bet_coff'],
                                                           amount = context.user_data['bet_amount'],
                                                           percentOwn=context.user_data['bet_percent'],
                                                           datePlaced = datePlaced))
    message = await cor
    context.user_data['previous_message_id'] = message['message_id']
    await context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.id)
    return 99

async def confrirmFinalBet(update: Update, context: CallbackContext) -> int:


    dateOGame = update.message.text
    context.user_data['bet_date_o_game'] = dateOGame
    cor = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                    message_id=context.user_data['previous_message_id'],
                                    text=getPromtBetConformation(sport=context.user_data['bet_sport'],
                                                           game=context.user_data['bet_game'],
                                                           bet=context.user_data['bet_bet'],
                                                           league=context.user_data['bet_league'],
                                                           coff=context.user_data['bet_coff'],
                                                           amount = context.user_data['bet_amount'],
                                                           percentOwn=context.user_data['bet_percent'],
                                                           datePlaced = context.user_data['bet_date_placed'],
                                                           dateOGame = dateOGame),
                                    reply_markup=getYesNoInlineKeyboard(Y_callback='confirmBet', N_callback='rejectBet'))
    message = await cor
    context.user_data['previous_message_id'] = message['message_id']
    await context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.id)
    return 100

async def confirmAndPlaceBet(update: Update, context: CallbackContext):
    query = update.callback_query

    bet_list = [context.user_data['bet_sport'],
                context.user_data['bet_league'],
           context.user_data['bet_game'],
           context.user_data['bet_bet'],
           context.user_data['bet_coff'],
           context.user_data['bet_amount'],
           context.user_data['bet_percent'],
           context.user_data['bet_date_placed'],
           context.user_data['bet_date_o_game']]

    placeBet(id = query['message']['chat']['id'],bet_list = bet_list)
    await query.answer('Ставка принята')
    await query.edit_message_text(text=getBetPlacedMessageText(sport=context.user_data['bet_sport'],
                                                           game=context.user_data['bet_game'],
                                                           bet=context.user_data['bet_bet'],
                                                           league=context.user_data['bet_league'],
                                                           coff=context.user_data['bet_coff'],
                                                           amount = context.user_data['bet_amount'],
                                                           percentOwn=context.user_data['bet_percent'],
                                                           datePlaced = context.user_data['bet_date_placed'],
                                                           dateOGame = context.user_data['bet_date_o_game']),
                                 reply_markup=None)
    return ConversationHandler.END

async def rejectBet(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=str('Start from beginning'),
                                  reply_markup=None)
    return ConversationHandler.END

def getPlaceBetSeparatelyHandler():
    handler = ConversationHandler(
        entry_points = [CommandHandler('place_bet', promtSport)],
        states = {
            91: [CommandHandler('cancel', cancel),
                MessageHandler(filters.TEXT , promtGame)
                 ],
            92: [CommandHandler('cancel', cancel),
                MessageHandler(filters.TEXT, promtLeague)
                 ],
            93: [CommandHandler('cancel', cancel),
                MessageHandler(filters.TEXT, promtBet),
                 ],
            94: [CommandHandler('cancel', cancel),
                MessageHandler(filters.TEXT, promtCoff),
                 ],
            95: [CommandHandler('cancel', cancel),
                MessageHandler(filters.TEXT, promtAmount),
                 ],
            96: [CommandHandler('cancel', cancel),
                MessageHandler(filters.TEXT, promptPercentOwn),
                 ],
            97: [CommandHandler('cancel', cancel),
                MessageHandler(filters.TEXT, promptDatePlaced),
                 ],
            98: [CommandHandler('cancel', cancel),
                MessageHandler(filters.TEXT,  promptDateGame),
                 ],
            99: [CommandHandler('cancel', cancel),
                MessageHandler(filters.TEXT, confrirmFinalBet),
                 ],
            100: [CallbackQueryHandler(confirmAndPlaceBet, pattern = 'confirmBet'),
                 CallbackQueryHandler(rejectBet, pattern = 'rejectBet')]
        },
        fallbacks = [CommandHandler('cancel', cancel)],
        per_user = True
    )

    return handler

def getEditBetResultHandler():
    bet_result_handler = ConversationHandler(
        entry_points = [CommandHandler('edit_result', editBetResultStart)],
        states = {
        41: [MessageHandler(filters.Regex('^([\s\d]+)$'), choseBetResultToEdit)],
        42: [CallbackQueryHandler(editBetWin, pattern = 'editBetWin'),
             CallbackQueryHandler(editBetLoss, pattern = 'editBetLoss')]
        },
        fallbacks = [CommandHandler('cancel', cancel)],
        per_user = True
    )
    return bet_result_handler

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
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True
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
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True
    )
    return conv_handler_place_bet

async def generateReportForTodayUser(update: Update, context: CallbackContext):
    report = generateReportTodayOneUser(user_id=update.message.from_user.id)
    await update.message.reply_text(text=report)

#-------------------ADMIN FUNCTIONS---------------------
async def getUsersData(update: Update, context: CallbackContext):

    user_id= update.message.from_user['id']
    if user_id == ADMIN_ID:
        users_table = open(USERS_DATABASE_PATH, 'rb')
        await context.bot.send_document(update.effective_chat.id, users_table)
        return ConversationHandler.END
    else:
        return ConversationHandler.END

async def getUsersBets(update: Update, context: CallbackContext):
    user_id = update.message.from_user['id']
    if user_id == ADMIN_ID:
        await update.message.reply_text('ID:')
        return 71
    else:
        return ConversationHandler.END

async def sendUserBets(update: Update, context: CallbackContext):
    user_id = update.message.text
    try:
        bets_file = getUserDataCSVPath(id = user_id)
        bets_file = open(bets_file, 'rb')
        await context.bot.send_document(update.effective_chat.id, bets_file)
    except FileNotFoundError:
        await update.message.reply_text('Eblan')

    return ConversationHandler.END

async def getUsersBalance(update: Update, context: CallbackContext):
    user_id = update.message.from_user['id']
    if user_id == ADMIN_ID:
        await update.message.reply_text('ID:')
        return 71
    else:
        return ConversationHandler.END

async def sendUserBalance(update: Update, context: CallbackContext):
    user_id = update.message.text
    try:
        bets_file = getUserBalancePath(id = user_id)
        bets_file = open(bets_file, 'rb')
        await context.bot.send_document(update.effective_chat.id, bets_file)
    except FileNotFoundError:
        await update.message.reply_text('Eblan')

    return ConversationHandler.END

async def getAdminHelp(update: Update, context: CallbackContext):
    user_id = update.message.from_user['id']
    if user_id == ADMIN_ID:
        await update.message.reply_text(getAdminHelpCommandText())
        return ConversationHandler.END
    else:
        return ConversationHandler.END

async def updateUserBetsAdmin(update: Update, context: CallbackContext):
    user_id = update.message.from_user['id']
    if user_id == ADMIN_ID:
        await update.message.reply_text('ID:')
        return 81
    else:
        return ConversationHandler.END

async def promtAdminBetsFile(update: Update, context: CallbackContext):
    try:
        user_id = int(update.message.text)
    except ValueError:
        await update.message.reply_text('Eblan')
    if checkIfRegistredID(user_id):
        await update.message.reply_text('Send File:')
        context.user_data['user_bets_id'] = user_id
        return 82
    else:
        await update.message.reply_text('Eblan')
        return ConversationHandler.END

async def updateUserBetsFileAdmin(update: Update, context: CallbackContext):

    cor = context.bot.get_file(update.message.document.file_id)
    path = getUserDataCSVPath(id = context.user_data['user_bets_id'])
    file = await cor
    await file.download(path)

    await update.message.reply_text('bets file updated')
    return ConversationHandler.END

async def generateReportForTodayAdmin(update: Update, context: CallbackContext):
    uid = update.message.from_user.id
    if uid == ADMIN_ID:
        report = generateAllUserReportToday()
        await update.message.reply_text(text=report)
    else:
        return ConversationHandler.END

def getUserBetsDataAdminHandler():
    handler = ConversationHandler(
        entry_points = [CommandHandler('get_user_bets', getUsersBets)],
        states = {
            71: [MessageHandler(filters.TEXT, sendUserBets)],

        },
        fallbacks = [CommandHandler('cancel', cancel)],
        per_user = True
    )
    return handler

def getUserBalanceDataAdminHandler():
    handler = ConversationHandler(
        entry_points = [CommandHandler('get_user_balance', getUsersBalance)],
        states = {
            71: [MessageHandler(filters.TEXT, sendUserBalance)],

        },
        fallbacks = [CommandHandler('cancel', cancel)],
        per_user = True
    )
    return handler

def getUpdateUserBetsFileAdminHandler():
    handler = ConversationHandler(
        entry_points = [CommandHandler('update_user_bets', updateUserBetsAdmin)],
        states = {
            81: [MessageHandler(filters.TEXT, promtAdminBetsFile)],
            82: [MessageHandler(filters.ATTACHMENT, updateUserBetsFileAdmin)]

        },
        fallbacks = [CommandHandler('cancel', cancel)],
        per_user = True
    )
    return handler



def runBot():
    application = ApplicationBuilder().token(TOKEN).build()
    conv_handler_register = getStartHandler()
    #conv_handler_place_bet = getPlaceBetHandler()
    bet_result_handler = getEditBetResultHandler()
    place_bet_s_handler = getPlaceBetSeparatelyHandler()
    admin_bets_handler = getUserBetsDataAdminHandler()
    admin_balance_handler = getUserBalanceDataAdminHandler()
    admin_edit_bets_handler = getUpdateUserBetsFileAdminHandler()

    application.add_handler(conv_handler_register)
    #application.add_handler(conv_handler_place_bet)
    application.add_handler(bet_result_handler)
    application.add_handler(admin_bets_handler)
    application.add_handler(admin_balance_handler)
    application.add_handler(admin_edit_bets_handler)
    application.add_handler(place_bet_s_handler)

    application.add_handler(CommandHandler('cancel', cancel))
    application.add_handler(CommandHandler('get_balance_history', getUserBalanceHistorExcell))
    application.add_handler(CommandHandler('get_bets_history', getUserBetsHistoryExcell))
    application.add_handler(CommandHandler('help', helpFunction))
    application.add_handler(CommandHandler('get_users', getUsersData))
    application.add_handler(CommandHandler('helpa', getAdminHelp))
    application.add_handler(CommandHandler('generate_report', generateReportForTodayUser))
    application.add_handler(CommandHandler('generate_report_a', generateReportForTodayAdmin))




    application.run_polling()