# Done By Richard

from Basic_Store_Func import *

#store names eg. 'Western Stall', 'MacDonalds'
#date: 'dd mm yyyy hh min' eg. '23 10 2020 10 00'
#day eg. 'Monday', 'Tuesday'
#period eg. 'Opening Hours', 'Breakfast', 'Lunch', 'Dinner'

def Return_All_Store_Menu(date_of_interest): #input date. Returns dictionary with stall name as key, and menu as value in a list
    current_menu = {}
    for store,menu in zip(Return_Store_Names(), [Return_Store_Menu(store_name=store_name,date_of_interest=date_of_interest) for store_name in Return_Store_Names()]):
        if menu != None:
            current_menu[store] = menu
    return current_menu

def Return_All_Store_Status(date_of_interest,period_of_interest): #input date and period. Returns status,status as list of Booleans
    curent_status = [Return_Store_Status(store_name=store_name,date_of_interest=date_of_interest,period_of_interest=period_of_interest) for store_name in Return_Store_Names()]
    return curent_status


def Stores_In_Operation(date_of_interest='now',period_of_interest='Opening Hours'): # returns store names as list of strings
    open_now=[]
    for store, open in zip(Return_Store_Names(),
                           Return_All_Store_Status(date_of_interest=date_of_interest, period_of_interest=period_of_interest)):
        if open == True:
            open_now.append(store)
    return open_now
