import re
from orders import *


def outputAlpha(order_list, isBuy):
    outputStr = ""
    if isBuy:
        outputStr += "B:"
    else:
        outputStr += "S:"

    for order in order_list:
        isICE =  order.get_order_type() == OrderType.ICE
        actual_qty = "({})".format(order.get_qty()) if isICE else ""
        display_qty = order.get_display_qty() if isICE else order.get_qty()
        orderStr = " {}{}@{}#{}".format(display_qty,actual_qty,int(order.get_price()),order.get_id())
        print(orderStr)
        outputStr += orderStr
    return outputStr
