import requests
import allure
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
    def test_get_orders_from_user_with_auth(self, create_order):
        # Предусловие. Создаем пользователя и логинимся
        order_number, order_name, order_status, token, email, name, password = create_order

        with allure.step(
            "Отправляем запрос на получение заказов конкретного пользователя"
        ):
            # Выполняем шаги
            response = requests.get(
                urls.get_orders_url, headers={"Authorization": token}
            )

        # Выполняем проверки
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["orders"] != None
        orders = response.json()["orders"]
        first_order = orders[0]
        assert first_order["number"] == order_number
        assert first_order["name"] == order_name
        assert first_order["status"] == order_status

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
