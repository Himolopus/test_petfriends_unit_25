import pytest
from  settings import all_pets_page, my_pets_page

'''Тестовый класс тестирования страницы "https://petfriends.skillfactory.ru/all_pets"'''
class TestAllPets:
    @pytest.fixture(autouse=True)
    def setup_method(self, session_driver, all_pets_elements):
        self.driver = session_driver
        self.header_element = all_pets_elements['header']
        self.image_elements = all_pets_elements['images']
        self.name_elements = all_pets_elements['names']
        self.description_elements = all_pets_elements['descriptions']

    def test_all_pets_page_show_up(self):
        assert self.driver.current_url == all_pets_page
        assert self.header_element.text == 'PetFriends'

    def test_pet_cards_photo_is_loaded(self):
        for i in range(len(self.name_elements)):
            assert self.image_elements[i].get_attribute('src') != '', 'Фото питомца не загружено'

    def test_pet_cards_has_name(self):
        for i in range(len(self.name_elements)):
            assert self.name_elements[i].text != '', 'Отсутствует имя питомца'

    def test_pet_cards_has_correct_description(self):
        for i in range(len(self.name_elements)):
            assert self.description_elements[i].text != '', 'Отсутствует описание питомца'
            assert ', ' in self.description_elements[i].text, 'Неверный формат описания'
            parts = self.description_elements[i].text.split(", ")
            assert len(parts[0]) > 0, 'Отсутствует порода питомца в описании'
            assert len(parts[1]) > 0, 'Отсутствует возраст питомца в описании'


'''Тестовый класс тестирования страницы "https://petfriends.skillfactory.ru/my_pets"'''
class TestMyPets:

    @pytest.fixture(autouse=True)
    def setup_method(self, session_driver, my_pets_elements):
        self.driver = session_driver
        self.pet_count = len(my_pets_elements['entities'])
        self.info_block_element = my_pets_elements['info_block']
        self.pets_with_photo_elements = my_pets_elements['pets_with_photo']
        self.name_elements = my_pets_elements['names']
        self.type_elements = my_pets_elements['types']
        self.age_elements = my_pets_elements['ages']

    def test_my_pets_page_show_up(self):
        assert self.driver.current_url == my_pets_page
        assert 'Питомцев' in self.info_block_element.text

    def test_amount_of_pets_from_info_and_table_are_equal(self):   # Task 1
        pet_count_info = None
        # Извлекаем кол-во питомцев из инфо блока с помощью списка
        parts = self.info_block_element.text.split()
        for i in range(len(parts)):
            if parts[i] == "Питомцев:":
                pet_count_info = int(parts[i + 1])
        # Сравнение кол-ва питомцев из инфо блока с количеством сущностей в таблице
        assert pet_count_info == self.pet_count, 'Количечество питомцев не соответствует статистике пользователя'


    def test_equal_or_more_than_half_of_pets_has_photo(self):   # Task 2
        # Проверка того что у половины или более питомцев есть фото
        assert len(self.pets_with_photo_elements) >= self.pet_count / 2, 'Более половины питомцев не имеют фото'

    def test_all_pets_has_name_type_age(self):   # Task 3

        for i in range(self.pet_count):
            # Проверка наличия имени и породы питомца, т.е. любой отображаемой строки
            assert self.name_elements[i].text and not self.name_elements[i].text.isspace(), 'Отсутствует имя питомца'
            assert self.type_elements[i].text and not self.type_elements[i].text.isspace(), 'Отсутствует порода питомца'
            # Проверка начличия возраста, который является целым положительным числом
            assert self.age_elements[i].text.isdigit(), 'Отсутствует или не валиден возраст питомца'


    def test_all_pets_has_uniqe_name(self):   # Task 4
        pet_names = [element.text for element in self.name_elements]
        # Проверка того что каждое имя питомца уникально
        assert len(pet_names) == len(set(pet_names)), 'Одинаковые имена питомцев'


    def test_all_pets_has_uniqe_combination_of_name_type_age(self):   # Task 5
        # Создаем список питомцев
        pets = []
        for i in range(self.pet_count):
            pets.append({'name': self.name_elements[i].text,
                         'type': self.type_elements[i].text,
                         'age': self.age_elements[i].text})
        # Сравниваем записи друг с другом
        for i in range(len(pets) - 1):
            for j in range(i + 1, len(pets)):
                assert pets[i] != pets[j], 'Повторяющиеся питомцы'
