# conftest.py
import pytest
import requests
import allure
from faker import Faker
from data import urls, data


@pytest.fixture(scope="function")
def fake():
    return Faker()

@pytest.fixture(scope="function")
def update_name_data(fake):
    return {"name": fake.name()}

@pytest.fixture(scope="function")
def update_email_data(fake):
    return {"email": fake.email()}

@pytest.fixture(scope="function")
def update_password_data(fake):
    return {"password": fake.password()}

@pytest.fixture
def payload(request):
    # Возвращаем объект другой фикстуры по её имени из параметров - для параметризации
    return request.getfixturevalue(request.param)


@pytest.fixture(scope="function")
def create_user(fake):
    attempts = 0
    email = password = name = None
    create_response = None
    status_code = None
    token = None

    while attempts < 5:
        try:
            # Генерируем случайные данные
            email = fake.email()
            password = fake.password()
            name = fake.name()

            # Создаём пользователя
            payload = {"email": email, "password": password, "name": name}
            resp = requests.post(urls.create_user_url, data=payload)

            status_code = resp.status_code
            if status_code == 200:
                create_response = resp.json()
                token = create_response.get("accessToken")
                break
            else:
                print(f"Пользователь уже существует ({status_code}). Повторная попытка...")
                attempts += 1

        except Exception as e:
            print(f"Произошла ошибка при создании пользователя: {e}")
            attempts += 1

    if not create_response or status_code != 200:
        pytest.fail("Не удалось создать пользователя после 5 попыток.")

    # отдаём данные тесту
    yield email, password, name, create_response, status_code

    # teardown — удаление пользователя
    try:
        if not token:
            # если токена нет из create, получим через логин
            login_resp = requests.post(urls.login_user_url, data={"email": email, "password": password})
            if login_resp.status_code == 200:
                token = login_resp.json().get("accessToken")
        if token:
            requests.delete(
                urls.create_change_user_data_url_or_delete,
                headers={"Authorization": token}
            )
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")


@pytest.fixture(scope="function")
def create_and_login_user(fake):
    attempts = 0
    email = password = name = token = None

    while attempts < 5:
        try:
            # Генерируем случайные данные
            email = fake.email()
            password = fake.password()
            name = fake.name()

            # Создаём пользователя
            payload = {"email": email, "password": password, "name": name}
            create_resp = requests.post(urls.create_user_url, data=payload)

            if create_resp.status_code == 200:
                # выполняем логин
                login_payload = {"email": email, "password": password}
                login_resp = requests.post(urls.login_user_url, data=login_payload)

                assert login_resp.status_code == 200, f"Ошибка логина: {login_resp.text}"
                token = login_resp.json().get("accessToken")
                break
            else:
                print(f"Пользователь уже существует ({create_resp.status_code}). Повторная попытка...")
                attempts += 1

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            attempts += 1

    if not token:
        pytest.fail("Не удалось создать пользователя после 5 попыток.")

    # отдаём данные тесту
    yield email, password, name, token

    # teardown — удаление пользователя
    try:
        if token:
            requests.delete(
                urls.create_change_user_data_url_or_delete,
                headers={"Authorization": token}
            )
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")



@pytest.fixture(scope="function")
@allure.step("Создание заказа через API")
def create_order(create_and_login_user):
    email, password, name, token = create_and_login_user

    # Формируем тело запроса
    payload = data.create_order_with_ingredient


    response = requests.post(
        urls.create_order_url,
        headers={"Authorization": token},
        data=payload
    )

    assert response.status_code == 200, f"Ошибка при создании заказа: {response.text}"

    order_json = response.json()["order"]
    order_number = order_json["number"]
    order_name = order_json["name"]
    order_status = order_json["status"]

    # Возвращаем все данные, чтобы тест мог их использовать
    return order_number, order_name, order_status, token, email, name, password
