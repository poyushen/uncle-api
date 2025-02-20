from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    ID: str
    姓名: str | None = None
    性別: str | None = None
    生日: datetime | None = None
    職級: str | None = None
    電話: str | None = None
    手機: str | None = None
    郵遞區號: str | None = None
    地址: str | None = None
    EMAIL: str | None = None
    備註: str | None = None
    佣金比率A: float | None = None
    佣金比率B: float | None = None
    信用額度: float | None = None
    介紹人: str | None = None
    介紹人佣金比率A: float | None = None
    介紹人佣金比率B: float | None = None
    公司佣金比率B: float | None = None
    公司借支佣金率C: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ID": "-1234",
                    "姓名": "王小明",
                    "性別": "男",
                    "生日": "2025-02-17T14:43:22",
                    "職級": None,
                    "電話": None,
                    "手機": None,
                    "郵遞區號": None,
                    "地址": None,
                    "EMAIL": None,
                    "備註": None,
                    "佣金比率A": 1.0,
                    "佣金比率B": None,
                    "信用額度": None,
                    "介紹人": "小沈",
                    "介紹人佣金比率A": None,
                    "介紹人佣金比率B": None,
                    "公司佣金比率B": None,
                    "公司借支佣金率C": None,
                }
            ]
        }
    }


class Group(BaseModel):
    出團日期: datetime
    貨幣1: str | None = None
    匯率1: float | None = None
    貨幣2: str | None = None
    匯率2: float | None = None
    貨幣3: str | None = None
    匯率3: float | None = None
    貨幣4: str | None = None
    匯率4: float | None = None
    貨幣5: str | None = None
    匯率5: float | None = None
    貨幣6: str | None = None
    匯率6: float | None = None
    貨幣7: str | None = None
    匯率7: float | None = None
    貨幣8: str | None = None
    匯率8: float | None = None
    盤房領回主貨幣: float | None = None
    主貨幣現金單: float | None = None
    盤房領回台幣: float | None = None
    台幣現金單: float | None = None
    地點: str | None = None
    損_公司總入金: float | None = None
    損_換算主貨幣: float | None = None
    損_總洗碼: float | None = None
    損_總回碼: float | None = None
    損_淨洗碼: float | None = None
    損_公司退佣: float | None = None
    損_出差費1: float | None = None
    損_出差費1_人數: int | None = None
    損_出差費2: float | None = None
    損_出差費2_人數: int | None = None
    損_出差費3: float | None = None
    損_出差費3_人數: int | None = None
    損_港務費: float | None = None
    損_港務費_人數: int | None = None
    損_其他支出費用_台幣: float | None = None
    損_其他支出費用_主貨幣: float | None = None
    團隊領款單_應領帳戶餘額: str | None = None
    團隊領款單_應領退佣: str | None = None
    團隊領款單_其他: str | None = None
    團隊領款單_應付款項: str | None = None
    團隊領款單_應領總金額: str | None = None
    團隊領款單_港幣金額: str | None = None
    團隊領款單_台幣金額: str | None = None
    團隊領款單_台支金額: str | None = None
    團隊領款單_外幣: str | None = None
    團隊領款單_外幣金額: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "出團日期": "2010-05-07T00:00:00",
                    "貨幣1": "港幣",
                    "匯率1": 1,
                    "貨幣2": "新台幣",
                    "匯率2": 0.2396,
                    "貨幣3": "台支",
                    "匯率3": 0.2396,
                    "貨幣4": None,
                    "匯率4": None,
                    "貨幣5": None,
                    "匯率5": None,
                    "貨幣6": None,
                    "匯率6": None,
                    "貨幣7": None,
                    "匯率7": None,
                    "貨幣8": None,
                    "匯率8": None,
                    "盤房領回主貨幣": None,
                    "主貨幣現金單": None,
                    "盤房領回台幣": None,
                    "台幣現金單": None,
                    "地點": "麗星郵輪",
                    "損_公司總入金": None,
                    "損_換算主貨幣": None,
                    "損_總洗碼": None,
                    "損_總回碼": None,
                    "損_淨洗碼": None,
                    "損_公司退佣": None,
                    "損_出差費1": None,
                    "損_出差費1_人數": None,
                    "損_出差費2": None,
                    "損_出差費2_人數": None,
                    "損_出差費3": None,
                    "損_出差費3_人數": None,
                    "損_港務費": None,
                    "損_港務費_人數": None,
                    "損_其他支出費用_台幣": None,
                    "損_其他支出費用_主貨幣": None,
                    "團隊領款單_應領帳戶餘額": None,
                    "團隊領款單_應領退佣": None,
                    "團隊領款單_其他": None,
                    "團隊領款單_應付款項": None,
                    "團隊領款單_應領總金額": None,
                    "團隊領款單_港幣金額": None,
                    "團隊領款單_台幣金額": None,
                    "團隊領款單_台支金額": None,
                    "團隊領款單_外幣": None,
                    "團隊領款單_外幣金額": None,
                },
            ]
        }
    }


