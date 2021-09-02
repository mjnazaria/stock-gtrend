

import pandas as pd    
import numpy as np     
from pytrends.request import TrendReq
import smtplib   
from email.message import EmailMessage
import time


email_address = 'doe@gmail.com'
email_pass = '123'

tickers = pd.read_csv('...\tickers.csv')

smoothing_win_length = 3    # smooth the search number using 3 min long window
threshold = 3               # threshold for search spike ratio to baseline

tickers = list(tickers)
tickers = [tickers[i:i+4] for i in range(0, len(tickers), 4)]   # split the tickser list into small blocks of 4 because of google api limit! 

t = time.localtime()
while t[3] < 16:
    for ticks in tickers:
        pytrend = TrendReq(timeout=(10,25), retries=3)
        pytrend.build_payload(kw_list=ticks, cat=0, timeframe='now 4-H') # now 1-d , now 4-H
        data = pytrend.interest_over_time()
        data.drop(columns='isPartial', inplace=True)
                      
        data_smooth = data.rolling(window=smoothing_win_length).mean().dropna()        
        baseline = data_smooth.iloc[:-10].mean()        
        alert = data_smooth.iloc[-1]/baseline > threshold
        
        
        if alert.sum() > 0:
            msg = EmailMessage()
            msg['From'] = email_address
            msg['To'] = email_address
            msg['Subject'] = ' * '.join(alert[alert==True].index)
            msg.set_content(' ')
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                 smtp.login(email_address, email_pass)
                 smtp.send_message(msg)  
            

        time.sleep(np.random.uniform(10,20))         
        t = time.localtime()
    

