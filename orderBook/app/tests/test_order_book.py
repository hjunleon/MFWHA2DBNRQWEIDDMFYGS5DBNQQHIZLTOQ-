import pytest
import sys
import os

sys.path.append(os.path.dirname(sys.path[0]))
# print(sys.path)
from order_book.book import *
from order_book.input_parser import parseAlphaFormat
from order_book.output_formatter import outputAlpha

# """
# Checks if book has the correct buy orders, sell orders, and total cost of unit stock 
# that was traded during the execution of the order

# """

test_case1 = [
    (
        [
            "SUB LO B Ffuj 200 13",
            "SUB LO B Yy7P 150 11",
            "SUB LO B YuFU 100 13",
            "SUB LO S IpD8 150 14",
            "SUB LO S y93N 190 15",
            "SUB LO B Y5wb 230 14",
            "SUB MO B IZLO 250",
            "CXL Ffuj",
            "CXL 49Ze",
            "END"
        ],
        {
            "buy": [
                {
                    "qty": 80,
                    "price": 14,
                    "id": "Y5wb"
                },
                {
                    "qty": 100,
                    "price": 13,
                    "id": "YuFU"
                },
                {
                    "qty": 150,
                    "price": 11,
                    "id": "Yy7P"
                }
            ],
            "sell":[]
        }
    ),
    (
        [
            "SUB LO B N1Eh 300 12",
            "SUB LO B 0Gxb 250 11",
            "SUB LO S JSvU 350 14",
            "SUB LO S uH6w 320 15",
            "SUB IOC S ckMR 150 10",
            "SUB IOC B DVeP 500 14",
            "SUB FOK S ejnR 200 12",
            "SUB FOK S 8uGs 200 9",
            "SUB LO B 2va9 250 12",
            "SUB LO B 9zS1 300 11",
            "CRP 2va9 480 11",
            "CRP 9zS1 170 11",
            "END"
        ],
        {
            "buy": [
                {
                    "qty": 200,
                    "price": 11,
                    "id": "0Gxb"
                },
                {
                    "qty": 170,
                    "price": 11,
                    "id": "9zS1"
                },
                {
                    "qty": 480,
                    "price": 11,
                    "id": "2va9"
                }
            ],
            "sell":[
                {
                    "qty": 320,
                    "price": 15,
                    "id": "uH6w"
                }
            ]
        }
    )
]


"""
{
            "buy":{ 
                "Y5wb":{
                    "qty": 80,
                    "price": 14,
                },
                "YuFU":{
                    "qty": 100,
                    "price": 13,
                },
                "Yy7P":{
                    "qty": 150,
                    "price": 11
                }
            },
            "sell":[]
        }

"""

@pytest.mark.parametrize("test_input,expected", test_case1)
@pytest.mark.timeout(0.1)
def test_book_final(test_input, expected):
    print("test_input length: ", len(test_input))
    book = Book()
    for i in range(len(test_input) - 1):
        cur_test = test_input[i]
        isOrder, retObj = parseAlphaFormat(cur_test)
        if isOrder:
            book.receive_order(retObj)
        else:
            book.receive_action(retObj)

        buyList = book.get_buy_orders()
        sellList = book.get_sell_orders()

        print("buyList")
        print("sellList")

        print([f"{x.get_qty()} {x.get_price()} {x.get_id()}" for x in buyList])
        print([f"{x.get_qty()} {x.get_price()} {x.get_id()}" for x in sellList])
    buyExpected = expected["buy"]
    sellExpected = expected["sell"]
    


    for idx, order in enumerate(buyList):
        curExpected = buyExpected[idx]
        assert order.get_qty() == curExpected["qty"]
        assert order.get_price() == curExpected["price"]
        assert order.get_id() == curExpected["id"]
    
    for idx, order in enumerate(sellList):
        curExpected = sellExpected[idx]
        assert order.get_qty() == curExpected["qty"]
        assert order.get_price() == curExpected["price"]
        assert order.get_id() == curExpected["id"]


    print("END")

