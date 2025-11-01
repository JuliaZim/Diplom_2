import requests
import random
import string
from data import urls
from faker import Faker
import allure
from data import data


fake = Faker()


@allure.step("Создание юзера")
def create_user():
    payload = {"name": fake.name(), "email": fake.email(), "password": fake.password()}
    response = requests.post(urls.create_user_url, data=payload)
    response_value = response.json()
    if response.status_code == 200:
        return (
            payload["email"],
            payload["password"],
            payload["name"],
            response_value,
            response.status_code,
        )
    elif response.status_code == 403:
        return None


@allure.step("Удаление юзера")
def delete_user(name, email, token):
    payload = {"name": name, "email": email}
    response = requests.delete(
        urls.create_change_user_data_url_or_delete,
        data=payload,
        headers={"Authorization": token},
    )


@allure.step("Логин юзера")
def create_and_login_user():
    attempts = 0
    while attempts < 5:
        try:
            email, password, name, create_response, status_code = create_user()
            if create_response is not None:
                token = create_response["accessToken"]
                # Выполняем логин пользоваателя
                payload = {"email": email, "password": password}
                response = requests.post(urls.login_user_url, data=payload)
                return email, password, name, token
                break
            else:
                print("Пользователь уже существует. Повторная попытка...")
                attempts += 1
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            attempts += 1
    print("Не удалось создать пользователя после 3 попыток.")


@allure.step("Создание заказа с ингредиентами")
def create_order(user_token):
    payload = data.create_order_with_ingredient
    response = requests.post(
        urls.create_order_url, headers={"Authorization": user_token}, data=payload
    )
    return (
        response.json()["order"]["number"],
        response.json()["order"]["name"],
        response.json()["order"]["status"],
    )
