from Utils.utils import *



START_MESSAGE_IF_NOT_REGISTRED = 'Привет ты не зарегестрирован поэтому не можешь ставить ставки здесь, Зарегестрироваться? '
START_MESSAGE_IF_REGISTRED = 'Привет ты зарегестрирован, постваить ставку: /place_bet'
REGISTER_1_IF_REGISTRED = 'Вы зарегестрированы'
REGISTER_1_IF_NOT_REGISTRED = 'Введи свое имя:'
REGISTER_2_NAME_EXISTS = 'Имя занято выбери более уникальное'
REGISTER_2_NAME_NOT_EXISTS ='Вы выбрали имя: '



def getStartIfRegisterText(id):
    new_line = '\n'
    text = f'Привет {getNamebyID(id)} ты уже зарегестрирован {new_line}' \
           f'Поставить ставку: /place_bet'
    return text

def getStartIfNotRegisterText():
    new_line = '\n'
    text = f'Привет ты не зарегестрирован поэтому не можешь ставить ставки {new_line}' \
           f'Зарегестрироваться? '

    return text

def getRegistrationNamePromptText():
    text = f'Введи свое имя:'
    return text

def getRefusedRegistrationText():
    new_line = '\n'
    text = f'Вы не сможете использовать бота без регистрации{new_line}Для регистрации /start'
    return text

def getNameRegistredText():
    text = f'Выбери другое имя, это занято используй /start заново'
    return text

def getNameApprovalText(name):
    new_line = '\n'
    text = f'Выбрано имя: {name}{new_line}Подтвердить?'
    return text

def getRegistrationConformationText(name, uname):
    new_line = '\n'
    text = f'{name} ты зарегестрирован.{new_line}Твой TGuname: {uname}.{new_line}' \
           f'/help для функционала.'
    return text

def getPromtBetPlaceText():
    new_line = '\n'
    text = f'Отправь ставку в формате:{new_line}' \
                 f'(спорт)(лига)(матч)(ставка)(коф)(сумма)(процент себе)(дата ставки)(дата события).{new_line}' \
                 f'Пример:{new_line}' \
                 f'(Football)(Intalia series A)(Juve - Lazio)(П1)(1.83)(1500)(10)(22-10-2022)(29-10-2022)'
    return text

def getBetApprovalText(bet_list):
    new_line = '\n'
    text = f'Спорт:                 {bet_list[0]}{new_line}' \
           f'Турнир:               {bet_list[1]}{new_line}' \
           f'Матч:                  {bet_list[2]}{new_line}' \
           f'Ставка:               {bet_list[3]}{new_line}' \
           f'Коф:                   {bet_list[4]}{new_line}' \
           f'Сумма:               {bet_list[5]}{new_line}' \
           f'Твой %:              {bet_list[6]}{new_line}' \
           f'Поcтсвлено:      {bet_list[7]}{new_line}' \
           f'Играеться:         {bet_list[8]}{new_line}' \
           f'Подтвердить?'
    return text

def getBetConformationText(bet_list):
    new_line = '\n'
    text = f'Ставка {new_line}{bet_list[2]} {bet_list[3]} за {bet_list[4]}{new_line}Принята.'
    return text

def getUserOpenedBetsListText(id):
    bet_list = getUserOpenedBetsList(id, params = ['BetUID','DatePlaced', 'Game', 'Bet', 'Coff', 'Amount'])
    if bet_list:
        new_line = '\n'
        text = f'Для того что бы выбрать ставку которую хочешь обновить ответь номером' \
               f'id ставки на это сообщение(BetID).{new_line} Пример ответа: 1{new_line}' \
               f'Открытые ставки:{new_line}'

        for i, data in enumerate(bet_list):
            text+=f'ID: {data[0]}{new_line}Дата ставки: {data[1]}{new_line}Игра:    {data[2]}{new_line}Исход:   {data[3]}{new_line}' \
                  f'Коф:    {data[4]}{new_line}Ставка:  {data[5]}{new_line}{new_line}'

        return text

    else:
        return False


def getEditBetResultTextIfBetNotExists():
    text = f'Не правильно введен айди, начни заново: /edit_results'
    return text

