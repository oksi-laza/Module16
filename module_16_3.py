from fastapi import FastAPI, Path
from typing import Annotated


app = FastAPI()    # создала приложение FastAPI


users = {'1': 'Имя: Example, возраст: 18'}


@app.get('/users')
async def get_all_users() -> dict:
    return users    # возвращает словарь users


@app.post('/user/{username}/{age}')
async def create_user(
        username: Annotated[str, Path(min_length=2, max_length=20, description='Enter username', example='Mat')],
        age: Annotated[int, Path(ge=18, le=100, description='Enter age', example='18')]) -> str:
    next_user_id = str(int(max(users, key=int)) + 1)   # идентификатор для нового пользователя
    print(next_user_id)
    users[next_user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {next_user_id} is registered'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: Annotated[str, Path(min_length=1, max_length=10, description='Enter ID user', example='3')],
        username: Annotated[str, Path(min_length=2, max_length=20, description='Enter username', example='Mat')],
        age: Annotated[int, Path(ge=18, le=100, description='Enter age', example='18')]) -> str:
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {user_id} has been updated'


@app.delete('/user/{user_id}')
async def delete_user(
        user_id: Annotated[str, Path(min_length=1, max_length=10, description='Enter ID user', example='3')]) -> str:
    users.pop(user_id)
    return f'User {user_id} has been deleted'
