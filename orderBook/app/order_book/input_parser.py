import re
from orders import *

# TODO: double check if data is valid (because now it's set to default values if invalid) 
def parseAlphaFormat(orderString):
    """
    It's called alpha format cuz it's from alpha lab haha  
    Parses the message and generates an object to be used later

    @return1 isOrder
    @return2 Order/Action object     
    """

    a = orderString.split(" ")
    retObj = None
    isOrder = (a[0] == "SUB")
    if (isOrder):
        orderType = ""
        price = 0
        displayQty = 0
        if (a[1] == "LO"):
            orderType = OrderType.LIMIT
            price = a[5]
        elif (a[1] == "MO"):
            orderType = OrderType.MARKET
            price = -1
        elif (a[1] == "IOC"):
            orderType = OrderType.IOC
            price = a[5]
        elif (a[1] == "FOK"):
            orderType = OrderType.FOK
            price = a[5]
        else:
            orderType = OrderType.ICE
            price = a[5]
            displayQty = a[6]

        side = ""
        if (a[2] == "B"):
            side = Side.B
        else:
            side = Side.S

        id = a[3]
        qty = a[4]
        retObj = Order(id,price,orderType,qty,side, displayQty)
    else:
        actionType = ""
        new_qty = -1
        new_price = -1
        if (a[0] == "CXL"):
            actionType = ActionType.CXL
        else:
            actionType = ActionType.CRP
            new_qty = a[2]
            new_price = a[3]
        id = a[1]
        retObj = Action(actionType,id,new_qty,new_price)

    return isOrder,retObj