def getEditBetResultTextIfBetExists(id, betUID):
    data = getBetByBetID(betID=int(betUID), id=id, params=['DatePlaced', 'Game', 'Bet', 'Coff', 'Amount'])

    if data:
        data = data[0]
        new_line = '\n'
        text = 'Исход этого события будет изменен:'
        text += f'{new_line}Дата ставки: {data[0]}{new_line}Игра:    {data[1]}{new_line}Исход:   {data[2]}{new_line}' \
                f'Коф:    {data[3]}{new_line}Ставка:  {data[4]}{new_line}{new_line}' \
                f'Выиграла эта ставка или нет?'

        return text
    else:
        return False

def getBetResultUpdatedText():
    text = f'Результат ставки обновлен.'
    return text

def getAdminHelpCommandText():
    new_line = '\n'
    text = f'/get_users         - get list of users info {new_line}' \
           f'/get_user_bets     - get particular user bet list {new_line}' \
           f'/get_user_balance  - get particular user balance{new_line}' \
           f'/update_user_bets  - update particular user bets{new_line}' \
           f'/generate_report_a - generate todays report for all users'
    return text

def getHelpText():
    new_line = '\n'
    text = f'Этот бот позволяет вести учет ставок которые ты поставил{new_line}' \
           f'Основные правила:{new_line}' \
           f'1.Для того что бы использовать бота тебе нужно зарегестрироваться. Если еще не зарегестрирован: /start{new_line}' \
           f'2.Сейчас бот находиться на стадии тестировки, если какие то лаги используй /cancel, и пиши: @vadim_doroxov{new_line}' \
           f'3.В использовании каждой функции этого бота есть описание припера ответа, пожалуйста соблюдайте его.{new_line}' \
           f'4.Сейчас бот работает в редиме тестировки, если есть какие то задержки в ответе меньше 30-40 секунд подождите' \
           f'если больше жмите /cancel и начинайте заново /start или /place_bet{new_line}' \
           f'Основные функции:{new_line}' \
           f'/start - старт регистрации если не зарегестрирован, советую всегда начинать с этой функции для проверки регистрации.{new_line}' \
           f'/place_bet - поставить/добавить ставку в свой учет, текст ставки строго типизирован и описан при вызове функции,' \
           f'поменять в боте можно только исход ставки, для всего остального связывайтесь с админом.{new_line}' \
           f'/edit_result - зафиксировать исход события, один раз для каждой ставки!{new_line}' \
           f'/get_balance_history - генерирует  таблицу с историей вашего баланса.{new_line}' \
           f'/get_bets_history - генерирует таблицу с историей всех ваший ставок.{new_line}' \
           f'/help - для вызова этого текста.{new_line}' \
           f'Админ: @vadim_doroxov'
    return text

def getPromtSportText():
    text = f'Введи спорт на который сделал ставку'
    return text

def getPromptGameText(sport):
    new_line = '\n'
    tab = '\t'
    text = f'---Ставка---{new_line}' \
           f'Спорт:{tab}{sport}{new_line}' \
           f'------------{new_line}' \
           f'Введи игру на которую сделал ставку'
    return text

def getPromptLeagueText(sport, game):
    new_line = '\n'
    tab = '\t'
    text = f'---Ставка---{new_line}' \
           f'Спорт :{tab}{sport}{new_line}' \
           f'Игра   :{tab}{game}{new_line}' \
           f'------------{new_line}' \
           f'Введи Лигу'
    return text

def getPromptBetText(sport, game, league):
    new_line = '\n'
    tab = '\t'
    text = f'---Ставка---{new_line}' \
           f'Спорт :{tab}{sport}{new_line}' \
           f'Игра   :{tab}{game}{new_line}' \
           f'Лига   :{tab}{league}{new_line}' \
           f'------------{new_line}' \
           f'Введи ставку'
    return text

def getPromtCoffText(sport, game,league, bet):
    new_line = '\n'
    tab = '\t'
    text = f'---Ставка---{new_line}' \
           f'Спорт :{tab}{sport}{new_line}' \
           f'Игра   :{tab}{game}{new_line}' \
           f'Лига   :{tab}{league}{new_line}' \
           f'Исход :{tab}{bet}{new_line}' \
           f'------------{new_line}' \
           f'Введи кофф (прим 2.0, 1.84)'
    return text

def getPromtAmontText(sport, game,league, bet, coff):
    new_line = '\n'
    tab = '\t'
    text = f'---Ставка---{new_line}' \
           f'Спорт :{tab}{sport}{new_line}' \
           f'Игра   :{tab}{game}{new_line}' \
           f'Лига   :{tab}{league}{new_line}' \
           f'Исход :{tab}{bet}{new_line}' \
           f'Коф      :{tab}{coff}{new_line}' \
           f'------------{new_line}' \
           f'Введи сумму ставки (прим 1400)'
    return text

