import requests
import allure
from data import urls, response_text
from faker import Faker


fake = Faker()


class TestCreateUser:
    @allure.title("Проверка успешного создания клиента")
    @allure.description(f"Проверка апи создания юзера: {urls.create_user_url}")
    @allure.feature("Проверка создания клиента")
    @allure.severity("High")
    def test_create_user_success(self, create_user):
        # Создание юзера
        email, password, name, create_response, status_code = create_user

        # Забираем токен
        token = create_response["accessToken"]

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
    def test_create_user_which_exist(self, create_user):
        # Предусловие. Создаем пользователя
        email, password, name, create_response, status_code = create_user
        # Забираем токен
        token = create_response["accessToken"]

        with allure.step('Отправляем повторный запрос на создание пользователя'):
        # Выполняем шаги
            payload = {"name": name, "email": email, "password": password}
            response = requests.post(urls.create_user_url, data=payload)

        # Выполняем проверки
        assert response.status_code == 403
        assert response.json()["success"] == False
        assert response.json()["message"] == response_text.user_exist_response

    @allure.title("Проверка логина без имени")
    @allure.description(f"Проверка апи создания юзера: {urls.create_user_url}")
    @allure.feature("Проверка создания клиента")
    @allure.severity("Low")
    def test_create_user_without_name_value(self, fake):
        email = fake.email()
        password = fake.password()
        # Выполняем шаги
        with allure.step('Отправляем запрос на создание пользователя без обязательных параметров'):
            payload = {"name": "", "email": email, "password": password}
            response = requests.post(urls.create_user_url, data=payload)

        # Выполняем проверки
        assert response.status_code == 403
        assert response.json()["success"] == False
        assert (
            response.json()["message"]
            == response_text.create_user_required_field_response
        )


    @allure.title("Проверка логина без email")
    @allure.description(f"Проверка апи создания юзера: {urls.create_user_url}")
    @allure.feature("Проверка создания клиента")
    @allure.severity("Low")
    def test_create_user_without_email_value(self, fake):
        name = fake.name()
        password = fake.password()
        # Выполняем шаги
        with allure.step('Отправляем запрос на создание пользователя без обязательных параметров'):
            payload = {"name": name, "email": "", "password": password}
            response = requests.post(urls.create_user_url, data=payload)

        # Выполняем проверки
        assert response.status_code == 403
        assert response.json()["success"] == False
        assert (
            response.json()["message"]
            == response_text.create_user_required_field_response
        )

    @allure.title("Проверка логина без пароля")
    @allure.description(f"Проверка апи создания юзера: {urls.create_user_url}")
    @allure.feature("Проверка создания клиента")
    @allure.severity("Low")
    def test_create_user_without_password_value(self, fake):
        name = fake.name()
        email = fake.email()

        # Выполняем шаги
        with allure.step('Отправляем запрос на создание пользователя без обязательных параметров'):
            payload = {"name": name, "email": email, "password": ""}
            response = requests.post(urls.create_user_url, data=payload)

        # Выполняем проверки
        assert response.status_code == 403
        assert response.json()["success"] == False
        assert (
            response.json()["message"]
            == response_text.create_user_required_field_response
        )