test_cases_output = [
    (
        [
            "SUB LO B Ffuj 200 13",
            "SUB LO B Yy7P 150 11",
            "SUB LO B YuFU 100 13",
            "SUB LO S IpD8 150 14",
            "SUB LO S y93N 190 15",
            "SUB LO B Y5wb 230 14",
            "SUB MO B IZLO 250",
            "CXL Ffuj",
            "CXL 49Ze",
            "END"
        ],
        {
            "inBetween": [0,0,0,0,0,2100,2850],
            "buy": "B: 80@14#Y5wb 100@13#YuFU 150@11#Yy7P",
            "sell":"S:"
        }
    ),
    (
        [
            "SUB LO B N1Eh 300 12",
            "SUB LO B 0Gxb 250 11",
            "SUB LO S JSvU 350 14",
            "SUB LO S uH6w 320 15",
            "SUB IOC S ckMR 150 10",
            "SUB IOC B DVeP 500 14",
            "SUB FOK S ejnR 200 12",
            "SUB FOK S 8uGs 200 9",
            "SUB LO B 2va9 250 12",
            "SUB LO B 9zS1 300 11",
            "CRP 2va9 480 11",
            "CRP 9zS1 170 11",
            "END"
        ],
        {
            "inBetween": [0,0,0,0,1800,4900,0,2350,0,0,0,0],
            "buy": "B: 200@11#0Gxb 170@11#9zS1 480@11#2va9",
            "sell":"S: 320@15#uH6w"
        }
    ),(
        [
            "SUB LO B c9Xt 200 10",
            "SUB MO B ESSq 300",
            "CXL i9Ze",
            "SUB LO S Zfjg 300 13",
            "SUB LO S p7kU 250 13",
            "SUB LO S rrjX 700 13",
            "SUB LO S W8DN 400 13",
            "CXL p7kU",
            "SUB MO B Q9DZ 1270",
            "END"
        ],
        {
            "inBetween":[0,0,0,0,0,0,16510],
            "buy": "B: 200@10#c9Xt",
            "sell": "S: 130@13#W8DN"
        }
    ),(
        [
            "SUB ICE B Rcjr 350 12 100",
            "SUB LO B 1FZU 70 12",
            "SUB ICE B qfZL 420 12 100",
            "SUB LO S NsSd 200 15",
            "SUB ICE B SKJl 150 17 90",
            "SUB LO S 5Rey 120 10",
            "SUB LO S mYZz 500 10",
            "END"
        ],
        {
            "inBetween":[0,0,0,0,2250,1440,6000],
            "buy": "B: 50(170)@12#qfZL 50(50)@12#Rcjr",
            "sell": "S: 50@15#NsSd"
        }
    ),(
        [
            "SUB LO B Ffuj 200 13",
            "SUB LO B Yy7P 150 11",
            "SUB LO B YuFU 100 13",
            "SUB LO S IpD8 150 14",
            "SUB LO S y93N 190 15",
            "SUB LO B Y5wb 230 14",
            "SUB MO B IZLO 250",
            "SUB IOC S Fwe5 200 14",
            "SUB FOK S IUKu 320 12",
            "SUB ICE S TqAv 480 12 100",
            "SUB LO S OQfS 120 12",
            "SUB LO B MNa6 130 13",
            "SUB LO B fzya 200 10",
            "SUB LO B LvQH 240 10",
            "CRP OQfS 50 12",
            "CRP Yy7P 150 10",
            "CXL LvQH",
            "END"
        ],
        {
            "inBetween":[0,0,0,0,0,2100,2850,1120,0,3900,0,1560,0,0],
            "buy": "B: 200@10#fzya 150@10#Yy7P",
            "sell": "S: 50@12#OQfS 80(80)@12#TqAv"
        }
    ),(
        [
            "SUB LO B cG0u 300 12",
            "SUB LO B prdL 250 11",
            "SUB LO S x7sH 350 14",
            "SUB LO S NvA1 320 15",
            "SUB IOC B iKdd 500 14",
            "SUB FOK S A2ei 200 12",
            "SUB MO B 68YU 900",
            "CXL 29Zk",
            "CRP cG0u 300 14",
            "END"
        ],
        {
            "inBetween":[0,0,0,0,4900,2400,4800],
            "buy": "B: 300@14#cG0u 250@11#prdL",
            "sell": "S:"
        }
    )
]


