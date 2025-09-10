import sender_stand_request
import data

def get_user_body(name,):
    current_body = data.user_body.copy()
    current_body["firstName"] = name
    return current_body

def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

def negative_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400

def negative_assert_missing_first_name():
    user_body = data.user_body_without_first_name  # Sin los paréntesis ()
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

def test_create_user_1_letter_in_first_name_get_success_response():
    negative_assert("A")

def test_create_user_16_letter_in_first_name_get_success_response():
    negative_assert("Аааааааааааааааа")

def test_create_user_space_letter_in_first_name_get_success_response():
    negative_assert("A Aaa")

def test_string_con_numeros():
    negative_assert("123")


def test_caracteres_especiales():
    negative_assert("№%@")

def test_missing_first_name():
    negative_assert_missing_first_name()

def test_caracteres_faltantes():
    negative_assert("")

def test_caracteres_diferente():
    negative_assert(12)

# Función de prueba negativa
# La respuesta contiene el siguiente mensaje de error: "No se han enviado todos los parámetros requeridos"
def negative_assert_no_firstname(user_body):
    # Guarda el resultado de llamar a la función a la variable "response"
    response = sender_stand_request.post_new_user(user_body)

    # Comprueba si la respuesta contiene el código 400
    assert response.status_code == 400

    # Comprueba si el atributo "code" en el cuerpo de respuesta es 400
    assert response.json()["code"] == 400

    # Comprueba si el atributo "message" en el cuerpo de respuesta se ve así:
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

# Prueba 8. Error
# La solicitud no contiene el parámetro "firstName"
def test_create_user_no_first_name_get_error_response():
    # El diccionario con el cuerpo de la solicitud se copia del archivo "data" a la variable "user_body"
    # De lo contrario, se podrían perder los datos del diccionario de origen
    user_body = data.user_body.copy()
    # El parámetro "firstName" se elimina de la solicitud
    user_body.pop("firstName")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)

