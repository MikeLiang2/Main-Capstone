from fastapi import APIRouter, HTTPException
from app.utils.users import mock_users
from app.models.users import AccountInfo, UserData
from datetime import datetime


router = APIRouter() 

# get user list with pagination
@router.get("/premission/user/{page}/{limit}", response_model=UserData)
def get_user_list(page: int, limit: int):
    start = (page - 1) * limit
    end = start + limit
    sliced_users = mock_users[start:end]
    return UserData(records=sliced_users, total=len(mock_users))

# get one user
@router.get("/premission/user/{user_id}", response_model=AccountInfo)
def get_user(user_id: int):
    for user in mock_users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# add user
@router.post("/premission/user", response_model=AccountInfo)
def add_user(user_data: AccountInfo):
    # 自动分配自增 ID：若当前没有用户，则从 1 开始
    new_id = max([user["id"] for user in mock_users], default=0) + 1

    new_user = {
        "id": new_id,
        "createTime": datetime.now().isoformat(),
        "updateTime": datetime.now().isoformat(),
        "email": user_data.email,
        "username": user_data.username,
        "password": user_data.password
    }
    mock_users.append(new_user)
    return AccountInfo(**new_user)

# update user
@router.put("/premission/user/update/{user_id}", response_model=AccountInfo)
def update_user(user_id: int, user_data: AccountInfo):
    for user in mock_users:
        if user["id"] == user_id:
            user["email"] = user_data.email
            user["username"] = user_data.username
            user["password"] = user_data.password
            user["updateTime"] = datetime.now().isoformat()
            user["roleId"] = user_data.roleId
            return user
    raise HTTPException(status_code=404, detail="User not found")


# remove user
@router.delete("/premission/user/delete/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(mock_users):
        if user["id"] == user_id:
            del mock_users[i]
            return {"message": f"User with id {user_id} deleted successfully."}
    
    raise HTTPException(status_code=404, detail="User not found")


