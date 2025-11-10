import requests
import pytest
import allure
from data import urls
from data import response_text



class TestLoginUser:
    @allure.title("Проверка успешного логина")
    @allure.description(f"Проверка апи логина юзера: {urls.create_user_url}")
    @allure.feature("Проверка логина")
    @allure.severity("High")
    def test_login_with_exist_logpas(self, create_user):
        # Предусловие. Создаем юзера
        email, password, name, create_response, status_code = create_user
        token = create_response["accessToken"]

        with allure.step("Отправляем запрос на логин пользователя"):
            # Выполняем логин пользоваателя
            payload = {"email": email, "password": password}
            response = requests.post(urls.login_user_url, data=payload)

        # Выполняем проверки
        assert response.status_code == 200
        response_value = response.json()
        assert response_value["success"] == True
        assert response_value["accessToken"] != None
        assert response_value["refreshToken"] != None
        assert response_value["user"]["email"] == email
        assert response_value["user"]["name"] != None

    @allure.description("Проверка апи логина юзера: {urls.create_user_url}")
    @allure.feature("Проверка логина")
    @allure.severity("High")
    @pytest.mark.parametrize(
        "incorrect_logpas_data",
        [
            ("log", "123", "Проверка логина с неправильным логином"),
            ("me123@whatyouknow.com", "", "Проверка логина: отсутствует пароль"),
            ("", "123", "Проверка логина: отсутствует логин"),
        ],
    )
    def test_login_with_incorrect_logpas(self, incorrect_logpas_data):
        with allure.step("Отправляем запрос на логин пользователя"):
            # Выполняем шаги
            email, password, title_case = incorrect_logpas_data
            payload = {"email": email, "password": password}
            allure.dynamic.title(title_case)
            response = requests.post(urls.login_user_url, data=payload)

        # Выполняем проверки
        assert response.status_code == 401
        response_value = response.json()
        assert response_value == response_text.incorrect_logpas_response
