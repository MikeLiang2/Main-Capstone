# for mock data
from app.models.users import UserInfo

mock_user = UserInfo(
    id=1,
    avatar="https://img1.baidu.com/it/u=1704600258,4057367107&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=800",
    username="admin",
    password="123456",
    email="admin@example.com",
    roles=["admin"],
    buttonPermissions=["add", "edit", "delete"],
    routePermissions=["/dashboard", "/admin"],
    token=""
)