class Location(BaseModel):
    地點: str

    model_config = {"json_schema_extra": {"examples": [{"地點": "台南"}]}}


class Currency(BaseModel):
    貨幣名稱: str
    貨幣代碼: str | None = None
    預設匯率: float | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [{"貨幣名稱": "新台幣", "貨幣代碼": None, "預設匯率": None}]
        }
    }


class GroupUser(BaseModel):
    客戶ID: str
    出團日期: datetime
    姓名: str | None = None
    備註: str | None = None
    佣金比率A: float | None = None
    佣金比率B: float | None = None
    介紹人: str | None = None
    介紹人佣金比率A: float | None = None
    介紹人佣金比率B: float | None = None
    公司佣金比率B: float | None = None
    公司借支佣金率C: float | None = None
    貨幣1_數量: float | None = None
    貨幣1: float | None = None
    貨幣2_數量: float | None = None
    貨幣2: float | None = None
    貨幣3_數量: float | None = None
    貨幣3: float | None = None
    貨幣4_數量: float | None = None
    貨幣4: float | None = None
    貨幣5_數量: float | None = None
    貨幣5: float | None = None
    貨幣6_數量: float | None = None
    貨幣6: float | None = None
    貨幣7_數量: float | None = None
    貨幣7: float | None = None
    貨幣8_數量: float | None = None
    貨幣8: float | None = None
    入金總額: float | None = None
    帳面餘額: float | None = None
    洗碼數B: float | None = None
    洗碼數A: float | None = None
    淨洗碼數A: float | None = None
    淨洗碼數B: float | None = None
    淨洗碼數: float | None = None
    佣金: float | None = None
    客應付款項: float | None = None
    其他: float | None = None
    客應領付總金額: float | None = None
    領款金額_貨幣1: float | None = None
    領款金額_貨幣2: float | None = None
    領款金額_貨幣3: float | None = None
    領款金額_貨幣4: float | None = None
    領款金額_貨幣5: float | None = None
    領款金額_貨幣6: float | None = None
    領款金額_貨幣7: float | None = None
    領款金額_貨幣8: float | None = None
    領款金額_其他: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "客戶ID": "0001",
                    "出團日期": "2025-02-20T00:00:00",
                    "姓名": "王小明",
                    "備註": None,
                    "佣金比率A": None,
                    "佣金比率B": None,
                    "介紹人": None,
                    "介紹人佣金比率A": None,
                    "介紹人佣金比率B": None,
                    "公司佣金比率B": None,
                    "公司借支佣金率C": None,
                    "貨幣1_數量": None,
                    "貨幣1": None,
                    "貨幣2_數量": None,
                    "貨幣2": None,
                    "貨幣3_數量": None,
                    "貨幣3": None,
                    "貨幣4_數量": None,
                    "貨幣4": None,
                    "貨幣5_數量": None,
                    "貨幣5": None,
                    "貨幣6_數量": None,
                    "貨幣6": None,
                    "貨幣7_數量": None,
                    "貨幣7": None,
                    "貨幣8_數量": None,
                    "貨幣8": None,
                    "入金總額": None,
                    "賬面餘額": None,
                    "洗碼數B": None,
                    "洗碼數A": None,
                    "淨洗碼數A": None,
                    "淨洗碼數B": None,
                    "淨洗碼數": None,
                    "佣金": None,
                    "客應付款項": None,
                    "其他": None,
                    "客應領付總金額": None,
                    "領款金額_貨幣1": None,
                    "領款金額_貨幣2": None,
                    "領款金額_貨幣3": None,
                    "領款金額_貨幣4": None,
                    "領款金額_貨幣5": None,
                    "領款金額_貨幣6": None,
                    "領款金額_貨幣7": None,
                    "領款金額_貨幣8": None,
                    "領款金額_其他": None,
                }
            ]
        }
    }