def getPromtPercentText(sport, game, league,bet, coff, amount):
    new_line = '\n'
    tab = '\t'
    text = f'---Ставка---{new_line}' \
           f'Спорт :{tab}{sport}{new_line}' \
           f'Игра   :{tab}{game}{new_line}' \
           f'Лига   :{tab}{league}{new_line}' \
           f'Исход :{tab}{bet}{new_line}' \
           f'Коф      :{tab}{coff}{new_line}' \
           f'Сумма :{tab}{amount}{new_line}' \
           f'------------{new_line}' \
           f'Введи свой процент (прим 10)'
    return text

def getPromtDatePlacedText(sport, game ,league, bet, coff, amount, percentOwn):
    new_line = '\n'
    tab = '\t'
    text = f'------------Ставка----------{new_line}' \
           f'Спорт               :{tab}{sport}{new_line}' \
           f'Игра                 :{tab}{game}{new_line}' \
           f'Лига                 :{tab}{league}{new_line}' \
           f'Исход               :{tab}{bet}{new_line}' \
           f'Коф                   :{tab}{coff}{new_line}' \
           f'Сумма              :{tab}{amount}{new_line}' \
           f'Твой процент  :{tab}{percentOwn}{new_line}' \
           f'----------------------------{new_line}' \
           f'Введи дату ставки(когда поставил) (прим 22-10-2022, 01-01-2001)'
    return text

def getPromtDateGameText(sport, game, league, bet, coff, amount, percentOwn, datePlaced):
    new_line = '\n'
    tab = '\t'
    text = f'------------Ставка----------{new_line}' \
           f'Спорт               :{tab}{sport}{new_line}' \
           f'Игра                 :{tab}{game}{new_line}' \
           f'Лига                 :{tab}{league}{new_line}' \
           f'Исход               :{tab}{bet}{new_line}' \
           f'Коф                   :{tab}{coff}{new_line}' \
           f'Сумма              :{tab}{amount}{new_line}' \
           f'Твой процент  :{tab}{percentOwn}{new_line}' \
           f'Дата ставки     :{tab}{datePlaced}{new_line}' \
           f'----------------------------{new_line}' \
           f'Введи дату Игры(когда рызыгрышь) (прим 22-10-2022, 01-01-2001)'
    return text

def getPromtBetConformation(sport, game,league, bet, coff, amount, percentOwn, datePlaced, dateOGame):
    new_line = '\n'
    tab = '\t'
    text = f'------------Ставка----------{new_line}' \
           f'Спорт               :{tab}{sport}{new_line}' \
           f'Игра                 :{tab}{game}{new_line}' \
           f'Лига                 :{tab}{league}{new_line}' \
           f'Исход               :{tab}{bet}{new_line}' \
           f'Коф                   :{tab}{coff}{new_line}' \
           f'Сумма              :{tab}{amount}{new_line}' \
           f'Твой процент  :{tab}{percentOwn}{new_line}' \
           f'Дата ставки     :{tab}{datePlaced}{new_line}' \
           f'Дата игры        :{tab}{dateOGame}{new_line}'\
           f'----------------------------{new_line}' \
           f'Верно?'
    return text


def getBetPlacedMessageText(sport, game,league, bet, coff, amount, percentOwn, datePlaced, dateOGame):
    new_line = '\n'
    tab = '\t'
    text = f'------------Ставка----------{new_line}' \
           f'Спорт               :{tab}{sport}{new_line}' \
           f'Игра                 :{tab}{game}{new_line}' \
           f'Лига                 :{tab}{league}{new_line}' \
           f'Исход               :{tab}{bet}{new_line}' \
           f'Коф                   :{tab}{coff}{new_line}' \
           f'Сумма              :{tab}{amount}{new_line}' \
           f'Твой процент  :{tab}{percentOwn}{new_line}' \
           f'Дата ставки     :{tab}{datePlaced}{new_line}' \
           f'Дата игры        :{tab}{dateOGame}{new_line}'\
           f'----------------------------{new_line}' \
           f'Ставка принята'
    return text



if __name__ == '__main__':
    print(getEditBetResultTextIfBetExists(id = 682847115, betUID = 1))