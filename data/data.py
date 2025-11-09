from faker import Faker

fake = Faker()

update_name_data = {"name": fake.name()}
update_email_data = {"email": fake.email()}
update_password_data = {"password": fake.password()}

create_order_with_ingredient = {
    "ingredients": [
        "61c0c5a71d1f82001bdaaa6f",
        "61c0c5a71d1f82001bdaaa72",
        "61c0c5a71d1f82001bdaaa6d",
    ]
}

create_order_without_ingredient = {
    "ingredients": [
    ]
}

create_order_with_incorrect_ingredient = {
    "ingredients": [
        "61c0",
        "6",
        "",
    ]
}