@pytest.mark.parametrize("test_input,expected", test_cases_output)
@pytest.mark.timeout(0.1) #0.1
def test_book_output(test_input, expected):
    print("test_input length: ", len(test_input))
    book = Book()
    stateIdx = 0
    states = expected["inBetween"]
    
    for i in range(len(test_input) - 1):
        cur_test = test_input[i]
        isOrder, retObj = parseAlphaFormat(cur_test)
        if isOrder:
            book.receive_order(retObj)
            curState = book.get_latest_sales_state()
            assert(states[stateIdx] == curState)
            stateIdx += 1
        else:
            book.receive_action(retObj)

        # buyList = book.get_buy_orders()
        # sellList = book.get_sell_orders()

        # print("buyList")
        # print("sellList")

        # print([f"{x.get_id()} {x.get_qty()} {x.get_price()} {x.get_display_qty()}" for x in buyList])
        # print([f"{x.get_id()} {x.get_qty()} {x.get_price()} {x.get_display_qty()}" for x in sellList])
    buyExpected = expected["buy"]
    sellExpected = expected["sell"]
    buyList = book.get_buy_orders()
    sellList = book.get_sell_orders()

    buyOutput = outputAlpha(buyList, True)
    sellOutput = outputAlpha(sellList, False)
    print(buyOutput)
    print(sellOutput)
    assert(buyOutput == buyExpected)
    assert(sellOutput == sellExpected)
    print("END")


# @pytest.mark.parametrize("test_input,expected", [
#     ("SUB LO B Ffuj 200 13",{
#         # "buy": [
#         #     {
#         #         "qty": 200,
#         #         "price": 13,
#         #         "id": "Ffuj"
#         #     }
#         # ],
#         # "sell":[],
#         "total_sales": 0
#     }),("SUB LO B Yy7P 150 11",{
#         # "buy": [
#         #     {
#         #         "qty": 200,
#         #         "price": 13,
#         #         "id": "Ffuj"
#         #     },
#         #     {
#         #         "qty": 100,
#         #         "price": 13,
#         #         "id": "Yy7P"
#         #     },
#         #     {
#         #         "qty": 150,
#         #         "price": 11,
#         #         "id": "Yy7P"
#         #     }
#         # ],
#         # "sell":[],
#         "total_sales": 0
#     }),("SUB LO B YuFU 100 13",{
#         "total_sales": 0
#     }),("SUB LO S IpD8 150 14",{

#     }),("SUB LO S y93N 190 15",{

#     }),("SUB LO B Y5wb 230 14",{

#     }),("SUB MO B IZLO 250",{

#     }),("CXL Ffuj",{

#     }),("CXL 49Ze",{

#     }),("END",{

#     })
    
# ])

