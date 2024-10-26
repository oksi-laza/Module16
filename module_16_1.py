from fastapi import FastAPI

app = FastAPI()    # создала приложение(объект) FastAPI


@app.get('/')
async def get_main_page() -> str:
    return 'Главная страница'


@app.get('/user/admin')
async def get_admin_page() -> str:
    return 'Вы вошли как администратор'


@app.get('/user/{user_id}')
async def get_user_number(user_id: int) -> str:
    return f'Вы вошли как пользователь № {user_id}'


@app.get('/user')
async def get_user_info(username: str, age: int) -> str:
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}'
