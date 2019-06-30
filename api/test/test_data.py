from lib.db import DB

datas = {
    # 表1
    "table1": [
        {'id': 1, 'name': 'chang'}
    ],
    # 表2
    "table2": [
        {'id': 1, 'class': 'one'}
    ],
}


# 插入测试数据到数据库表中
def init_data():
    db = DB()
    for table, data in datas.items():
        pass
        for d in data:
            db.insert(table, d)
