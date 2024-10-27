from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory='templates')    # 'templates' - в качестве папки шаблонов

users = []


class User(BaseModel):    # класс(модель) User, наследованный от BaseModel
    """
    :param id (int) - номер пользователя
    :param username (str) - имя пользователя
    :param age (int) - возраст пользователя
    """
    id: int
    username: str
    age: int


@app.get('/')
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/user/{user_id}')
def get_user(request: Request,
             user_id: Annotated[int, Path(ge=1, le=1000, description='Enter ID user', example='3')]) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'user': user})
    raise HTTPException(status_code=404, detail='User was not found')


@app.post('/user/{username}/{age}')
def create_user(
        username: Annotated[str, Path(min_length=2, max_length=20, description='Enter username', example='Mat')],
        age: Annotated[int, Path(ge=18, le=100, description='Enter age', example='18')]) -> User:
    if not users:
        user_id = 1
    else:
        user_id = users[-1].id + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
def update_user(
        user_id: Annotated[int, Path(ge=1, le=1000, description='Enter ID user', example='3')],
        username: Annotated[str, Path(min_length=2, max_length=20, description='Enter username', example='Mat')],
        age: Annotated[int, Path(ge=18, le=100, description='Enter age', example='18')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user    # возвращаем объект с отредактированными данными выбранного пользователя
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
def delete_user(user_id: Annotated[int, Path(ge=1, le=1000, description='Enter ID user', example='3')]) -> User:
    for user in users:
        if user.id == user_id:
            index_found_user = users.index(user)
            return users.pop(index_found_user)
    raise HTTPException(status_code=404, detail='User was not found')
