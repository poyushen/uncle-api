import json
from datetime import datetime
from typing import List

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from db import fetch_data, insert_data, exec_table
from schema import User, Group, Location, Currency, GroupUser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=["*"],
)

NUM_COLS = json.load(open("./num_cols.json", "r"))


@app.get("/users/", tags=["user"])
def get_users() -> List[User]:
    """
    Get all users in T_客戶
    """

    sql = "SELECT * FROM PRAISE.dbo.T_客戶"
    df = fetch_data(sql)
    if df is None:
        raise HTTPException(status_code=404, detail="No User in DB.")

    output = []
    for i in df.index:
        output.append({k: df[k].iloc[i] for k in User.__fields__.keys()})

    return output


@app.get("/user/", tags=["user"])
def get_user_by_id(user_id: str) -> User:
    """
    Get user with [user_id] in T_客戶
    """

    sql = f"SELECT * FROM PRAISE.dbo.T_客戶 WHERE ID = '{user_id}'"
    df = fetch_data(sql)
    if df is None:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} not found."
        )

    output = {k: df[k].iloc[0] for k in User.__fields__.keys()}

    return output


@app.post("/user/", tags=["user"])
def create_user(user: User):
    """
    Create new user in T_客戶
    """

    user_id = user.__dict__["ID"]
    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_客戶 WHERE ID = '{user_id}'"
    df = fetch_data(fetch_sql)
    if df is not None:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} already exists."
        )

    cols = list(User.__fields__.keys())
    types = ",".join(["%d" if col in NUM_COLS["T_客戶"] else "%s" for col in cols])
    sql = f"""
        INSERT INTO PRAISE.dbo.T_客戶 ({", ".join(cols)}, add_time, add_user_id, update_time, update_user_id)
        values ({types}, %s, %d, %s, %d)
    """

    data = [user.__dict__[k] for k in User.__fields__.keys()]
    data.extend([datetime.now(), 6, datetime.now(), 6])

    insert_data(sql, data)


@app.delete("/user/", tags=["user"])
def delete_user(user_id: str):
    """
    Delete user with [user_id] in T_客戶
    """

    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_客戶 WHERE ID = '{user_id}'"
    df = fetch_data(fetch_sql)
    if df is None:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} not found."
        )

    sql = f"DELETE FROM PRAISE.dbo.T_客戶 WHERE ID = '{user_id}'"

    exec_table(sql)


@app.put("/user/", tags=["user"])
def update_user(user_id: str, user: User):
    """
    Update user with [user_id] in T_客戶
    """

    if user_id != user.__dict__["ID"]:
        raise HTTPException(
            status_code=404,
            detail=f"User ID {user_id} and {user.__dict__['ID']} not matched.",
        )

    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_客戶 WHERE ID = '{user_id}'"
    df = fetch_data(fetch_sql)
    if df is None:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} not found."
        )

    infos = []
    for k, v in user.__dict__.items():
        if v is None:
            infos.append(f"{k} = NULL")
        elif k in NUM_COLS["T_客戶"]:
            infos.append(f"{k} = {v}")
        else:
            infos.append(f"{k} = N'{v}'")

    sql = f"""
        UPDATE PRAISE.dbo.T_客戶
        SET {', '.join(infos)}, update_time = '{datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')}'
        WHERE ID = '{user_id}'
    """

    exec_table(sql)


@app.get("/groups/", tags=["group"])
def get_groups() -> List[Group]:
    """
    Get all groups in T_旅行團
    """

    sql = "SELECT * FROM PRAISE.dbo.T_旅行團"
    df = fetch_data(sql)
    if df is None:
        raise HTTPException(status_code=404, detail="No Group in DB.")

    sql2 = "SELECT 出團日期, COUNT(客戶ID) AS 客戶總數 FROM PRAISE.dbo.T_旅行團客戶 GROUP BY 出團日期"
    df2 = fetch_data(sql2)

    merged_df = pd.merge(df, df2, on="出團日期", how="left")
    merged_df["客戶總數"] = merged_df["客戶總數"].fillna(0)

    output = []
    for i in merged_df.index:
        output.append({k: merged_df[k].iloc[i] for k in Group.__fields__.keys()})

    return output


