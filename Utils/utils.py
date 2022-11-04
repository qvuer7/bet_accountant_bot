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
         'DateOGame': [], 'Result': [], 'MarginTotal': [], 'MarginUP': [], 'MarginYours': []}, index = [])
    df_balance = pd.DataFrame(
        {'Date': [], 'BalanceUP': [], 'BalanceOwn': []}
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

def getUserExcellBetsPath(id):
    path = getUserDataFolderPath(id = id)+str(id) + '_bets.xlsx'
    return path

def getUserExcellBalancePath(id):
    path = getUserDataFolderPath(id = id) + str(id) + '_balance.xlsx'
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

def getUserOpenedBetsList(id, params):
    '''

    :param id: telegram id of user
    :param params: params of bet to be returned from list
    :return:
    '''
    df = pd.read_csv(getUserDataCSVPath(id))
    df = df.loc[df['Result'] == 'Pending'][params]
    if df.empty:
        return False
    else:
        return df.values.tolist()

def changeBetResult(id, betId, result):
    '''

    :param id: int telegram user id
    :param betId: int bet id
    :param result: Win/Loss
    :return:
    '''
    user_bet_df = pd.read_csv(getUserDataCSVPath(id))

    if int(betId) not in user_bet_df['BetUID'].values:
        return False

    else:
        print('bet id found')
        user_bet_df.loc[user_bet_df['BetUID'] == betId, 'Result'] = result
        user_bet_df.to_csv(getUserDataCSVPath(id), index = False)
        return True

def calculateUserBalance(id):
    df = pd.read_csv(getUserDataCSVPath(id))
    df.loc[df['Result'] == 'Win', 'MarginTotal'] = df.loc[df['Result'] == 'Win', 'Amount'] * \
                                                    df.loc[df['Result'] == 'Win', 'Coff']  - \
                                                    df.loc[df['Result'] == 'Win', 'Amount']
    df.loc[df['Result'] == 'Loss', 'MarginTotal'] = -df.loc[df['Result'] == 'Loss', 'Amount']
    df.loc[df['Result'] != 'Pending', 'MarginUP'] = df.loc[df['Result'] != 'Pending', 'MarginTotal'] * \
                                                    (100 - df.loc[df['Result'] != 'Pending', 'PercentOwn'])/100
    df.loc[df['Result'] != 'Pending', 'MarginYours'] = df.loc[df['Result'] != 'Pending', 'MarginTotal'] * \
                                                        df.loc[df['Result'] != 'Pending', 'PercentOwn']/100

    df.to_csv(getUserDataCSVPath(id), index = False)

def updateUserBalance(id):
    df_balance = pd.read_csv(getUserBalancePath(id))
    df_bets = pd.read_csv(getUserDataCSVPath(id))

    df_balance['Date'] =  df_bets['DateOGame'].unique()

    for date in df_bets['DateOGame'].unique():
        df_balance.loc[df_balance['Date'] == date, 'BalanceOwn'] = \
            df_bets.loc[df_bets['DateOGame'] == date, 'MarginYours'].sum()

        df_balance.loc[df_balance['Date'] == date, 'BalanceUP'] = \
            df_bets.loc[df_bets['DateOGame'] == date, 'MarginUP'].sum()

    df_balance.to_csv(getUserBalancePath(id), index = False)

def generateUserBetsHistoryXSL(id):
    df = pd.read_csv(getUserDataCSVPath(id = id))
    df.to_excel(getUserExcellBetsPath(id = id))
    return True

def generateUserBalanceHistoryXSL(id):
    df = pd.read_csv(getUserDataCSVPath(id = id))
    df.to_excel(getUserExcellBalancePath(id = id))
    return True

def getBetByBetID(betID, id, params):
    df = pd.read_csv(getUserDataCSVPath(id))
    df = df.loc[df['BetUID'] == betID][params]
    if df.empty:
        return False
    else:
        return df.values.tolist()


if __name__ == '__main__':
    '''
    registerUser(id = 1488, name = 'Andrii', uname = 'AZ')
    bet_list = parseBet('(Football)(Italia 1)(Juventus - Lazio)(W1)(1.83)(1500)(10)(22-10-2022)(29-10-2022)')
    placeBet(id = 1488, bet_list = bet_list)
    placeBet(id=1488, bet_list=bet_list)
    placeBet(id = 1488, bet_list = bet_list)
    changeBetResult(id=1488, betId=1, result='Win')
    changeBetResult(id=1488, betId=2, result='Loss')
    changeBetResult(id=1488, betId=3, result='Win')


    bet_list = parseBet('(Football)(Italia 1)(Juventus - Lazio)(W1)(1.83)(1500)(10)(26-10-2022)(24-10-2022)')
    placeBet(id = 1488, bet_list = bet_list)
    bet_list = parseBet('(Football)(Italia 1)(Juventus - Lazio)(W1)(1.83)(1500)(10)(26-10-2022)(11-12-2022)')
    placeBet(id=1488, bet_list=bet_list)
    changeBetResult(id = 1488, betId=4, result = 'Win')
    changeBetResult(id=1488, betId=5, result='Win')
    calculateUserBalance(id = 1488)
    updateUserBalance(id = 1488)
    
    generateUserBetsHistoryXSL(id = 1488)
    generateUserBalanceHistoryXSL(id = 1488)
    '''
    #changeBetResult(id = 682847115, betId=2, result = 'Huynya')
    calculateUserBalance(id = 682847115)
    updateUserBalance(id = 682847115)