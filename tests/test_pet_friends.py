from api import PetFriends
from settings import valid_email, valid_password


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_not_get_api_key_for_user(email='alnn@mail.ru', password='111222333'):
    """ Проверяем что запрос api ключа с некорректными данными возвращает статус 403(The error code
    means that provided combination of user email and password is incorrect)"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Djon', animal_type='ej',
                                     age='4', pet_photo='images/ezik.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_invalid_data(name='$fdg', animal_type='87fgf',
                                     age='old', pet_photo='images/ezik.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными(это баг)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_incomplete_data(name='Tom',
                                     age='7', pet_photo='images/ezik.jpg'):
    """Проверяем можно ли добавить питомца без одного из параметров - нет animal_type"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Djon", "ej", "4", "images/ezik.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_not_delete_self_pet():
    """Проверяем не возможность удаления питомца с неверными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Name_not", "Animal_type_not", "5", "images/not.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Djon', animal_type='ej', age=6):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_not_update_self_pet_info(name='Dj', animal_type='j', age=6):
    """Проверяем не возможность обновления информации о питомце с неверными данными """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_successful_update_self_pet_info_name(name='Fred', animal_type='ej', age=6):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_add_pet_with_valid_data_without_photo(name='Frod', animal_type='enot',
                                     age='2'):
    """Проверяем что можно добавить питомца без фотографии"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_photo_pet(pet_photo='images/enot.jpg'):
    """Проверяем что можно добавить фото к питомцу, созданному без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if pet_photo in my_pets['pets'][0]['id']:

        _, my_pets = pf.add_pet_without_photo(auth_key, 'Frod', 'enot', '2')

    status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    assert status == 200
    assert result['pet_photo'] != ''

def test_add_new_pet_with_invalid_photo(name='Pit', animal_type='animal',
                                     age='2', pet_photo='images/Black.gif'):
    """Проверяем как добавляется питомец если фото в формате GIF"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_photo_png(name='Bob', animal_type='animal',
                                     age='5', pet_photo='images/hog.png'):
    """Проверяем как добавляется питомец если фото в формате PNG"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name