@app.get("/group/", tags=["group"])
def get_group_by_date(group_date: str) -> Group:
    """
    Get group with [group date] in T_旅行團

    param group_date: "YYYY-MM-DD"
    """

    sql = f"SELECT * FROM PRAISE.dbo.T_旅行團 WHERE 出團日期 = '{group_date}'"
    df = fetch_data(sql)
    if df is None:
        raise HTTPException(
            status_code=404, detail=f"Group with date {group_date} not found."
        )

    sql2 = f"SELECT 出團日期, COUNT(客戶ID) AS 客戶總數 FROM PRAISE.dbo.T_旅行團客戶 WHERE 出團日期 = '{group_date}' GROUP BY 出團日期"
    df2 = fetch_data(sql2)

    if df2 is None:
        merged_df = df
        df["客戶總數"] = 0
    else:
        merged_df = pd.merge(df, df2, on="出團日期")

    output = {k: merged_df[k].iloc[0] for k in Group.__fields__.keys()}

    return output


@app.post("/group/", tags=["group"])
def create_group(group: Group):
    """
    Create new group in T_旅行團
    """

    group_date = group.__dict__["出團日期"]
    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_旅行團 WHERE 出團日期 = '{group_date}'"
    df = fetch_data(fetch_sql)
    if df is not None:
        raise HTTPException(
            status_code=404, detail=f"Group with date {group_date} already exists."
        )

    cols = list(Group.__fields__.keys())
    cols = [col for col in cols if col not in ["update_time", "客戶總數"]]
    types = ",".join(["%d" if col in NUM_COLS["T_旅行團"] else "%s" for col in cols])
    sql = f"""
        INSERT INTO PRAISE.dbo.T_旅行團 ({", ".join(cols)}, add_time, add_user_id, update_time, update_user_id)
        values ({types}, %s, %d, %s, %d)
    """

    data = [group.__dict__[k] for k in Group.__fields__.keys()]
    data.extend([datetime.now(), 6, datetime.now(), 6])

    insert_data(sql, data)


@app.delete("/group/", tags=["group"])
def delete_group(group_date: str):
    """
    Delete group with [group_date] in T_旅行團

    param group_date: "YYYY-MM-DD"
    """

    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_旅行團 WHERE 出團日期 = '{group_date}'"
    df = fetch_data(fetch_sql)
    if df is None:
        raise HTTPException(
            status_code=404, detail=f"Group with date {group_date} not found."
        )

    sql = f"DELETE FROM PRAISE.dbo.T_旅行團 WHERE 出團日期 = '{group_date}'"

    exec_table(sql)


@app.put("/group/", tags=["group"])
def update_group(group_date: str, group: Group):
    """
    Update group with [group_date] in T_旅行團

    param group_date: "YYYY-MM-DD"
    """

    body_date = datetime.strftime(group.__dict__["出團日期"], "%Y-%m-%d")
    print(group_date, body_date, group_date == body_date)

    if group_date != body_date:
        raise HTTPException(
            status_code=404,
            detail=f"Group date {group_date} and {body_date} not matched.",
        )

    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_旅行團 WHERE 出團日期 = '{group_date}'"
    df = fetch_data(fetch_sql)
    if df is None:
        raise HTTPException(
            status_code=404, detail=f"Group with date {group_date} not found."
        )

    infos = []
    for k, v in group.__dict__.items():
        if k in ["update_time", "客戶總數"]:
            continue
        if v is None:
            infos.append(f"{k} = NULL")
        elif k in NUM_COLS["T_旅行團"]:
            infos.append(f"{k} = {v}")
        else:
            infos.append(f"{k} = N'{v}'")

    sql = f"""
        UPDATE PRAISE.dbo.T_旅行團
        SET {', '.join(infos)}, update_time = '{datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')}'
        WHERE 出團日期 = '{group_date}'
    """

    exec_table(sql)


@app.get("/locations/", tags=["location"])
def get_locations() -> list:
    """
    Get all locations in T_地點
    """

    sql = "SELECT * FROM PRAISE.dbo.T_地點"
    df = fetch_data(sql)

    if df is None:
        raise HTTPException(status_code=404, detail="No Location in DB.")

    output = []
    for i in df.index:
        output.append(df["地點"].iloc[i])
        # output.append({k: df[k].iloc[i] for k in Location.__fields__.keys()})

    return output


@app.post("/location/", tags=["location"])
def create_location(location: Location):
    """
    Create new location in T_地點
    """

    loc = location.__dict__["地點"]
    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_地點 WHERE 地點 = N'{loc}'"
    df = fetch_data(fetch_sql)
    if df is not None:
        raise HTTPException(status_code=404, detail=f"Location {loc} already exists.")

    sql = "INSERT INTO PRAISE.dbo.T_地點 (地點) values (%s)"
    data = [location.__dict__[k] for k in Location.__fields__.keys()]
    insert_data(sql, data)


