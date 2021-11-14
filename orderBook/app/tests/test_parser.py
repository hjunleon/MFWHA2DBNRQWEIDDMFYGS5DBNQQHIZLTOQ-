import pytest
import sys
# print(sys.path)
from order_book.orders import *
from order_book.input_parser import parseAlphaFormat

print(sys.path)


@pytest.mark.parametrize("test_input,expected", [
    ("SUB LO B Ffuj 200 13", {
        "isOrder": True,
        "id": "Ffuj",
        "price": 13,
        "qty": 200,
        "isBuy":True,
        "orderType": OrderType.LIMIT
    }), ("SUB LO B Yy7P 150 11", {
        "isOrder": True,
        "id": "Yy7P",
        "price": 11,
        "qty": 150,
        "isBuy":True,
        "orderType": OrderType.LIMIT
    }), ("SUB LO B YuFU 100 13", {
        "isOrder": True,
        "id": "YuFU",
        "price": 13,
        "qty": 100,
        "isBuy":True,
        "orderType": OrderType.LIMIT
    }), ("SUB LO S IpD8 150 14", {
        "isOrder": True,
        "id": "IpD8",
        "price": 14,
        "qty": 150,
        "isBuy":False,
        "orderType": OrderType.LIMIT
    }),("SUB LO S y93N 190 15",{
        "isOrder": True,
        "id": "y93N",
        "price": 15,
        "qty": 190,
        "isBuy":False,
        "orderType": OrderType.LIMIT
    }),("SUB LO B Y5wb 230 14",{
        "isOrder": True,
        "id": "Y5wb",
        "price": 14,
        "qty": 230,
        "isBuy":True,
        "orderType": OrderType.LIMIT
    }), ("SUB MO B IZLO 250",{
        "isOrder": True,
        "id": "IZLO",
        # "price": 14,
        "qty": 250,
        "isBuy":True,
        "orderType": OrderType.MARKET
    }), ("CXL Ffuj",{
        "isOrder": False,
        "id": "Ffuj",
        "actionType":ActionType.CXL
    }), ("CXL 49Ze",{
        "isOrder": False,
        "id": "49Ze",
        "actionType": ActionType.CXL
    }), ("CRP 9zS1 170 11", {
        "isOrder": False,
        "id": "9zS1",
        "actionType": ActionType.CRP
    }), ("SUB IOC S ckMR 150 10", {
        "isOrder": True,
        "id": "ckMR",
        "price": 10,
        "qty": 150,
        "isBuy":False,
        "orderType": OrderType.IOC
    }), ("SUB FOK S 8uGs 200 9", {
        "isOrder": True,
        "id": "8uGs",
        "price": 9,
        "qty": 200,
        "isBuy":False,
        "orderType": OrderType.FOK
    }), ("SUB ICE B Rcjr 350 12 100", {
        "isOrder": True,
        "id": "Rcjr",
        "price": 12,
        "qty": 350,
        "display_qty": 100,
        "isBuy":True,
        "orderType": OrderType.ICE
    })       
])
def test_alpha_parser(test_input, expected):
    isOrder, retObj = parseAlphaFormat(test_input)
    assert isOrder == expected["isOrder"]
    if (isOrder == False):
        assert retObj.get_order_id() == expected["id"]
        assert retObj.get_action_type() == expected["actionType"]
    else:
        assert retObj.get_id() == expected["id"]
        assert retObj.get_order_type() == expected["orderType"]
    
    # print(expected["orderType"] == retObj.get_order_type())
    
    if "isBuy" in expected:
        isBuy = Side.B if expected["isBuy"] else Side.S 
        assert retObj.get_side() == isBuy

    if "price" in expected:
        assert retObj.get_price() == expected["price"]
    if "qty" in expected:
        assert retObj.get_qty() == expected["qty"]
    if "display_qty" in expected:
        assert retObj.get_display_qty() == expected["display_qty"]


if __name__ == '__main__':
    print(sys.path)
