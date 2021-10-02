from main import LinkedList
from drivers import IStructureDriver
from factory_method import SimpleFileFactoryMethod, JsonFileFactoryMethod

class LinkedListWithDriver(LinkedList):
	def __init__(self, data=None, driver=None):
		super().__init__(data)
		self.driver = driver

	@property
	def driver(self):
		return self._driver

	@driver.setter
	def driver(self, driver):
		if not isinstance(driver, (IStructureDriver, type(None))):
			raise TypeError
		self._driver = driver

	def read(self): # читаем из файла, записываем в LinkedList
		data_from_driver = self.driver.read() # вызываем метод read() класса IStructureDriver, переопределенной в дочернем классе, для считываения данных
		self.clear() # очищаем LinkedList
		for value in data_from_driver:
			self.append(value) # добавляем значения в строках прочитанного файла в LinkedList

	def write(self): # из LinkedList записываем в файл
		self.driver.write(self) # записываем данные из LinkedList в файл
	

if __name__ == '__main__':
	ll = LinkedListWithDriver() # 'экзмепляр класса 'LinkedListWithDriver (data = None, Driver = None)
	ll.driver = SimpleFileFactoryMethod.get_driver() # инициализация драйвера, с вводом имени файла
	ll.read() # чтение из файла, добавление данных в список
	ll.write() # запись в файл из списка


	ll.driver = JsonFileFactoryMethod.get_driver()
	ll.write()



