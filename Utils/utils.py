import pandas as pd
from config import *
import datetime
import os

def checkIfRegistredID(id):
    '''


    :return True if registred/ False if not:
    '''
    df = pd.read_csv(USERS_DATABASE_PATH)

    if id in df['TelegramID'].values:
        print('registred')
        return True
    else:
        print('not registred')
        return False

def checkIfRegistredName(name):
    '''

    :param name: String, check if named passed to this function is registred
    :return: True - registred / False - not
    '''

    df = pd.read_csv(USERS_DATABASE_PATH)
    if name in df['Name'].values:
        return True
    else:
        return False

def getNamebyID(id):
    '''

    :param id: telegram id of user name to be returned
    :return: name of correspondend telegram user
    '''

    df = pd.read_csv(USERS_DATABASE_PATH)
    name =df[df['TelegramID'] == id]['Name']
    try:
        return name.item()
    except ValueError:
        return False

def registerUser(id, name, uname):
    '''
    adding user to USERS_DATABASE_PATH csv file
    and creates bets files and betslips photos folder for the user

    :param id: integer tg id of user
    :param name: string user chosen name
    :param uname: string user tg name
    :return: None
    '''

    df_users = pd.read_csv(USERS_DATABASE_PATH)

    date = f'{str(datetime.datetime.now().day)}-{str(datetime.datetime.now().month)}-{str(datetime.datetime.now().year)}'
    row = {'Name': name, 'TelegramUName': uname, 'TelegramID': id, 'DateRegistred': date}

    df_users = df_users.append(row, ignore_index=True)
    df_users.to_csv(USERS_DATABASE_PATH, index=False)

    df_user = pd.DataFrame(
        {'BetUID': [], 'Sport': [], 'League': [], 'Game': [], 'Bet': [], 'Coff': [], 'Amount': [], 'PercentOwn': [], 'DatePlaced': [],
         'DateOGame': [], 'Result': []}, index = [])
    df_balance = pd.DataFrame(
        {'Date': [], 'Balance': [], 'BalanceMargin': []}
    )
    createUserDatabase(id)

    df_user.to_csv(getUserDataCSVPath(id), index=False)
    df_balance.to_csv(getUserBalancePath(id), index = False)

def getUserDataFolderPath(id):
    '''
    return user data folder path

    :param id: telegram id of user
    :return: path of correspondent user data folder
    '''

    path = USERS_DATABASE_BETS_DATA_PATH + str(id) + '/'
    return path

def getUserDataCSVPath(id):
    '''
    return user csv file path
    :param id: telegram id of user
    :return: str: path of correspondent user CSV folder
    '''

    path = getUserDataFolderPath(id) + 'bets.csv'
    return path

def getUserDataPhotosPath(id):
    '''
    return user photos folder path
    :param id: telegram id of user
    :return: path of correspondent user photos datafolder
    '''
    path = getUserDataFolderPath(id) + str('Betslips/')
    return path

def getUserBalancePath(id):
    '''

    :param id:  telegram ud of user
    :return: path to user balance csv file
    '''
    path = getUserDataFolderPath(id) + 'balance.csv'
    return path

def createUserDatabase(id):
    '''
    creates direcoty of user contains csv for beets file and folder for betslips photos
    :param id: user tg id
    :return: None
    '''
    folder_path = getUserDataFolderPath(id)
    csv_path = getUserDataCSVPath(id)
    photos_path = getUserDataPhotosPath(id)
    balance_path = getUserBalancePath(id)

    os.mkdir(folder_path)
    open(csv_path, 'a+')
    open(balance_path, 'a+')
    os.mkdir(photos_path)

def placeBet(id, bet_list):
    '''
    Adding bet to correspondent user csv file

    :param bet: bet -> array, format ['sport'(str), 'league'(str), 'game'(str), 'bet'(str), coff(float), amount(int),
                                       percent(int), date placed(str), date game (str)]
    :return: None
    '''
    df_user = pd.read_csv(getUserDataCSVPath(id))
    bet_uid = len(df_user) + 1
    bet_dict = {'BetUID': bet_uid, 'Sport': bet_list[0], 'League': bet_list[1],
                'Game':  bet_list[2], 'Bet':    bet_list[3],
                'Coff':  bet_list[4], 'Amount': bet_list[5],
                'PercentOwn': bet_list[6], 'DatePlaced': bet_list[7],
                'DateOGame': bet_list[8], 'Result': 'Pending'}

    df_user = df_user.append(bet_dict, ignore_index=True)
    df_user.to_csv(getUserDataCSVPath(id), index = False)

def getRegex():
    return '\((.*?)\)\((.*?)\)\((.*?)\)\((.*?)\)\(([0-9]*.[.].[0-9]*)\)\(([0-9]*)\)\(([0-9]*)\)\(([0-9]*.[-].[0-9]*.[-].[0-9]*)\)\(([0-9]*.[-].[0-9]*.[-].[0-9]*)\)'

def parseBet(bet):
    '''
    parsing bet from text format into list of bet data
    :param bet: string in format (спорт)(лига)(матч)(ставка)(коф)(сумма)(процент себе)(дата ставки)(дата события)
    :return: text format of the bet, list of bet
    '''
    bet_list = bet.replace('(', '').split(')')[:-1]
    return  bet_list

if __name__ == '__main__':


    #registerUser(id = 1488, name = 'Andrii', uname = 'AZ')
    bet_list = parseBet('(спорт)(лига)(матч)(ставка)(коф)(сумма)(процент себе)(дата ставки)(дата события)')
    placeBet(id = 1488, bet_list = bet_list)

