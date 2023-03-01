from qdp import QDP
from Agent import agent
import pandas as pd
import argparse
class exchange():
    
    def __init__(self,name='fba_agent',path=None)-> None:
        self.account=agent(name=name)
        self.qdp= QDP(
        host="39.123.37.56",
        user ="QDPUSER",
        passward="Fbaquant1#",
        database="QDP",
        port=3307
        )
        self.path=path

    
    def get_stock_data(self,startday="2022-01-01",endday="2023-01-01"):
        if self.path==None:
            return self.qdp.get(
                table="PRICECHART_BY_DATE__KRX",
                symbols=["A005930"],
                start=startday,
                end=endday
            )
        else: return pd.read_csv(self.path)
        
    
    def save_stock_data(self):
        return self.get_stock_data().to_csv('stockdata.csv')
    

    def get_log_data(self):
        return self.account.trading(self.get_stock_data())

    def save_log_data(self):
        return self.get_log_data().to_csv('log.csv')
    

if __name__=="__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-d",'--data', default=None,help='csv path')
    parser.add_argument("-u",'--update',default='Exchange.py',help='run py name')
    args=parser.parse_args()
    if args.update== 'Exchange.py':
        ex=exchange(path=args.data)
        ex.save_stock_data()
        ex.save_log_data()

