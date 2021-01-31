import numpy as np

class DynamicTimeWrapper(object):
    
    def __init__(self,ts1:"time series 1",ts2:"time series 2"): 
        self.ts1 = ts1 
        self.ts2 = ts2 
        self.dist_table = np.full([len(ts1),len(ts2)],np.nan)    
        self.calDistFunc = lambda x,y: (x-y)**2 
        self.connection = [] 
    
        # recurssion calculation: 
    def calCumDist(self,i,j):
        
        # already been calculated 
        if self.dist_table[i,j] == self.dist_table[i,j]:
            return self.dist_table[i,j]

        if i == j == 0:
            cum_dist = self.calDistFunc(self.ts1[i],self.ts2[j])
        else:
            cand_index = [(i-1,j-1),(i-1,j),(i,j-1)] if (i>0 and j>0) else [(max(i-1,0),max(j-1,0))]
            dist = sorted([self.calCumDist(k,l) for k,l in cand_index])[0] 
            cum_dist = self.calDistFunc(self.ts1[i],self.ts2[j]) + dist 
        
        # update distance table 
        self.dist_table[i,j] = cum_dist 
        
        return cum_dist 
    
    def nodeConnection(self):

        # initialize 
        i,j = self.dist_table.shape[0]-1, self.dist_table.shape[1]-1 
        self.connection.append((i,j)) 

        # path backward search 
        while i>0 or j>0:
            if i>0 and j>0:
                cand_index = [(i-1,j-1),(i-1,j),(i,j-1)]
                cand_dist = [self.dist_table[k,l] for k,l in cand_index]
                i,j =  sorted(zip(cand_index,cand_dist),key=lambda x:x[1])[0][0]
                self.connection.append((i,j)) 
            else:
                i,j = max(i-1,0),max(j-1,0)
                self.connection.append((i,j)) 
        
        return 
    
    def generateNewDate(self):
        ts1_new = []
        ts2_new = [] 
        for i,j in self.connection:
            ts1_new.append(self.ts1[i])
            ts2_new.append(self.ts2[j])
        return ts1_new, ts2_new 
    
    def DTWMatchCorr(self):
        
        # distance & match 
        _ = self.calCumDist(len(self.ts1)-1,len(self.ts2)-1)
        
        # node connection
        self.nodeConnection()
        
        # new series (constructed by match results) 
        ts1_new, ts2_new = self.generateNewDate()        
        
        corr = np.corrcoef(ts1_new,ts2_new)[0,1]
    
        return corr