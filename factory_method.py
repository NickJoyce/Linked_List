from abc import ABC, abstractmethod # для создание абстрактных классов

from drivers import IStructureDriver, SimpleFileDriver, JsonFileDriver


class DriverFactoryMethod(ABC): #ы абстрактный класс
    @classmethod 
    @abstractmethod
    def get_driver(cls) -> IStructureDriver: # получение драйвера
        ...


class SimpleFileFactoryMethod(DriverFactoryMethod): # наследует асбтрактный класс. Должен переопределить методы которые есть в абстрактном классе.
    DEFAULT_NAME = 'untitled.txt' # атрибут класса - имя файла по умолчанию

    @classmethod
    def get_driver(cls) -> IStructureDriver:
        filename = input('Введите название текстового файла: (.txt)').strip() # ввод имени файла, удаление переноса строки в конце
        filename = filename or cls.DEFAULT_NAME # если имя файла введено, то имя файла, если нет то имя файла по умолчанию
        if not filename.endswith('.txt'): # если filename не заканчивается '.txt'
            filename = f'{filename}.txt' # то добавляем расширение файла в конец строки имени

        return SimpleFileDriver(filename) # создаем экземпляр класса 


# TODO реализовать класс JsonFileDriveFactoryMethod
class JsonFileFactoryMethod(DriverFactoryMethod):
    DEFAULT_NAME = 'untitled.json'

    @classmethod
    def get_driver(cls) -> IStructureDriver:
        filename = input('Введите название json-файла (.json):').strip()
        filename = filename or cls.DEFAULT_NAME
        if not filename.endswith('.json'):
            filename = f'{filename}.json'
        return JsonFileDriver(filename)


if __name__ == '__main__':

    driver = SimpleFileFactoryMethod.get_driver() # экземпляр класса SimpleFileDriver
    print(driver)
    data = [1,2,3] # данные которые нужно записать в файл txt
    driver.write(data)
    driver.read()


    driver = JsonFileFactoryMethod.get_driver() # экземпляр класса JsonFileDriver
    print(driver)
    data = [3,2,1] # данные которые нужно записать в файл json
    driver.write(data)
    driver.read()
