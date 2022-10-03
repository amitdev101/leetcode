#There is N delivery centers. 
#Each Delivery Outlet has some packages to be delivered, denoted by parcels[i]. 
#There is a Rule how delivery should be completed.
# On each day, an equal number of parcerls are to be dispatched from each 
#delivery center that has atleast one parcel remaining.
#Find minimum nunmber of days needed to deliver all the parcels.
#Input:
#parcels= {2,3,4,3,3}

#Output
#3

#*/

def min_days_equal_delivery(parcels):
    unique = set(parcels)
    return len(unique) - (0 in unique)
    

parcels = [2,3,4,3,3]   
print("total days:", min_days_equal_delivery(parcels))