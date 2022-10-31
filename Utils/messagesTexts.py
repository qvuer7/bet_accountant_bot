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
           f'Используй /place_bet что бы ставить.'
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

if __name__ == '__main__':
    print(getStartIfNotRegisterText())