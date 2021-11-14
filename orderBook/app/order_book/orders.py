from enum import Enum
# from functools import total_ordering

# @total_ordering
class OrderType(Enum):
    LIMIT = 1
    MARKET = 2
    IOC = 3
    FOK = 4
    ICE = 5

    def __eq__(self, other):
        # print(self.value)
        # print(other.value)
        # print(self.__class__)
        # print(other.__class__)
        # print(isinstance(self, OrderType)) # True
        # print(isinstance(other, OrderType)) # False
        """Overrides the default implementation"""
        # if isinstance(other, OrderType):
        # if self.__class__ is other.__class__:
        return self.value == other.value
        # return False

class ActionType(Enum):
    CXL = 1
    CRP = 2

    def __eq__(self, other):
        return self.value == other.value

class Side(Enum):
    B = 1
    S = 2
    
    def __eq__(self, other):
        # print(dir(self))
        return self.value == other.value

class Order:
    def __init__(self,id,price,order_type,qty=0,side='B', display_qty=0):
        self.id = id
        self.price = float(price)  
        self.order_type = order_type
        self.qty = int(qty)
        self.display_qty = int(display_qty)
        self.side=side
        self.next, self.prev = None, None
    
    def get_id(self):
        return self.id

    def get_price(self):
        return self.price
    
    def set_price(self,p):
        self.price = p
        # if self.side == Side.B:
        #     # self.price

    def get_qty(self):
        return self.qty
    
    def set_qty(self, q):
        self.qty = q

    def get_order_type(self):
        return self.order_type
    
    def get_side(self):
        return self.side

    def get_next_order(self):
        return self.next

    def get_prev_order(self):
        return self.prev# if orderObj else None

    def get_display_qty(self):
        return self.display_qty

    def set_display_qty(self, qty):
        self.display_qty = qty

    # def is

    """
        Assumptions:
            1. one order is buy, the other is sell
    """
    def isMatch(self, other_order):
        if self.get_order_type() == OrderType.MARKET or other_order.get_order_type() == OrderType.MARKET:
            return True

        if other_order.get_side() == Side.B:
            return other_order.get_price() >= self.get_price()
        return other_order.get_price() <= self.get_price()

class Action:
    def __init__(self,action_type,order_id,new_qty=0,new_price=0):
        self.id = id
        self.action_type = action_type
        self.order_id = order_id
        self.new_qty = int(new_qty)
        self.new_price = float(new_price)

    def get_action_type(self):
        return self.action_type

    def get_order_id(self):
        return self.order_id

    def get_new_qty(self):
        return self.new_qty

    def get_new_price(self):
        return self.new_price
