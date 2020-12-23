'''
DynamicTimeWrapper Algorithm for matrix    
Auther: George WU
Date: 2020-12-01
'''

import numpy as np 

def cal_connect_count(distance_table):
    # inital connection number: the connection of last value in each series  
    connect_num = 1

    # backward search 
    i,j = distance_table.shape[0]-1, distance_table.shape[1]-1 
    while i>0 and j>0:
        # take care of the order 
        cand_distance = {
            distance_table[i-1,j]:(i-1,j),
            distance_table[i,j-1]:(i,j-1),
            distance_table[i-1,j-1]:(i-1,j-1)
        }
        i,j = cand_distance[min(cand_distance)]
        connect_num += 1 
        

    if i+j != 0:
        connect_num += (i+j)

    return connect_num 



def cal_dtw_distance(stacked_series:'stacked series: series1 & series2',split:'split: beginning index of series2'=20):
    
    series1 = stacked_series[:split]
    series2 = stacked_series[split:] 
    
    # set initial path distance table & cumulative distance 
    distance_table = np.full([len(series1),len(series2)],np.nan)
    
    # cal_distance: 
    cal_distance = lambda x,y: (x-y)**2
    
    # recurssion calculation: 
    def cal_cum_distance(i,j):
        
        # already been calculated 
        if distance_table[i,j] == distance_table[i,j]:
            return distance_table[i,j]
        else:
            # recurssion calculation 
            if i>0 and j>0:
                temp_distance = cal_distance(series1[i],series2[j]) + min(cal_cum_distance(i-1,j-1),cal_cum_distance(i-1,j),cal_cum_distance(i,j-1))
            elif i>0 and j==0:
                temp_distance = cal_distance(series1[i],series2[j]) + cal_cum_distance(i-1,j)
            elif i==0 and j>0:
                temp_distance = cal_distance(series1[i],series2[j]) + cal_cum_distance(i,j-1)
            elif i==0 and j==0:
                temp_distance = cal_distance(series1[i],series2[j])
            
            # update recording 
            distance_table[i,j] = temp_distance 
            # return 
            return temp_distance 
    
    # cumulative distance
    cum_distance = cal_cum_distance(len(series1)-1,len(series2)-1) 
    
    # number of connection 
    connect_count = cal_connect_count(distance_table)
    
    mean_distance = cum_distance/connect_count 
    
    return mean_distance 