import requests
import pytest
import allure
from helpers import help_script
from data import urls, response_text
from faker import Faker


fake = Faker()


class TestCreateUser:
    @allure.title("Проверка успешного создания клиента")
    @allure.description(f"Проверка апи создания юзера: {urls.create_user_url}")
    @allure.feature("Проверка создания клиента")
    @allure.severity("High")
    def test_create_user_success(self):
        # Создание юзера
        email, password, name, create_response, status_code = help_script.create_user()

        # Забираем токен
        token = create_response["accessToken"]

        # Постусловия. Удаляем юзера
        help_script.delete_user(name, email, token)

        # Выполняем проверки
        assert status_code == 200
        assert create_response["success"] == True
        assert create_response["accessToken"] != None
        assert create_response["refreshToken"] != None
        assert create_response["user"]["email"] == email
        assert create_response["user"]["name"] == name

    @allure.title("Проверка успешного логина")
    @allure.description(f"Проверка апи создания юзера: {urls.create_user_url}")
    @allure.feature("Проверка создания клиента")
    @allure.severity("Medium")
    def test_create_user_which_exist(self):
        # Предусловие. Создаем пользователя
        email, password, name, create_response, status_code = help_script.create_user()
        # Забираем токен
        token = create_response["accessToken"]

        with allure.step('Отправляем повторный запрос на создание пользователя'):
        # Выполняем шаги
            payload = {"name": name, "email": email, "password": password}
            response = requests.post(urls.create_user_url, data=payload)

        # Постусловия. Удаляем юзера
        help_script.delete_user(name, email, token)

        # Выполняем проверки
        assert response.status_code == 403
        assert response.json()["success"] == False
        assert response.json()["message"] == response_text.user_exist_response

    @allure.description(f"Проверка апи создания юзера: {urls.create_user_url}")
    @allure.feature("Проверка создания клиента")
    @allure.severity("Low")
    @pytest.mark.parametrize(
        "create_user_data",
        [
            (
                "",
                fake.email(),
                fake.password(),
                "Проверка создания пользователя: Отсутствует имя",
            ),
            (
                fake.name(),
                "",
                fake.password(),
                "Проверка создания пользователя: Отсутствует email",
            ),
            (
                fake.name(),
                fake.email(),
                "",
                "Проверка создания пользователя: Отсутствует пароль",
            ),
        ],
    )
    def test_create_user_without_required_value(self, create_user_data):
        # Выполняем шаги
        with allure.step('Отправляем запрос на создание пользователя без обязательных параметров'):
            name, email, password, title_case = create_user_data
            allure.dynamic.title(title_case)
            payload = {"name": name, "email": email, "password": password}
            response = requests.post(urls.create_user_url, data=payload)

        # Выполняем проверки
        assert response.status_code == 403
        assert response.json()["success"] == False
        assert (
            response.json()["message"]
            == response_text.create_user_required_field_response
        )