@app.delete("/location/", tags=["location"])
def delete_location(loc: str):
    """
    Delete location [loc] in T_地點
    """

    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_地點 WHERE 地點 = N'{loc}'"
    df = fetch_data(fetch_sql)
    if df is None:
        raise HTTPException(status_code=404, detail=f"Location {loc} not found.")

    sql = f"DELETE FROM PRAISE.dbo.T_地點 WHERE 地點 = N'{loc}'"

    exec_table(sql)


@app.put("/location/", tags=["location"])
def update_location(loc: str, location: Location):
    """
    Update location [loc] in T_地點
    """

    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_地點 WHERE 地點 = N'{loc}'"
    df = fetch_data(fetch_sql)
    if df is None:
        raise HTTPException(status_code=404, detail=f"Location {loc} not found.")

    new_loc = location.__dict__["地點"]
    print(new_loc)

    sql = f"""
        UPDATE PRAISE.dbo.T_地點
        SET 地點 = N'{new_loc}'
        WHERE 地點 = N'{loc}'
    """

    exec_table(sql)


@app.get("/currencies", tags=["currency"])
def get_currencies() -> List[Currency]:
    """
    Get all currencies in T_貨幣
    """

    sql = "SELECT * FROM PRAISE.dbo.T_貨幣"
    df = fetch_data(sql)

    if df is None:
        raise HTTPException(status_code=404, detail="No Currency in DB.")

    output = []
    for i in df.index:
        output.append({k: df[k].iloc[i] for k in Currency.__fields__.keys()})

    return output


@app.get("/currency/", tags=["currency"])
def get_currency_by_name(currency_name: str) -> Currency:
    """
    Get currency with name [currency_name] in T_貨幣
    """

    sql = f"SELECT * FROM PRAISE.dbo.T_貨幣 WHERE 貨幣名稱 = N'{currency_name}'"
    df = fetch_data(sql)
    print(df)
    if df is None:
        raise HTTPException(
            status_code=404, detail=f"Currency with name {currency_name} not found"
        )

    output = {k: df[k].iloc[0] for k in Currency.__fields__.keys()}

    return output


@app.post("/currency/", tags=["currency"])
def create_currency(currency: Currency):
    """
    Create new currency in T_貨幣
    """

    currency_name = currency.__dict__["貨幣名稱"]
    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_貨幣 WHERE 貨幣名稱 = N'{currency_name}'"
    df = fetch_data(fetch_sql)
    if df is not None:
        raise HTTPException(
            status_code=404,
            detail=f"Currency with name {currency_name} already exists.",
        )

    cols = list(Currency.__fields__.keys())
    types = ",".join(["%d" if col in NUM_COLS["T_貨幣"] else "%s" for col in cols])
    sql = f"""
        INSERT INTO PRAISE.dbo.T_貨幣 ({", ".join(cols)}, add_time, add_user_id, update_time, update_user_id)
        values ({types}, %s, %d, %s, %d)
    """

    data = [currency.__dict__[k] for k in Currency.__fields__.keys()]
    data.extend([datetime.now(), 6, datetime.now(), 6])
    insert_data(sql, data)


@app.delete("/currency/", tags=["currency"])
def delete_currency(currency_name: str):
    """
    Delete currency with name [currency_name] in T_貨幣
    """

    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_貨幣 WHERE 貨幣名稱 = N'{currency_name}'"
    df = fetch_data(fetch_sql)
    if df is None:
        raise HTTPException(
            status_code=404,
            detail=f"Currency with name {currency_name} not found.",
        )

    sql = f"DELETE FROM PRAISE.dbo.T_貨幣 WHERE 貨幣名稱 = N'{currency_name}'"

    exec_table(sql)


@app.put("/currency/", tags=["currency"])
def update_currency(currency_name: str, currency: Currency):
    """
    Update currency with name [currency_name] in T_貨幣
    """

    if currency_name != currency.__dict__["貨幣名稱"]:
        raise HTTPException(
            status_code=404,
            detail=f"Currency name {currency_name} and {currency.__dict__['貨幣名稱']} not matched.",
        )

    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_貨幣 WHERE 貨幣名稱 = N'{currency_name}'"
    df = fetch_data(fetch_sql)
    if df is None:
        raise HTTPException(
            status_code=404, detail=f"Currency with name {currency_name} not found."
        )

    infos = []
    for k, v in currency.__dict__.items():
        if v is None:
            infos.append(f"{k} = NULL")
        elif k in NUM_COLS["T_貨幣"]:
            infos.append(f"{k} = {v}")
        else:
            infos.append(f"{k} = N'{v}'")

    sql = f"""
        UPDATE PRAISE.dbo.T_貨幣
        SET {', '.join(infos)}, update_time = '{datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')}'
        WHERE 貨幣名稱 = N'{currency_name}'
    """

    exec_table(sql)


