import heapq
from orders import *
from limit import *

# TODO: use custom heap implementation
# TODO: Rethink the apporach of this code, i think im supposed to add any orders directly first, then evaluate if a match has occured
class Book():
    """
    Priority of book  is first by price, second by time
    Buy Priority: Higher price, higher priority
    Sell Priority: Lower price, higher priority
    Note: Only for specific stock. Not sure if each stock/asset has it's own book but feels like it
    """
    def __init__(self):
        self.buy_tree = []    # max heap, a list of Limit objects
        self.buy_len = 0
        self.sell_tree = []   # min heap, a list of Limit objects, https://stackoverflow.com/questions/7941011/traversing-heapified-list
        self.sell_len = 0
        self.buyOrderMap = {}  #order id to order object
        self.sellOrderMap = {}
        self.limitBuyMap = {}  #limit price to limit object
        self.limitSellMap = {}
        self.totalSales = 0
        self.saleStates = []

    def inc_buy_len(self):
        self.buy_len += 1

    def dec_buy_len(self):
        self.buy_len -= 1
    
    def get_buy_len(self):
        return self.buy_len
        
    def get_sell_len(self):
        return self.sell_len
    
    def inc_sell_len(self):
        self.sell_len += 1
    
    def dec_sell_len(self):
        self.sell_len -= 1

    def add_new_limit(self, limitObj, isBuy=True):
        tree = self.buy_tree if isBuy else self.sell_tree
        heapq.heappush(tree,  limitObj)
        self.limitBuyMap[limitObj.get_limit_price()] = limitObj
        self.inc_buy_len()

    def get_total_sales(self):
        return self.totalSales

    def get_latest_sales_state(self):
        # print(len(self.saleStates))
        # print(self.saleStates)
        return self.saleStates[len(self.saleStates) - 1]

    def new_sales_state(self, sale):
        self.saleStates.append(sale)

    def order_buy_list(self):
        self.buy_tree.sort()

    def order_sell_list(self):
        self.sell_tree.sort()


    def get_lowest_sell(self):
        return self.sell_tree[0] if self.sell_len > 0 else None

    def get_lowest_sell_order(self):
        lowest_limit = self.get_lowest_sell()
        # print("lowest_limit")
        # print(lowest_limit)
        if lowest_limit == None:
            return None
        return lowest_limit.get_top_order()

    def get_highest_buy(self):
        return self.buy_tree[0] if self.buy_len > 0 else None

    def get_highest_buy_order(self):
        lowest_limit = self.get_highest_buy()
        # print("lowest_limit")
        # print(lowest_limit)
        if lowest_limit == None:
            return None
        return lowest_limit.get_top_order()


    # meant for FOKs 
    def remove_top_sell_limit(self):
        cur_limit = self.get_lowest_sell()
        heapq.heappop(self.sell_tree)
        self.limitSellMap.pop(cur_limit.get_limit_price())
        self.dec_sell_len()
    
    # meant for FOKs
    def remove_top_buy_limit(self):
        cur_limit = self.get_highest_buy()
        heapq.heappop(self.buy_tree)
        self.limitBuyMap.pop(cur_limit.get_limit_price())
        self.dec_buy_len()
    
    def remove_top_sell(self):
        # print("remove_top_sell: ", "=" * 50)
        best_sell = self.get_lowest_sell()
        order_removed = None
        # print(best_sell)
        # print(f"best_sell: {best_sell.get_size()}")
        # print([x.get_limit_price() for x in self.sell_tree])
        # print("")
        if best_sell and best_sell.get_size() > 1:
            # print("Removing one order fro sell limit")
            order_removed = best_sell.remove_first()
        else:
            # print("No more sell limits")
            order_removed = heapq.heappop(self.sell_tree)
            self.limitSellMap.pop(best_sell.get_limit_price())
            self.dec_sell_len()
        
        # print([x.get_limit_price() for x in self.sell_tree])
        return order_removed
    def remove_top_buy(self):
        best_buy = self.get_highest_buy()
        # print(best_buy)
        # print(f"best_buy: {best_buy.get_size()}")
        # print([x.get_limit_price() for x in self.buy_tree])
        # print("")
        order_removed = None
        if best_buy and best_buy.get_size() > 1:
            # print("Removing one order from buy limit")
            order_removed = best_buy.remove_first()
        else:
            # print("No more buy limits")
            order_removed = heapq.heappop(self.buy_tree)
            self.limitBuyMap.pop(best_buy.get_limit_price())
            self.dec_buy_len()
        
        # print([x.get_limit_price() for x in self.buy_tree])
        return order_removed


    def receive_order(self, orderObj):
        """
            Receives order from somewhere 
        """
        print("An order was received")
        # print("Buy tree len: ", self.buy_len)
        # print("Sell tree len: ", self.sell_len)
        # print(f"orderObj: {orderObj.get_id()} {orderObj.get_qty()} {orderObj.get_price()}")
        curSale = 0
        if orderObj.get_order_type() == OrderType.LIMIT:
            curSale = self.execute_LO(orderObj)
        elif orderObj.get_order_type() == OrderType.MARKET:
            curSale = self.execute_MO(orderObj)
        elif orderObj.get_order_type() == OrderType.IOC:
            curSale = self.execute_IOC(orderObj)
        elif orderObj.get_order_type() == OrderType.FOK:
            curSale = self.execute_FOK(orderObj)
        else:
            curSale = self.execute_ICE(orderObj)

        self.totalSales += curSale
        self.new_sales_state(curSale)

    def receive_action(self, actionObj):
        # print("An action was received")
        if actionObj.get_action_type() == ActionType.CXL:
            self.execute_CXL(actionObj)
        elif actionObj.get_action_type() == ActionType.CRP:
            self.execute_CRP(actionObj)
        # self.new_sales_state(0)

    def execute_order(self, order_obj):
        isBuy = order_obj.get_side() == Side.B
        getBestOrder, removeTopOrder = None, None
        if isBuy:
            getBestOrder = self.get_lowest_sell_order
            removeTopOrder = self.remove_top_sell

        else:
            getBestOrder = self.get_highest_buy_order
            removeTopOrder = self.remove_top_buy

        bestOrder = getBestOrder()
        curSale = 0
        while(bestOrder and bestOrder.isMatch(order_obj) and order_obj.get_qty() > 0):
            bestOrder = getBestOrder()
            isICE = bestOrder.get_order_type() == OrderType.ICE
            displayQty = 0
            if isICE:
                displayQty = bestOrder.get_display_qty() 
                
            sell_price = bestOrder.get_price()

            sell_qty = bestOrder.get_qty() if not isICE else displayQty
            # print(f"sell_qty: {sell_qty}")
            buy_qty = order_obj.get_qty() 
            sale_amt = min(sell_qty, buy_qty)
            # print(f"sale_amt: {sale_amt}")
            buyLeft = buy_qty - sale_amt
            sellLeft = bestOrder.get_qty() - sale_amt
            curSale += sell_price * sale_amt
            order_obj.set_qty(buyLeft)

            
            shouldReaddICE = isICE and sellLeft > 0
            # print(f"shouldReaddICE: {shouldReaddICE}")
            if sale_amt == sell_qty:
                # print("Can still try to find another order from book")
                removed_order = removeTopOrder()
                if shouldReaddICE:
                    removed_order.set_qty(sellLeft)
                    curQty = removed_order.get_qty()
                    # displayQty = removed_order.get_display_qty()
                    if displayQty > curQty:
                        removed_order.set_display_qty(curQty)
                    self.insert_order(removed_order)


                    # print(f"READD ICE: {removed_order.get_id()} {removed_order.get_qty()} {removed_order.get_price()}")
                    
                    buyList = self.get_buy_orders()
                    sellList = self.get_sell_orders()

                    # print("buyList")
                    # print("sellList")

                    print([f"{x.get_id()} {x.get_qty()} {x.get_price()} {x.get_display_qty()}" for x in buyList])
                    print([f"{x.get_id()} {x.get_qty()} {x.get_price()} {x.get_display_qty()}" for x in sellList])
                bestOrder = getBestOrder()
            else:
                if isICE:
                    bestOrder.set_display_qty(displayQty - sale_amt)    
                bestOrder.set_qty(sellLeft)
        return curSale

    def insert_order(self, order_obj):
        isBuy = order_obj.get_side() == Side.B
        orderMap = self.buyOrderMap if isBuy else self.sellOrderMap
        limitMap = self.limitBuyMap if isBuy else self.limitSellMap
        tree = self.buy_tree if isBuy else self.sell_tree
        incLen = self.inc_buy_len if isBuy else self.inc_sell_len 
        orderPrice = order_obj.get_price()
        # print("Not fully fulfilled, add to buy order tree")
        # print(self.limitBuyMap)
        thisLimit = None
        if (orderPrice in limitMap):
            thisLimit = limitMap[orderPrice]
        else:
            #Wrap in function
            thisLimit = Limit(orderPrice,isBuy)
            heapq.heappush(tree, thisLimit)
            limitMap[orderPrice] = thisLimit
            incLen()
        thisLimit.add_order(order_obj) 
        orderMap[order_obj.get_id()] = order_obj

    def execute_LO(self,order_obj):

        curSale = self.execute_order(order_obj)
        

        #Check if order is completely fulfilled
        order_qty = order_obj.get_qty()

        if (order_qty > 0):
            self.insert_order(order_obj)
        return curSale

    def execute_MO(self,order_obj):
        return self.execute_order(order_obj)
    
    def execute_IOC(self,order_obj):
        return self.execute_order(order_obj)

    def execute_ICE(self,order_obj):
        return self.execute_LO(order_obj)
        # curSale =  self.execute_order(order_obj)

        # #Check if order is completely fulfilled
        # order_qty = order_obj.get_qty()

        # if (order_qty > 0):
        #     self.insert_order(order_obj)
        # return curSale


    def execute_FOK(self,order_obj):
        isBuy = False
        if (order_obj.get_side() == Side.B):
            isBuy = True 
            # return self.execute_FOK_B(order_obj)
            
        # return self.execute_FOK_S(order_obj)

        #  must sort the heapq list, but using timsort isn't that bad for semi sorted list
        # print(self.buy_tree)

        tree,removeTopLimit,getLength = None,None, None
        
        if isBuy:
            self.order_sell_list()
            tree = self.sell_tree
            getLength = self.get_sell_len
            removeTopLimit = self.remove_top_sell_limit
            # removeTopOrder
        else:
            self.order_buy_list()
            tree = self.buy_tree
            getLength = self.get_buy_len
            removeTopLimit = self.remove_top_buy_limit
        
        limitIdx = 0
        orderIdx = 0
        bestLimit = tree[limitIdx]
        bestOrder = bestLimit.get_top_order()
        curSale = 0
        # print("Start quantites: ", order_obj.get_qty())
        # print(f"Best Limit: {bestLimit.get_size()} , {bestLimit.get_limit_price()}")
        # print("Best Order: ", bestOrder.get_qty())
        while(bestOrder and order_obj.isMatch(bestOrder) and order_obj.get_qty() > 0):
            # bestSell = bestSellLimit.
            buy_price = bestOrder.get_price()
            sell_qty, buy_qty= order_obj.get_qty(), bestOrder.get_qty() 
            sale_amt = min(sell_qty, buy_qty)
            curSale += buy_price * sale_amt

            buyLeft = buy_qty - sale_amt
            sellLeft = sell_qty - sale_amt

            # print(f"buyLeft: {buyLeft}")
            # print(f"sellLeft: {sellLeft}")

            order_obj.set_qty(sellLeft)
            if sale_amt == buy_qty and buyLeft == 0:
                # Can still try to find another sell order
                # self.remove_top_sell()
                bestOrder = bestOrder.get_next_order()
                orderIdx += 1
                if bestOrder == None:
                    limitIdx += 1
                    orderIdx = 0
                    bestLimit = tree[limitIdx] if limitIdx < getLength() else None
                    bestOrder = bestLimit.get_top_order()
            else:
                bestOrder.set_qty(buyLeft)
                
        #     print(f"limitIdx: {limitIdx}")
        #     print(f"orderIdx: {orderIdx}")

        # print("Leftover quantites: ", order_obj.get_qty())
        # print(f"limitIdx: {limitIdx}")
        # print(f"orderIdx: {orderIdx}")
        if order_obj.get_qty() == 0:
            # print("FILL")
            cur_limit_idx = 0
            while (cur_limit_idx < limitIdx):
                removeTopLimit()
                cur_limit_idx += 1
            cur_order_idx = 0
            while (cur_order_idx < orderIdx):
                bestLimit.remove_first()
                cur_order_idx += 1
            return curSale
        
        # print("KILL")
        return 0


    def execute_CXL(self, actionObj):
        order_id = actionObj.get_order_id()
        # limit_price = 
        # print("CXL: ", order_id)
        # print(self.buyOrderMap)
        # print(self.sellOrderMap)
        # print((order_id not in self.buyOrderMap) and (order_id not in self.sellOrderMap))
        if order_id not in self.buyOrderMap and order_id not in self.sellOrderMap:
            return
        isBuy = True if order_id in self.buyOrderMap else False
        orderMap, limitMap = None, None
        
        if isBuy:
            orderMap = self.buyOrderMap
            limitMap = self.limitBuyMap
        else:
            orderMap = self.sellOrderMap
            limitMap = self.limitSellMap

        # print("Cancelling buy order")
        orderObj = orderMap[order_id]
        limitObj = limitMap[orderObj.get_price()]
        orderMap.pop(order_id)
        limitMap.pop(orderObj.get_price())

        # print(f'limit: {limitObj.limit_price}')
        limitObj.remove_order(order_id)
    def execute_CRP(self, actionObj):
        order_id = actionObj.get_order_id()
        isBuy = False
        # print("CRP: ", order_id)
        # print(self.buyOrderMap)
        # print(self.sellOrderMap)
        # print(self.limitBuyMap)
        # print((order_id not in self.buyOrderMap) and (order_id not in self.sellOrderMap))
        newPrice = actionObj.get_new_price()
        newQty = actionObj.get_new_qty()
        if order_id not in self.buyOrderMap and order_id not in self.sellOrderMap:
            return
        if order_id in self.buyOrderMap:
            isBuy = True
        orderMap, limitMap = None, None
        
        if isBuy:
            orderMap = self.buyOrderMap
            limitMap = self.limitBuyMap
        else:
            orderMap = self.sellOrderMap
            limitMap = self.limitSellMap
        
        orderObj = orderMap[order_id]
        curPrice = orderObj.get_price()
        curQty = orderObj.get_qty()
        # print(newPrice, curPrice)
        # print(newQty, curQty)
        limitObj = limitMap[curPrice]
        if curPrice == newPrice:
            orderObj.set_qty(newQty)
            if newQty > curQty:
                limitObj.move_order_to_back(orderObj)
        else:
            limitObj = limitMap[curPrice]
            limitObj.remove_order(order_id)
            orderMap.pop(order_id)
            if limitObj.get_size() == 0:
                limitMap.pop(curPrice)
            orderObj.set_price(newPrice)
            orderObj.set_qty(newQty)

            thisLimit = None

            if (newPrice in limitMap):
                thisLimit = limitMap[newPrice]
            else:
                # print("Adding new limit")
                thisLimit = Limit(newPrice, isBuy)
                self.add_new_limit(thisLimit, isBuy)
                
            thisLimit.add_order(orderObj) 
            orderMap[order_id] = orderObj


    """
    Returns a sorted array of orders based on their limits 
    """
    def get_buy_orders(self):
        print("GETTING ALL BUY ORDERS")
        self.buy_tree.sort()
        result = []
        for limitObj in self.buy_tree:
            print("limitObj: ",limitObj.get_limit_price())
            if limitObj:
                result.extend(limitObj.get_order_list())
                # print(result)
        return result

    def get_sell_orders(self):
        print("GETTING ALL SELL ORDERS")
        self.sell_tree.sort()
        result = []
        for limitObj in self.sell_tree:
            print("limitObj: ",limitObj.get_limit_price())
            if limitObj:
                result.extend(limitObj.get_order_list())
        return result
