import json
import os
from config import *
import pandas as pd
import datetime

class User:

    def __init__(self, id):

        self.id = id
        self.df_users = pd.read_csv(USERS_DATABASE_PATH)
        self.data_path = fr'/Users/andriizelenko/qvuer7/projects/beting_accountant/bets_data_from_users/{self.id}.csv'


    def _checkIfRegistredID(self):
        '''

        :return True if registred/ False if not:
        '''


        if self.id in self.df_users['TelegramID'].values:
            return True
        else:
            return False

    def _checkIfRegistredName(self, name):
        '''


        :param name: String, check if named passed to this function is registred
        :return: True - registred / False - not
        '''
        if name in self.df_users['Name']:
            return True
        else:
            return False

    def _getName(self):

        return self.df_users[self.df_users['TelegramID'] == self.id]['Name'].item()

    def _registerUser(self, uname, name):
        self.name = name
        self.uname = uname
        self.date = f'{str(datetime.datetime.now().day)}-{str(datetime.datetime.now().month)}-{str(datetime.datetime.now().year)}'
        row = {'Name' : self.name, 'TelegramUName': self.uname, 'TelegramID': self.id, 'DateRegistred':self.date}
        self.df_users = self.df_users.append(row, ignore_index=True)
        self.df_users.to_csv(r'/Users/andriizelenko/qvuer7/projects/beting_accountant/data/Users.csv', index=False)

        self.data_df = pd.DataFrame(
            {'Sport': [], 'League': [], 'Game': [],'Bet':[] ,'Coff': [], 'Amount': [], 'PercentOwn': [], 'DatePlaced': [],
             'DateOGame': []})
        self.data_path = fr'/Users/andriizelenko/qvuer7/projects/beting_accountant/bets_data_from_users/{self.id}.csv'
        self.data_file = open(self.data_path, 'a+')
        self.data_df.to_csv(self.data_path, index = False)

    def _placeBet(self, bet):
        self.data_df = pd.read_csv(self.data_path)
        bet2place = {'Sport': bet[0], 'League': bet[1], 'Game': bet[2],'Bet':bet[3], 'Coff': bet[4], 'Amount':bet[5], 'PercentOwn': bet[6], 'DatePlaced': bet[7],
                     'DateOGame': bet[8]}
        self.data_df = self.data_df.append(bet2place, ignore_index=True)
        self.data_df.to_csv(self.data_path, index = False)