@app.get("/groupusers/", tags=["group user"])
def get_groupusers_by_date(group_date: str) -> List[GroupUser]:
    """
    Get group users with date [group_date] in T_旅行團客戶
    """

    sql = f"SELECT * FROM PRAISE.dbo.T_旅行團客戶 WHERE 出團日期 = '{group_date}'"
    df = fetch_data(sql)
    if df is None:
        raise HTTPException(
            status_code=404,
            detail=f"Group User date {group_date} not found.",
        )

    output = []
    for i in df.index:
        output.append({k: df[k].iloc[i] for k in GroupUser.__fields__.keys()})

    print(len(output))

    return output


@app.get("/groupuser/", tags=["group user"])
def get_groupuser_by_id_date(user_id: str, group_date: str) -> GroupUser:
    """
    Get group user with ID[user_id] and date [group_date] in T_旅行團客戶
    """

    sql = f"SELECT * FROM PRAISE.dbo.T_旅行團客戶 WHERE 客戶ID = '{user_id}' AND 出團日期 = '{group_date}'"
    df = fetch_data(sql)
    if df is None:
        raise HTTPException(
            status_code=404,
            detail=f"Group User with ID {user_id} and date {group_date} not found.",
        )

    output = {k: df[k].iloc[0] for k in GroupUser.__fields__.keys()}

    return output


@app.post("/groupuser/", tags=["group user"])
def create_groupuser(group_user: GroupUser):
    """
    Create new group user in T_旅行團客戶
    """

    user_id = group_user.__dict__["客戶ID"]
    group_date = group_user.__dict__["出團日期"]
    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_旅行團客戶 WHERE 客戶ID = '{user_id}' AND 出團日期 = '{group_date}'"
    df = fetch_data(fetch_sql)
    if df is not None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} and date {group_date} already exists.",
        )

    cols = list(GroupUser.__fields__.keys())
    types = ",".join(
        ["%d" if col in NUM_COLS["T_旅行團客戶"] else "%s" for col in cols]
    )
    sql = f"""
        INSERT INTO PRAISE.dbo.T_旅行團客戶 ({", ".join(cols)})
        values ({types})
    """

    data = [group_user.__dict__[k] for k in GroupUser.__fields__.keys()]

    insert_data(sql, data)


@app.delete("/groupuser/", tags=["group user"])
def delete_groupuser(user_id: str, group_date):
    """
    Delete group user with ID [user_id] and date [group_date] in T_旅行團客戶
    """

    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_旅行團客戶 WHERE 客戶ID = '{user_id}' AND 出團日期 = '{group_date}'"
    df = fetch_data(fetch_sql)
    if df is None:
        raise HTTPException(
            status_code=404,
            detail=f"Group User with ID {user_id} and date {group_date} not found.",
        )

    sql = f"DELETE FROM PRAISE.dbo.T_旅行團客戶 WHERE 客戶ID = '{user_id}' AND 出團日期 = '{group_date}'"

    exec_table(sql)


@app.put("/groupuser/", tags=["group user"])
def update_groupuser(user_id: str, group_date: str, group_user: GroupUser):
    """
    Update group user with ID [user_id] and date [group_date] in T_旅行團客戶
    """

    if user_id != group_user.__dict__["客戶ID"]:
        raise HTTPException(
            status_code=404,
            detail=f"User ID {user_id} and {group_user.__dict__['客戶ID']} not matched.",
        )
    if group_date != datetime.strftime(group_user.__dict__["出團日期"], "%Y-%m-%d"):
        raise HTTPException(
            status_code=404,
            detail=f"Group date {group_date} and {group_user.__dict__['出團日期']} not matched.",
        )

    fetch_sql = f"SELECT * FROM PRAISE.dbo.T_旅行團客戶 WHERE 客戶ID = '{user_id}' AND 出團日期 = '{group_date}'"
    df = fetch_data(fetch_sql)
    if df is None:
        raise HTTPException(
            status_code=404,
            detail=f"Group User with ID {user_id} and date {group_date} not found.",
        )

    infos = []
    for k, v in group_user.__dict__.items():
        if v is None:
            infos.append(f"{k} = NULL")
        elif k in NUM_COLS["T_旅行團客戶"]:
            infos.append(f"{k} = {v}")
        else:
            infos.append(f"{k} = N'{v}'")

    sql = f"""
        UPDATE PRAISE.dbo.T_旅行團客戶
        SET {', '.join(infos)}
        WHERE 客戶ID = '{user_id}' AND 出團日期 = '{group_date}'
    """

    exec_table(sql)