test_case2 = [
    (
        [
            "SUB LO B Ffuj 200 13",
            "SUB LO B Yy7P 150 11",
            "SUB LO B YuFU 100 13",
            "SUB LO S IpD8 150 14",
            "SUB LO S y93N 190 15",
            "SUB LO B Y5wb 230 14",
            "SUB MO B IZLO 250",
            "CXL Ffuj",
            "CXL 49Ze",
            "END"
        ],
        [
            0,0,0,0,0,2100,2850,0,0
        ]
    ),
    (
        [
            "SUB LO B N1Eh 300 12",
            "SUB LO B 0Gxb 250 11",
            "SUB LO S JSvU 350 14",
            "SUB LO S uH6w 320 15",
            "SUB IOC S ckMR 150 10",
            "SUB IOC B DVeP 500 14",
            "SUB FOK S ejnR 200 12",
            "SUB FOK S 8uGs 200 9",
            "SUB LO B 2va9 250 12",
            "SUB LO B 9zS1 300 11",
            "CRP 2va9 480 11",
            "CRP 9zS1 170 11",
            "END"
        ],
        [
            0,0,0,0,1800,4900,0,2350,0,0,0,0
        ]
    ),
    (
        [
            "SUB LO B N1Eh 100 12",
            "SUB LO B ff1Eh 200 12",
            "SUB LO B v1qh 400 10",
            "SUB LO B 0Gxb 250 11",
            "SUB LO S JSvU 350 14",
            "SUB LO S uH6w 320 15",
            "CXL v1qh",
            "SUB IOC S ckMR 150 10",
            "SUB IOC B DVeP 500 14",
            "SUB IOC S cxVP 100 11",
            "SUB FOK B exXR 203 19",
            "SUB FOK S ejnR 200 12",
            "CXL ejnR",
            "SUB FOK S 8uGs 200 9",
            "SUB LO B 2va9 250 12",
            "SUB LO B 9zS1 300 11",
            "CRP 2va9 480 11",
            "CRP 9zS1 170 11",
            "END"
        ],
        [
            0,0,0,0,0,0,1800,4900,1200,3045,0,2250,0,0,0
        ]
    ),
    (
        [
            "SUB LO B N1Eh 100 12",
            "SUB LO B ff1Eh 200 12",
            "SUB LO B v1qh 400 10",
            "SUB LO B 0Gxb 250 11",
            "SUB LO S JSvU 350 14",
            "SUB LO S uH6w 320 15",
            "CXL v1qh",
            "SUB LO S GffA 50 11",
            "SUB LO S GffB 50 11",
            "SUB LO S GffC 50 11",
            "SUB LO S GffD 50 11",
            "SUB LO S GffE 50 11",
            "SUB LO S ffhs 200 12",
            "SUB LO B wyTs 400 16",
            "SUB LO B F5#d 150 15",
            "SUB LO S wgko 350 14",
            "SUB LO S mmb7 320 15",
            "SUB IOC S ckMR 150 10",
            "SUB IOC B DVeP 500 14",
            "SUB IOC S cxVP 100 11",
            "SUB FOK B exXR 203 19",
            "SUB FOK S ejnR 200 12",
            "CXL ejnR",
            "SUB FOK S 8uGs 200 9",
            "SUB LO B 2va9 250 12",
            "SUB LO B 9zS1 300 11",
            "CRP 2va9 480 11",
            "CRP 9zS1 170 11",
            "END"
        ],
        [
            0,0,0,0,0,0,600,600,600,600,600,600,5300,2150,0,0,1650,4900,1100,3045,0,0,0,0
        ]
    )
]

@pytest.mark.parametrize("test_input,expected", test_case2)
@pytest.mark.timeout(0.1)
def test_book_intermediate_states(test_input, expected):
    print("Expected length: ", len(expected))
    print("test_input length: ", len(test_input))
    book = Book()
    stateIdx = 0
    for i in range(len(test_input) - 1):
        cur_test = test_input[i]
        print(cur_test)
        isOrder, retObj = parseAlphaFormat(cur_test)
        if isOrder:
            book.receive_order(retObj)
            curState = book.get_latest_sales_state()
            print(f"curState: {curState}", "=" * 40)
            assert(expected[stateIdx] == curState)
            stateIdx += 1
        else:
            book.receive_action(retObj)

        buyList = book.get_buy_orders()
        sellList = book.get_sell_orders()
        
        print([f"{x.get_id()} {x.get_qty()} {x.get_price()}" for x in buyList])
        print([f"{x.get_id()} {x.get_qty()} {x.get_price()}" for x in sellList])
    print("END")

if __name__ == '__main__':
    test_book_intermediate_states(*(test_case2[3]))
    # test_book_final(*(test_case1[0]))
