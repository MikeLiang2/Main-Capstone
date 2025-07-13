from datetime import datetime
from typing import List

mock_users = []

for i in range(1, 101):  # 假设有 100 条用户数据
    mock_users.append({
        "id": i,
        "createTime": datetime.now().isoformat(),
        "updateTime": datetime.now().isoformat(),
        "email": f"user{i}@example.com",
        "username": f"user{i}",
        "password": "******",
        "roleId": 1 if i % 2 == 0 else 2  # 默认角色 ID
    })

edit_users_test = [
    {
        "id": 101,
        "createTime": datetime.now().isoformat(),
        "updateTime": datetime.now().isoformat(),
        "email": "user1@example.com",
        "username": "user1",
        "password": "39019192",
        "roleId": 1
    },
    {
        "id": 102,
        "createTime": datetime.now().isoformat(),
        "updateTime": datetime.now().isoformat(),
        "email": "user2@example.com",
        "username": "user2",
        "password": "186504",
        "roleId": 2
    }
]

mock_users.extend(edit_users_test)
