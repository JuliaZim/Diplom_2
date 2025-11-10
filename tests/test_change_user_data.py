import requests
import pytest
import allure
from data import urls
from faker import Faker
from data import response_text

fake = Faker()


class TestChangeUserData:
    @allure.title("Проверка успешного изменения имени пользователя")
    @allure.description(
        f"Проверка апи изменения данных юзера: {urls.create_change_user_data_url_or_delete}"
    )
    @allure.feature("Проверка изменения данных юзера")
    @allure.severity("High")
    def test_change_user_name_success(self, create_and_login_user, update_name_data):
        # Предусловие. Создаем пользователя и логинимся
        email, password, name, token = create_and_login_user

        # Выполняем шаги
        payload = update_name_data
        with allure.step("Отправляем запрос на изменение данных юзера"):
            response = requests.patch(
                urls.create_change_user_data_url_or_delete,
                headers={"Authorization": token},
                data=payload,
            )

        # Выполняем прооверки
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["user"]["name"] == payload["name"]
        assert response.json()["user"]["email"] == email

    @allure.title("Проверка успешного изменения email пользователя")
    @allure.description(
        f"Проверка апи изменения данных юзера: {urls.create_change_user_data_url_or_delete}"
    )
    @allure.feature("Проверка изменения данных юзера")
    @allure.severity("High")
    def test_change_user_email_success(self, create_and_login_user, update_email_data):
        # Предусловие. Создаем пользователя и логинимся
        email, password, name, token = create_and_login_user

        with allure.step("Отправляем запрос на изменение данных юзера"):
            # Выполняем шаги
            payload = update_email_data
            response = requests.patch(
                urls.create_change_user_data_url_or_delete,
                headers={"Authorization": token},
                data=payload,
            )

        # Выполняем прооверки
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["user"]["name"] == name
        assert response.json()["user"]["email"] == payload["email"]

    @allure.title("Проверка успешного изменения пароля пользователя")
    @allure.description(
        f"Проверка апи изменения данных юзера: {urls.create_change_user_data_url_or_delete}"
    )
    @allure.feature("Проверка изменения данных юзера")
    @allure.severity("High")
    def test_change_user_password_success(self, create_and_login_user, update_password_data):
        # Предусловие. Создаем пользователя и логинимся
        email, password, name, token = create_and_login_user

        with allure.step("Отправляем запрос на изменение данных юзера"):
            # Выполняем шаги
            payload = update_password_data
            response = requests.patch(
                urls.create_change_user_data_url_or_delete,
                headers={"Authorization": token},
                data=payload,
            )

        # Выполняем проверки
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["user"]["email"] == email
        assert response.json()["user"]["name"] == name

    @allure.description(
        f"Проверка апи изменения данных юзера: {urls.create_change_user_data_url_or_delete}. Негативный кейс, без авторизации."
    )
    @allure.feature("Проверка изменения данных юзера")
    @allure.severity("High")
    @pytest.mark.parametrize(
        ("payload", "title_case"),
        [
            ("update_email_data", "Проверка изменения email без авторизации"),
            ("update_name_data", "Проверка изменения email без авторизации"),
            ("update_password_data", "Проверка изменения email без авторизации"),
        ],
        ids = ["email", "name", "password"],
        indirect=["payload"]
    )
    def test_change_user_password_if_user_unauth(self, payload, title_case):
        with allure.step("Отправляем запрос на изменение данных юзера"):
            # Выполняем шаги
            allure.dynamic.title(title_case)
            response = requests.patch(
                urls.create_change_user_data_url_or_delete, data=payload
            )

        # Выполняем проверки
        assert response.status_code == 401
        response_value = response.json()
        assert response_value["success"] == False
        assert response_value["message"] == response_text.user_unauth
