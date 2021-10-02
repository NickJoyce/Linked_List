from node import Node, DoubleLinkedNode

from iterators import LinkedListIterator

from itertools import repeat

from prettytable import PrettyTable

import copy



class LinkedList():
	NODE_TYPE = Node


	def __init__(self, data=None):
		self.len = 0  
		self.head = None
		self.tail = None
		if data is not None:
			for value in data:
				self.append(value)


    # ГЕТТЕРЫ И СЕТТЕРЫ
	@property
	def len(self):
		return self._len

	@len.setter
	def len(self, value):
		# > 0
		self._len  = value

	@property
	def head(self):
		return self._head

	@head.setter
	def head(self, head_node):
		self._head = head_node

	@property
	def tail(self):
		return self._tail

	@tail.setter
	def tail(self, tail_node):
		self._tail = tail_node



	# ДЛИННА СПИСКА
	def __len__(self): 
		return self.len 


	# СТРОКОВЫЕ ПРЕДСТАВЛЕНИЯ
	def __str__(self): # вывод для пользователя
		return f'{[node for node in self]}'

	def __repr__(self) -> str: # вывод для разработчика
		return f"{self.__class__.__name__}({[list_value for list_value in self]})"

 

	# ИТЕРАЦИЯ
	def __iter__(self):
		return LinkedListIterator(self.head, self.len)


	# ИНДЕКСИРОВАНИЕ
	def __getitem__(self, index): # автоматически вызывается для операций индексирования экземпляров (выражения индексирования типа: self[i]) 
		node = self.step_by_step_on_nodes(index) # получаем узел по индексу
		return node.value # возвращаем атрибут value экземпляра класса Node

	def __setitem__(self, index, value): # автоматически вызывается для операции присваивания по индексу (выражения присваивания типа: self[i] = value)
		node = self.step_by_step_on_nodes(index)
		node.value = value
	
	def __delitem__(self, index): 	# автоматически вызывается для операций удаления по индексу(ключу) (выражения удаления типа del self[i])
		self._is_valid_index(index)

		if index == 0: # если удаляемый элемент первый
			self.head = self.head.next # голова равна узлу записанному у нее в атрибуте next, если это последний элемент то будет None
			if self.head == None:
				self.tail = None

		elif index == self.len-1: # если удаляемый элемент последний
			prev_node = self.step_by_step_on_nodes(index-1) # предпоследний узел
			prev_node.next = None # удаляем ссылку в атрибуте next у предпоследнего узла
			self.tail = prev_node # меняем хвост на предпоследний
			
		else: # если удалемый элемент не первый и не последний
			prev_node = self.step_by_step_on_nodes(index-1) # узел перед удаляемым 
			next_node = self.step_by_step_on_nodes(index+1) # узел после удаляемого
			self.linked_nodes(prev_node, next_node) # соединяем предыдущий и следующий узлы, узел удаляется автоматически потому что на него нет ссылки
		self.len -= 1 




	# ПЕРЕЗАГРУЗКА ОПЕРАЦИЙ СЛОЖЕНИЯ
	def __add__(self, other: "LinkedList") -> "LinkedList": # сложение
		if not isinstance(other, LinkedList):  
			raise TypeError
		for i in other:
			self.append(i)
		return self

	def __radd__(self, other): # правостороннее сложение с листом
		if not isinstance(other, list):
			raise TypeError
		ll = self.__class__(other)
		for i in self:
			ll.append(i)
		return ll

	def __iadd__(self, other): # одновременное сложение и присваивание
		if not isinstance(other, LinkedList):  
			raise TypeError
		self = self + other
		return self



	# ПЕРЕЗАГРУЗКА ОПЕРАЦИЙ УМНОЖЕНИЯ
	def __mul__(self, other): # метод клонирования последовательности
		self._is_int(other)
		for list_ in repeat([node_value for node_value in self], other-1):
			for item in list_:
				self.append(item)
		return self

	def __rmul__(self, other: int) -> "LinkedList": #  правостороннее умножение
		self._is_int(other)
		return self*other

	def __imul__(self, other: int) -> "LinkedList": # одновременное умножение и присваивание
		self._is_int(other)
		self = self*other
		return self  




	# ПРОВЕРКИ 
	def _is_valid_index(self, index):
		"""Проверка валидности индекса"""
		if not isinstance(index, int):
			raise TypeError
		if not 0 <= index < self.len:
			raise IndexError

	@staticmethod
	def _is_int(value):
		"""Проверка целочисленности"""
		if not isinstance(value, int): 
			raise TypeError	




	def step_by_step_on_nodes(self, index): 
		"""Получение элемента списка по индексу"""
		self._is_valid_index(index)

		current_node = self.head
		for i in range(index):
			current_node = current_node.next

		return current_node

	@staticmethod
	def linked_nodes(left_node, right_node): 
		"""Связывание узлов односвязного списка"""
		left_node.next = right_node
	




	def append(self, value): 
		"""Добавление элемента в конец списка"""
		append_node = self.NODE_TYPE(value) # создаем экземпляр класса NODE_TYPE и присваеваем переменной append_node
		if self.head is None:
			self.head = self.tail = append_node
		else:
			self.linked_nodes(self.tail, append_node)
			self.tail = append_node
		self.len += 1


	def insert(self, index, value):
		self._is_int(index)
		# negative index

		insert_node = self.NODE_TYPE(value) # создаем узел, тип вставляемого узла зависит от типа списка

		if index == 0: # указан нулевой индекс
			self.linked_nodes(insert_node, self.head) # связываем созданный узел и узел-голову
			self.head = insert_node # превращаем в голову созданный узел
			self.len += 1 # увеличиваем длинну

		elif index > self.len-1: # указан индекс равный или превышающий размер последовательности
			self.append(value) # добавляем значение в конец списка

		else: # указан не нулевой и не равный размеру последовательности индекс 
			prev_node = self.step_by_step_on_nodes(index-1) # индекс перед тем который будет сдвигаться вправо
			current_node = prev_node.next # узел который будет сдвигаться вправо
			self.linked_nodes(prev_node, insert_node) # соединяем предыдущий и созданный узел. 
			self.linked_nodes(insert_node, current_node) # соединяем созданный узел и узел на мето которого происходит вставка
			self.len += 1 # увеличиваем длинну списка
		

	def index(self, value):
		"""Ищет элемент в списке и возвращает его индекс"""

		for i, v in enumerate(self):
			if v == value:
				return i
		else:
			raise ValueError(f'{value} is not in the list')


	def remove(self, value):
		"""Удаляет из списка указанный элемент, первый который встретиться"""
		for i, v in enumerate(self):
			if v == value:
				del self[i]
				break
		else:
			raise ValueError(f'{value} is not in the list')


	def count(self, value):
		"""Возвращает сколько раз значение появляется в списке"""
		if value in self:
			counter = 0
			for i in range(self.len):
				node = self.step_by_step_on_nodes(i)
				if node.value == value:
					counter += 1
			return counter
		else:
			return 0


	def extend(self, obj):
		"""дополняет список элементами из указанного объекта"""
		try:
			iter(obj)
		except:
			raise TypeError(f"'{obj.__class__.__name__}' is not iterable")
		
		if obj == self: 
			counter = 0
			len_ = self.len
			for i in obj:
				self.append(i)
				counter +=1
				if counter == len_:
					break
		else:
			for i in obj:
				self.append(i)


	def pop(self, index=None):
		"""Возвращает элемент [на указанной позиции], удаляя его из списка.
		   Если элемент не указан, считается что имеется в виду последний элемент
		"""
		if not isinstance(index, (int, type(None))):
			raise TypeError

		if not index == None:
			if not 0 <= index < self.len:
				raise IndexError

		if index is None:
			node = self.tail 
			del self[self.len - 1]

		else:
			node = self.step_by_step_on_nodes(index)
			del self[index]
		
		return node.value


	def clear(self):
		"""Очистка списка"""
		self.head = None
		self.tail = None
		self.len = 0


	def nodes_iterator(self) -> 'Iterator':
		current_node = self.head # первый узел это head
		for i in range(self.len): # количество итераций равно длинне
			yield current_node # на каждой итерации в генератор добавляется узел
			current_node = current_node.next # следующий узел определяется по атрибуту next текущего узла


	def __contains__(self, value):
		for node in self.nodes_iterator(): # для узлов в генераторе
			if node.value == value: # значение узла равно значению слева от in
				return True
		return False



class DoubleLinkedList(LinkedList):
	NODE_TYPE = DoubleLinkedNode

	@staticmethod
	def linked_nodes(left_node, right_node):
		"""Связывание узлов двусвязного списка"""
		left_node.next = right_node
		right_node.prev = left_node




	








