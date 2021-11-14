from order_book.orders import Order


class Limit:
    def __init__(self,limit_price, isBuy=True):
        """
        limit price refers to the common price for all the orders under this Limit object
        size refers to the number of orders that share this common price is

        """
        self.limit_price = limit_price
        self.isBuy = isBuy
        self.comp_price = -limit_price if isBuy else limit_price
        self.size = 0
        # self.parent,self.left,self.right = None,None,None #Limit instances
        self.topOrder, self.lastOrder = None, None
        self.orderIdToOrder = {}
        
    def __lt__(self, other):
        return self.comp_price < other.comp_price

    def __gt__(self, other):
        return self.comp_price > other.comp_price

    def get_limit_price(self):
        return self.limit_price

    def get_size(self):
        return self.size

    def set_size(self,size):
        self.size = size
    
    def inc_size(self):
        self.size += 1

    def dec_size(self):
        self.size -= 1
        
    def get_top_order(self):
        return self.topOrder

    def get_last_order(self):
        return self.lastOrder

    def get_order_list(self):
        res = []
        curNode = self.topOrder
        while (curNode):
            # print(curNode.get_id())
            res.append(curNode)
            curNode = curNode.next
        return res
    

    def remove_first(self):
        # print("remove_first: ","=" * 50)
        if (self.size == 0 or self.topOrder == None):
            return
        # print("Top Order get qty")
        # print(self.topOrder)
        # print(self.topOrder.get_qty())
        # print("")
        order_id = self.topOrder.get_id()
        order_removed = self.orderIdToOrder.pop(order_id)
        self.topOrder = self.topOrder.next
        order_removed.next = None
        order_removed.prev = None
        if self.topOrder:
            #Need to remove the limit itself or keep it there? I think ideally should remove
            self.topOrder.prev = None
        else:
            print("No more limits left")
        self.dec_size()
        return order_removed


    """
    Assumed order id inside
    """
    def remove_order(self, order_id):
        print(self.orderIdToOrder)
        if order_id not in self.orderIdToOrder:
            return
        orderObj = self.orderIdToOrder[order_id]
        prevObj = orderObj.prev
        nextObj = orderObj.next
        if prevObj:
            prevObj.next = nextObj
        else:
            self.topOrder = nextObj
        self.orderIdToOrder.pop(order_id)
        self.dec_size()

    def add_order(self, order):
        if (not self.lastOrder):
            print("New order in limit")
            print("")
            self.topOrder = order
            self.lastOrder = order
            self.lastOrder.next = None
            self.lastOrder.prev = None

        else:
            self.lastOrder.next = order
            order.prev = self.lastOrder
            self.lastOrder = self.lastOrder.next
        self.orderIdToOrder[order.get_id()] = order
        self.inc_size()

    def move_order_to_back(self, order):
        self.remove_order(order.get_id())
        self.add_order(order)