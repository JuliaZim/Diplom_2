import requests
import allure
from helpers import help_script
from data import urls
from data import response_text


class TestGetOrders_from_user:
    @allure.title(
        "Проверка получения заказов конкретного пользователя. Пользователь Авторизован"
    )
    @allure.description(
        f"Проверка апи получения заказов конкретного пользователя: GET {urls.get_orders_url}"
    )
    @allure.feature("Проверка получения заказов конкретного пользователя")
    @allure.severity("High")
    def test_get_orders_from_user_with_auth(self):
        # Предусловие. Создаем пользователя и логинимся
        email, password, name, token = help_script.create_and_login_user()
        number, name_burger, status = help_script.create_order(token)

        with allure.step(
            "Отправляем запрос на получение заказов конкретного пользователя"
        ):
            # Выполняем шаги
            response = requests.get(
                urls.get_orders_url, headers={"Authorization": token}
            )

        # Постусловия. Удаляем юзера
        help_script.delete_user(name, email, token)

        # Выполняем проверки
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["orders"] != None
        orders = response.json()["orders"]
        first_order = orders[0]
        assert first_order["number"] == number
        assert first_order["name"] == name_burger
        assert first_order["status"] == status

    @allure.title(
        "Проверка получения заказов конкретного пользователя. Пользователь неавторизован"
    )
    @allure.description(
        f"Проверка апи получения заказов конкретного пользователя: GET {urls.get_orders_url}"
    )
    @allure.feature("Проверка получения заказов конкретного пользователя")
    @allure.severity("High")
    def test_get_orders_from_user_without_auth(self):
        with allure.step(
            "Отправляем запрос на получение заказов конкретного пользователя"
        ):
            # Выполняем шаги
            response = requests.get(urls.get_orders_url)

        # Выполняем проверки
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()["message"] == response_text.user_unauth
