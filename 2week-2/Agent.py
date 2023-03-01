from qdp import QDP
import pandas as pd
class agent():
    
    def __init__(self,name,credits=1000000,holdings=0):
        self.name=name
        self.credits=credits
        self.holdings=holdings
         #qdp.ipynb return 값
    
    def trading(self,stock_data:pd.DataFrame):
        stock_data['CLOSE_SHIFT1']=stock_data['CLOSE'].shift(1,fill_value=10**10)
        stock_data['CLOSE_SHIFT2']=stock_data['CLOSE'].shift(2,fill_value=10**10)
        stock_data['BUY_SELL']=0
        stock_data['LOG']=None
        for idx, val in stock_data.iterrows():
            if self.credits>val['CLOSE']:
                if val['CLOSE_SHIFT1']<val['CLOSE'] and val['CLOSE_SHIFT2']<val['CLOSE_SHIFT1']:
                    
                    buy_count=self.credits//val['CLOSE']
                    stock_data.loc[idx,'BUY_SELL']=buy_count
                    self.credits-=buy_count*val['CLOSE']
                    self.holdings+=buy_count
                    stock_data.loc[idx,'LOG']=f"{self.name}.now credits {self.credits} buys {buy_count} ${val['CLOSE']} at {val['DATE']}"
            if self.holdings >0:
                if val['CLOSE_SHIFT1']>=val['CLOSE']:

                    sell_amount=self.holdings*val['CLOSE']
                    self.credits+=sell_amount
                    stock_data.loc[idx,'BUY_SELL']=sell_amount
                    stock_data.loc[idx,'LOG']=f"{self.name}.now credits {self.credits} sells {self.holdings} ${val['CLOSE']} at {val['DATE']}."
                    self.holdings=0
                    

        return stock_data.loc[stock_data['BUY_SELL']!=0]['LOG']

        
if __name__=='__main__':
    qdp = QDP(
    host="39.123.37.56",
    user ="QDPUSER",
    passward="Fbaquant1#",
    database="QDP",
    port=3307
)
    price = qdp.get(
    table="PRICECHART_BY_DATE__KRX",
    symbols=["A005930"],
    start="2022-01-01",
    end="2023-01-01"
)
    ag=agent('a',1000000,0,price)
    print(ag.trading())
