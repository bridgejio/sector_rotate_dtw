import numpy as np
import pandas as pd

def long_only_backtest(trading_date:'list',split_date_list:'date to change position',data_ret:'return of data',position:'position'):
    
    # set initial value 
    port_value = 1 
    port_value_record = {} 
    mmd = 0 
    
    for split_date in split_date_list:
        split_date_index = trading_date.index(split_date)
        period_date = trading_date[split_date_index+20:split_date_index+40]       
    
        long_cand_asset = position[split_date]
        if min(long_cand_asset.values()) < 0:
            long_asset = []
        else:
            long_asset = [k for k,v in long_cand_asset.items()]
            # positions 
            num_of_asset = len(long_asset)
            port_by_asset = np.array([port_value/num_of_asset]*num_of_asset)  

        for date in period_date:
            if long_asset:
                port_by_asset *= np.array(data_ret[long_asset].loc[date].mean()+1)
                port_value = sum(port_by_asset)
                port_value_record[date] = port_value
            else:
                # empty position 
                port_value_record[date] = port_value
    
    port_value_record = pd.Series(port_value_record).values
    port_value_record /= port_value_record[0]      
    
    return port_value_record


def long_short_backtest(trading_date,split_date_list,data_ret,long_position, short_position):
    
    # set initial value 
    long_port_value = 0.5
    short_port_value = 0.5 
    port_value = 1 
    port_value_record = {} 
    mmd = 0 
    
    for split_date in split_date_list:
        split_date_index = trading_date.index(split_date)
        period_date = trading_date[split_date_index+20:split_date_index+40]       
        
        # long position 
        long_cand_asset = long_position[split_date]
        if min(long_cand_asset.values()) < 0:
            long_asset = []
        else:
            long_asset = list(long_cand_asset)
            # positions 
            num_of_long_asset = len(long_asset)
            long_port_by_asset = 0.5 * np.array([port_value/num_of_long_asset]*num_of_long_asset)  
            long_port_value = sum(long_port_by_asset)
        
        # short position 
        short_cand_asset = short_position[split_date]  
        if max(short_cand_asset.values()) > 0:
            short_asset = []
        else:
            short_asset = list(short_cand_asset)        
            # positions 
            num_of_short_asset = len(short_asset)
            short_port_by_asset = 0.5 * np.array([port_value/num_of_short_asset]*num_of_short_asset)        
            short_port_value = sum(short_port_by_asset)
        
        for date in period_date:
            
            # long asset change 
            if long_asset: 
                long_port_by_asset *= np.array(data_ret[long_asset].loc[date].mean()+1)     
                long_port_value = sum(long_port_by_asset)    
            else:
                pass    
            # short asset change 
            if short_asset:
                short_port_by_asset *= np.array(-data_ret[short_asset].loc[date].mean()+1)    
                short_port_value = sum(short_port_by_asset)
            else:
                pass
            
            port_value = long_port_value + short_port_value 
            port_value_record[date] = port_value 
    
    port_value_record = pd.Series(port_value_record).values
    port_value_record /= port_value_record[0]      
    
    return port_value_record


def general_stat(value:'array-like'):
    # annualized return      
    annual_ret = ((value[-1]/value[0])**(250/len(value)) -1)*100    
    
    # maximum drawdown 
    mmd = max((np.maximum.accumulate(value) - value) / np.maximum.accumulate(value))
    
    # Sharpe Ratio
    ret = pd.Series(value).pct_change()
    sharpe_ratio = np.sqrt(250) * ret.mean()/ret.std()
    
    # annualized volatility 
    annual_vol = np.sqrt(250) * ret.std()     
    
    return {
        'annualized return':annual_ret,
        'maximum drawdown':mmd,
        'sharpe ratio':sharpe_ratio,
        'annualized vol': annual_vol
    }