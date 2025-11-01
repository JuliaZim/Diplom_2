import requests
import allure
from helpers import help_script
from data import urls
from data import data
from data import response_text


"""с авторизацией,
без авторизации,
с ингредиентами,
без ингредиентов,
с неверным хешем ингредиентов."""


class TestCreateOrder:
    @allure.title("Проверка создания заказа с авторизацией")
    @allure.description(f"Проверка апи создания заказа: {urls.create_order_url}")
    @allure.feature("Проверка создания заказа")
    @allure.severity("High")
    def test_create_order_with_ingredients_with_auth(self):
        # Предусловие. Создаем пользователя и логинимся
        email, password, name, token = help_script.create_and_login_user()

        with allure.step('Отправляем запрос на создание заказа'):
        # Выполняем шаги
            payload = data.create_order_with_ingredient
            response = requests.post(
                urls.create_order_url, headers={"Authorization": token}, data=payload
            )

        # Постусловия. Удаляем юзера
        help_script.delete_user(name, email, token)

        # Выполняем прооверки
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["name"] != None
        assert response.json()["order"]["number"] != None

    @allure.title("Проверка создания заказа без ингредиентов")
    @allure.description(f"Проверка апи создания заказа: {urls.create_order_url}")
    @allure.feature("Проверка создания заказа")
    @allure.severity("High")
    def test_create_order_without_ingredients_with_auth(self):
        # Предусловие. Создаем пользователя и логинимся
        email, password, name, token = help_script.create_and_login_user()

        with allure.step('Отправляем запрос на создание заказа'):
        # Выполняем шаги
            payload = data.create_order_without_ingredient
            response = requests.post(
                urls.create_order_url, headers={"Authorization": token}, data=payload
            )


        # Постусловия. Удаляем юзера
        help_script.delete_user(name, email, token)

        # Выполняем прооверки
        assert response.status_code == 400
        assert response.json()["success"] == False
        assert (
            response.json()["message"]
            == response_text.order_without_ingredient_response
        )

    @allure.title("Проверка создания заказа без авторизации")
    @allure.description(
        f"Проверка апи создания заказа: {urls.create_order_url}. Негативный кейс, без авторизации."
    )
    @allure.feature("Проверка создания заказа")
    @allure.severity("High")
    def test_create_order_if_user_unauth(self):
        with allure.step('Отправляем запрос на создание заказа'):
        # Выполняем шаги
            payload = data.create_order_with_ingredient
            response = requests.post(urls.create_order_url, data=payload)

        # Выполняем проверки
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["name"] != None
        assert response.json()["order"]["number"] != None

    @allure.title("Проверка создания заказа с несуществующими ингредиентами")
    @allure.description(f"Проверка апи создания заказа: {urls.create_order_url}")
    @allure.feature("Проверка создания заказа")
    @allure.severity("High")
    def test_create_order_with_incorrect_ingredients_with_auth(self):
        # Предусловие. Создаем пользователя и логинимся
        email, password, name, token = help_script.create_and_login_user()

        with allure.step('Отправляем запрос на создание заказа'):
        # Выполняем шаги
            payload = data.create_order_with_incorrect_ingredient
            response = requests.post(
                urls.create_order_url, headers={"Authorization": token}, data=payload
            )

        # Постусловия. Удаляем юзера
        help_script.delete_user(name, email, token)

        # Выполняем прооверки
        assert response.status_code == 500
        assert response_text.order_with_incorrect_ingredients in response.text
