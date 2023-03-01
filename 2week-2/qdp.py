import time
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine
import pymysql
class QDP:

    def __init__(self, host, user, passward, database, port):
        """QDP SQL DATABASE

        Args:
            host (str): host ip
            user (str): user id
            passward (str): user passward
            database (str): name of database
            port (int): port

        Note:
            Database is a part of QDP project.
            It's a property of FBA Quant.
        """
        self.__sql_engine  = create_engine("mysql+pymysql://{user}:{pw}@{host}:{port}/{db}".format(
                                                                                                    user=user,
                                                                                                    pw=passward,
                                                                                                    host=host,
                                                                                                    port=port,
                                                                                                    db=database
                                                                                                )
                                        )                                       

    @property
    def table(self):
        command = "SHOW TABLE STATUS"
        df = pd.read_sql_query(sql=command, con=self.__sql_engine)
        return df
    
    @staticmethod
    def now(format="%Y:%m:%d %H:%M:%S.%f"):
        return datetime.fromtimestamp(time.time()).strftime(format)

    def get(self, table, symbols=None, columns=None, start=None, end=None, symbol_check=True):
        """Get Method

        Args:
            table (str): name of DB table
            symbols (list): list of symbols
            columns (list): list of columns
            start (DATE or DATETIME): %Y-%m-%d
            end (DATE or DATETIM): %Y-%m-%d
            symbol_check (bool): if True, checks whether the required symbols are in the table or not
        
        Returns:
            pd.DataFrame
        """

        # Manual limit of frequent queries... TODO --> 서버단위의 Query Limit 생성?
        time.sleep(0.25)

        # TypeChecking
        if type(symbols) != type(None) and type(symbols) != list:
            raise TypeError("symbols must be list")
        if type(columns) != type(None) and type(columns) != list:
            raise TypeError("columns must be list")

        # The code below returns Exception if the queried symbol doesn't exist in the TABLE
        if symbol_check:
            not_exist_symbol = []
            command = "SELECT DISTINCT SYMBOL FROM {table}".format(table=table)
            exist_symbol = set(pd.read_sql_query(sql=command, con=self.__sql_engine)["SYMBOL"])
            for symbol in symbols:
                if symbol not in exist_symbol:
                    not_exist_symbol.append(symbol)
            if len(not_exist_symbol) != 0:
                raise Exception("{} doesn't exist in {table}".format(not_exist_symbol, table=table))

        # Replace arguments for SQL query
        if type(symbols) == type(None):
            symbols = "*"
        else:
            symbols = str(symbols).replace("[","(").replace("]",")")

        if type(columns) == type(None):
            columns = "*"
        else:
            columns = ["DATE", "SYMBOL"] + columns
            columns = str(columns).replace("[","(").replace("]",")").replace("'","")

        if type(start) == type(None):
            start = self.now("%Y-%m-%d")
        if type(end) == type(None):
            end = self.now("%Y-%m-%d")

        # SQL Query
        command = "SELECT {columns} FROM {table} ".format(columns=columns, table=table)

        if symbols != "*":
            command = command + "WHERE SYMBOL in {symbols} ".format(symbols=symbols)
        
        if "WHERE" in command:
            command = command + "AND DATE BETWEEN '{start}' AND '{end}'".format(start=start, end=end)
        else:
            command = + "WHERE DATE BETWEEN '{start}' AND '{end}'".format(start=start, end=end)

        # Run the SQL command
        df = pd.read_sql_query(sql=command, con=self.__sql_engine)

        return df