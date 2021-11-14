import heapq
from orders import *
from limit import *

# TODO: use custom heap implementation
# TODO: Rethink the apporach of this code, i think im supposed to add any orders directly first, then evaluate if a match has occured
class Book():
    def __init__(self):
        self.buy_tree = []    # max heap, a list of Limit objects
        self.buy_len = 0
        self.sell_tree = []   # min heap, a list of Limit objects
        self.sell_len = 0
        self.orderMap = {}
        self.limitBuyMap = {}
        self.limitSellMap = {}
        self.totalSales = 0

    def inc_buy_len(self):
        self.buy_len += 1

    def dec_buy_len(self):
        self.buy_len -= 1
    
    def inc_sell_len(self):
        self.sell_len += 1
    
    def dec_sell_len(self):
        self.sell_len -= 1

    def get_total_sales(self):
        return self.totalSales

    def get_lowest_sell(self):
        return self.sell_tree[0] if self.sell_len > 0 else None

    def get_lowest_sell_order(self):
        lowest_limit = self.get_lowest_sell()
        print("lowest_limit")
        print(lowest_limit)
        if lowest_limit == None:
            return None
        return lowest_limit.get_top_order()

    def get_highest_buy(self):
        return self.buy_tree[0] if self.buy_len > 0 else None

    def get_highest_buy_order(self):
        lowest_limit = self.get_highest_buy()
        print("lowest_limit")
        print(lowest_limit)
        if lowest_limit == None:
            return None
        return lowest_limit.get_top_order()

    def remove_top_sell(self):
        best_sell = self.get_lowest_sell()
        print(best_sell)
        if best_sell and best_sell.get_size() > 0:
            best_sell.remove_first()
        else:
            heapq.heappop(self.sell_tree)
            self.sell_len -= 1

    def remove_top_buy(self):
        best_buy = self.get_highest_buy()
        print(best_buy)
        if best_buy and best_buy.get_size() > 0:
            best_buy.remove_first()
        else:
            heapq.heappop(self.buy_tree)
            self.buy_len -= 1

    def receive_order(self, orderObj):
        """
            Receives order from somewhere 
        """
        if orderObj.get_order_type() == OrderType.LIMIT:
            self.execute_LO(orderObj)

        def execute_LO(self,order_obj):
        print(f"buy_tree with length {self.buy_len}")
        print([x.get_limit_price() for x in self.buy_tree])
        print(f"sell_tree with length {self.sell_len}")
        print([x.get_limit_price() for x in self.sell_tree])
        if (order_obj.get_side() == Side.B):
            self.execute_LO_B(order_obj)
            return
        self.execute_LO_S(order_obj)

        # best = ""
        # curMap = None
        # get_best_func, remove_top = None, None
        # isBuy = -1 if order_obj.get_side() == Side.B else 1
        # if (isBuy == -1):
        #     curMap = self.limitBuyMap
        #     get_best_func = self.get_lowest_sell
        #     remove_top = self.remove_top_sell
        #     inc_len = self.inc_buy_len
        # else:
        #     curMap = self.limitSellMap
        #     get_best_func = self.get_highest_buy
        #     remove_top = self.remove_top_buy
        #     inc_len = self.inc_sell_len

        # best = get_best_func()
        # print("Best")
        # print(best)
        # print(f'order_obj.get_price(): {order_obj.get_price()}')
        # while(best and order_obj.get_price() > 0):
        #     # print(best.get_limit_price())
        #     best = get_best_func()
        #     price = best.get_price()
        #     qty1, qty2 = best.get_qty(),order_obj.get_qty() 
        #     sale_amt = min(qty1, qty2)
        #     print(f'price: {price}')
        #     print(f'sale_amt: {sale_amt}')
        #     self.totalSales += price * sale_amt

        #     order_obj.set_qty(qty2 - sale_amt)

        #     if sale_amt == qty1:
        #         # Can still try to find another sell order
        #         remove_top()
        #         best = get_best_func()
        #     else:
        #         best.set_qty(qty1 - sale_amt)


        # #Check if buy order is completely fulfilled
        # qty = order_obj.get_qty()
        # price = order_obj.get_price() * isBuy

        # print(f"price: {price}")
        # print(f"qty: {qty}")

        # if (qty > 0):
        #     #Not fully fulfilled, add to buy order tree
        #     thisLimit = None
        #     if (price in curMap):
        #         thisLimit = curMap[price]
        #     else:
        #         thisLimit = Limit(price)
        #         heapq.heappush(self.buy_tree, thisLimit)
        #         inc_len()
        #     thisLimit.add_order(order_obj) 

    def execute_LO_B(self,buy_obj):
        bestSell = self.get_lowest_sell_order()
        curSale = 0
        # print(f'buy_obj: {buy_obj.get_price()}')
        # if (bestSell):
        #     print(f'bestSell: {bestSell.get_price()}')
        # else:
        #     print("bestSell None")
        while(bestSell and bestSell.get_price() <= buy_obj.get_price() and buy_obj.get_qty() > 0):
            bestSell = self.get_lowest_sell_order()
            sell_price = bestSell.get_price()
            sell_qty, buy_qty= bestSell.get_qty(),buy_obj.get_qty() 
            sale_amt = min(sell_qty, buy_qty)
            # print(f'sell_qty, buy_qty: {sell_qty},{buy_qty}')
            # print(f'price: {sell_price}')
            # print(f'sale_amt: {sale_amt}')
            
            buyLeft = buy_qty - sale_amt
            sellLeft = sell_qty - sale_amt

            curSale += sell_price * sale_amt
            
            buy_obj.set_qty(buyLeft)
            if sale_amt == sell_qty and sellLeft == 0:
                # Can still try to find another sell order
                # print("Can still try to find another sell order")
                self.remove_top_sell()
                bestSell = self.get_lowest_sell_order()
            else:
                # print(f"sell_qty - sale_amt: {sell_qty - sale_amt}")
                bestSell.set_qty(sellLeft)
        
        

        #Check if buy order is completely fulfilled
        buy_qty = buy_obj.get_qty()
        buy_price = buy_obj.get_price()
        buy_id = buy_obj.get_id()

        if (buy_qty > 0):
            print("Not fully fulfilled, add to buy order tree")
            print(self.limitBuyMap)
            thisLimit = None
            if (buy_price in self.limitBuyMap):
                thisLimit = self.limitBuyMap[buy_price]
            else:
                #Wrap in function
                thisLimit = Limit(buy_price,True)
                heapq.heappush(self.buy_tree, thisLimit)
                self.limitBuyMap[buy_price] = thisLimit
                self.inc_buy_len()
            thisLimit.add_order(buy_obj) 
            self.buyOrderMap[buy_id] = buy_obj
        return curSale

        def execute_LO_S(self,sell_obj):
        bestBuy = self.get_highest_buy_order()
        curSale = 0
        # if (bestBuy):
        #     print(f'sell_obj: {sell_obj.get_price()}')
        #     print(f'bestBuy: {bestBuy.get_price()}')
        # else:
        #     print("bestBuy None")
        
        while(bestBuy and bestBuy.get_price() >= sell_obj.get_price() and sell_obj.get_qty() > 0):
            bestBuy = self.get_highest_buy_order()
            sell_price = bestBuy.get_price()
            sell_qty, buy_qty= sell_obj.get_qty() ,bestBuy.get_qty()
            sale_amt = min(sell_qty, buy_qty)
            # print(f'sell_qty, buy_qty: {sell_qty},{buy_qty}')
            # print(f'price: {sell_price}')
            # print(f'sale_amt: {sale_amt}')

            curSale += sell_price * sale_amt
            
            buyLeft = buy_qty - sale_amt
            sellLeft = sell_qty - sale_amt
            sell_obj.set_qty(sellLeft)
            sell_qty = sell_obj.get_qty()

            if sale_amt == buy_qty and buyLeft == 0:
                # Can still try to find another sell order
                self.remove_top_buy()
                bestBuy = self.get_highest_buy_order()
            else:
                bestBuy.set_qty(buyLeft)

        #Check if sell order is completely fulfilled
        sell_qty = sell_obj.get_qty()
        sell_price = sell_obj.get_price()
        sell_id = sell_obj.get_id()
        if (sell_qty > 0):
            # print("Not fully fulfilled, add to sell order tree")
            # print(self.limitSellMap)
            #Not fully fulfilled, add to buy order tree
            thisLimit = None
            if (sell_price in self.limitSellMap):
                thisLimit = self.limitSellMap[sell_price]
            else:
                thisLimit = Limit(sell_price, False)
                heapq.heappush(self.sell_tree,  thisLimit)
                self.limitSellMap[sell_price] = thisLimit
                self.inc_sell_len()
            thisLimit.add_order(sell_obj) 
            self.sellOrderMap[sell_id] = sell_obj
        return curSale


        def execute_MO_B(self,buy_obj):
        bestSell = self.get_lowest_sell_order()
        curSale = 0
        # print(f'buy_obj: {buy_obj.get_price()}, {buy_obj.get_qty()}')
        # print(bestSell)
        # if (bestSell):
        #     print(f'bestSell: {bestSell.get_price()}, {bestSell.get_qty()}')
        # else:
        #     print("bestSell None")
        while(bestSell and buy_obj.get_qty() > 0):
            bestSell = self.get_lowest_sell_order()
            sell_price = bestSell.get_price()
            sell_qty, buy_qty= bestSell.get_qty(),buy_obj.get_qty() 
            sale_amt = min(sell_qty, buy_qty)
            # print(f'sell_qty, buy_qty: {sell_qty},{buy_qty}')
            # print(f'price: {sell_price}')
            # print(f'sale_amt: {sale_amt}')
            
            buyLeft = buy_qty - sale_amt
            sellLeft = sell_qty - sale_amt

            curSale += sell_price * sale_amt
            buy_obj.set_qty(buyLeft)
            if sale_amt == sell_qty and sellLeft == 0:
                # Can still try to find another sell order
                # print("Can still try to find another sell order")
                self.remove_top_sell()
                bestSell = self.get_lowest_sell_order()
            else:
                # print(f"sell_qty - sale_amt: {sell_qty - sale_amt}")
                bestSell.set_qty(sellLeft)

        
        return curSale

            def execute_MO_S(self, sell_obj):
        bestBuy = self.get_highest_buy_order()
        curSale = 0
        while(bestBuy and sell_obj.get_qty() > 0):
            bestBuy = self.get_highest_buy_order()
            sell_price = bestBuy.get_price()
            sell_qty, buy_qty= sell_obj.get_qty() ,bestBuy.get_qty()
            sale_amt = min(sell_qty, buy_qty)
            curSale += sell_price * sale_amt

            buyLeft = buy_qty - sale_amt
            self.totalSales += sell_price * sale_amt
            sell_obj.set_qty(buyLeft)
            if sale_amt == buy_qty and buyLeft == 0:
                # Can still try to find another sell order
                self.remove_top_buy()
                bestBuy = self.get_highest_buy_order()
            else:
                bestBuy.set_qty(buyLeft)

        #Check if sell order is completely fulfilled
        sell_qty = sell_obj.get_qty()
        sell_price = sell_obj.get_price()
        return curSale

    def execute_IOC_B(self,buy_obj):
        bestSell = self.get_lowest_sell_order()
        curSale = 0
        while(bestSell and bestSell.get_price() <= buy_obj.get_price() and buy_obj.get_qty() > 0):
            bestSell = self.get_lowest_sell_order()
            sell_price = bestSell.get_price()
            sell_qty, buy_qty= bestSell.get_qty(),buy_obj.get_qty() 
            sale_amt = min(sell_qty, buy_qty)


            buyLeft = buy_qty - sale_amt
            sellLeft = sell_qty - sale_amt
            curSale += sell_price * sale_amt
            buy_obj.set_qty(buyLeft)
            if sale_amt == sell_qty and sellLeft == 0:
                # Can still try to find another sell order
                # print("Can still try to find another sell order")
                self.remove_top_sell()
                bestSell = self.get_lowest_sell_order()
            else:
                bestSell.set_qty(sellLeft)

        return curSale
            def execute_IOC_S(self,sell_obj):
        bestBuy = self.get_highest_buy_order()
        curSale = 0
        while(bestBuy and bestBuy.get_price() >= sell_obj.get_price() and sell_obj.get_qty() > 0):
            bestBuy = self.get_highest_buy_order()
            sell_price = bestBuy.get_price()
            sell_qty, buy_qty= sell_obj.get_qty() ,bestBuy.get_qty()
            sale_amt = min(sell_qty, buy_qty)
            curSale += sell_price * sale_amt

            print("This order: ", sell_price * sale_amt)

            self.totalSales += sell_price * sale_amt

            buyLeft = buy_qty - sale_amt
            sellLeft = sell_qty - sale_amt
            sell_obj.set_qty(sellLeft)
            sell_qty = sell_obj.get_qty()

            if sale_amt == buy_qty and buyLeft == 0:
                # Can still try to find another sell order
                self.remove_top_buy()
                bestBuy = self.get_highest_buy_order()
            else:
                bestBuy.set_qty(buyLeft)

        #Check if sell order is completely fulfilled
        sell_qty = sell_obj.get_qty()
        sell_price = sell_obj.get_price()
        return curSale

    def execute_FOK_B(self,buy_obj):
        #  must sort the heapq list, but using timsort isn't that bad for semi sorted list
        self.order_buy_list()
        limitIdx = 0
        orderIdx = 0
        bestSellLimit = self.sell_tree[limitIdx]
        bestSellOrder = bestSellLimit.get_top_order()
        curSale = 0
        while(bestSellOrder and bestSellOrder.get_price() <= buy_obj.get_price() and buy_obj.get_qty() > 0):
            # bestSell = bestSellLimit.
            sell_price = bestSellOrder.get_price()
            sell_qty, buy_qty= bestSellOrder.get_qty(),buy_obj.get_qty() 
            sale_amt = min(sell_qty, buy_qty)

            
            buyLeft = buy_qty - sale_amt
            sellLeft = sell_qty - sale_amt

            curSale += sell_price * sale_amt
            buy_obj.set_qty(buyLeft)
            if sale_amt == sell_qty and sellLeft == 0:
                # Can still try to find another sell order
                # self.remove_top_sell()
                bestSellOrder = bestSellOrder.get_next_order()
                orderIdx += 1
                if bestSellOrder == None:
                    limitIdx += 1
                    orderIdx = 0
                    bestSellLimit = self.sell_tree[limitIdx]
                    bestSellOrder = bestSellLimit.get_top_order()
            else:
                bestSellOrder.set_qty(sell_qty - sale_amt)
        print("Leftover quantites: ", buy_obj.get_qty())
        if buy_obj.get_qty() == 0:
            print("FILL")
            cur_limit_idx = 0
            while (cur_limit_idx < limitIdx):
                self.remove_top_buy_limit()
                cur_limit_idx += 1
            cur_order_idx = 0
            while (cur_order_idx < orderIdx):
                bestSellLimit.remove_first()
                cur_order_idx += 1
            return curSale
        print("KILL")
        return 0



    def execute_FOK_S(self,sell_obj):
        #  must sort the heapq list, but using timsort isn't that bad for semi sorted list
        print(self.buy_tree)

        self.order_buy_list()
        limitIdx = 0
        orderIdx = 0
        bestBuyLimit = self.buy_tree[limitIdx]
        bestBuyOrder = bestBuyLimit.get_top_order()
        curSale = 0
        print("Start quantites: ", sell_obj.get_qty())
        print(f"Best Limit: {bestBuyLimit.get_size()} , {bestBuyLimit.get_limit_price()}")
        print("Best Order: ", bestBuyOrder.get_qty())
        while(bestBuyOrder and bestBuyOrder.get_price() >= sell_obj.get_price() and sell_obj.get_qty() > 0):
            # bestSell = bestSellLimit.
            buy_price = bestBuyOrder.get_price()
            sell_qty, buy_qty= sell_obj.get_qty(), bestBuyOrder.get_qty() 
            sale_amt = min(sell_qty, buy_qty)
            curSale += buy_price * sale_amt

            buyLeft = buy_qty - sale_amt
            sellLeft = sell_qty - sale_amt

            print(f"buyLeft: {buyLeft}")
            print(f"sellLeft: {sellLeft}")

            sell_obj.set_qty(sellLeft)
            if sale_amt == buy_qty and buyLeft == 0:
                # Can still try to find another sell order
                # self.remove_top_sell()
                bestBuyOrder = bestBuyOrder.get_next_order()
                orderIdx += 1
                if bestBuyOrder == None:
                    limitIdx += 1
                    orderIdx = 0
                    bestBuyLimit = self.buy_tree[limitIdx] if limitIdx < self.get_buy_len() else None
                    bestBuyOrder = bestBuyLimit.get_top_order()
            else:
                bestBuyOrder.set_qty(buyLeft)
                
            print(f"limitIdx: {limitIdx}")
            print(f"orderIdx: {orderIdx}")

        print("Leftover quantites: ", sell_obj.get_qty())
        print(f"limitIdx: {limitIdx}")
        print(f"orderIdx: {orderIdx}")
        if sell_obj.get_qty() == 0:
            print("FILL")
            cur_limit_idx = 0
            while (cur_limit_idx < limitIdx):
                self.remove_top_buy_limit()
                print(self.buy_tree)
                cur_limit_idx += 1
            cur_order_idx = 0
            while (cur_order_idx < orderIdx):
                bestBuyLimit.remove_first()
                cur_order_idx += 1
            return curSale
        
        print("KILL")
        return 0

