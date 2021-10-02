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











if __name__ == '__main__':

	ll = LinkedList([1,2,3])
	dll = DoubleLinkedList([10,20,30])

	def test_several_iterators():
		"""Создание несколько итераторов"""
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		try:
			iter_1 = iter(ll)
			iter_2 = iter(ll)
			for i in range(len(ll)):
				next(iter_1)
			for i in range(len(ll)):
				next(iter_2)
			result['ll'] = 'SUCCESS'
		except:
			pass
		try:
			iter_1 = iter(dll)
			iter_2 = iter(dll)
			for i in range(len(dll)):
				next(iter_1)
			for i in range(len(dll)):
				next(iter_2)
			result['dll'] = 'SUCCESS'			
		except:
			pass
		return result

	def test_stop_iteration():
		"""Вызов StopIteration"""
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		iter_1 = iter(ll)
		try:
			for i in range(len(ll)+1):
				next(iter_1)
		except StopIteration:
			result['ll'] = 'SUCCESS'

		iter_1 = iter(dll)
		try:
			for i in range(len(dll)+1):
				next(iter_1)
		except StopIteration:
			result['dll'] = 'SUCCESS'
		return result

	def test__getitem__():
		"""Вызов __getitem__"""
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		if ll[0] == 1 and ll[1] == 2 and ll[2] == 3:
			result['ll'] = 'SUCCESS'
		if dll[0] == 10 and dll[1] == 20 and dll[2] == 30:
			result['dll'] = 'SUCCESS'
		return result

	def test__setitem__():
		"""Вызов __setitem__"""
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		ll_copy = copy.deepcopy(ll)
		ll_copy[0] = 100
		ll_copy[1] = 100
		ll_copy[2] = 100
		if str(ll_copy) == '[100, 100, 100]':
			result['ll'] = 'SUCCESS'

		dll_copy = copy.deepcopy(dll)
		dll_copy[0] = 100
		dll_copy[1] = 100
		dll_copy[2] = 100
		if str(dll_copy) == '[100, 100, 100]':
			result['dll'] = 'SUCCESS'
		
		return result

	def test__delitem__():
		"""Вызов __delitem_"""
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		ll_copy = copy.deepcopy(ll)
		list_ = []
		del ll_copy[0]
		list_ += [str(ll_copy) == '[2, 3]', ll_copy.head.value == 2, ll_copy.tail.value == 3]
		del ll_copy[0]
		list_ += [str(ll_copy) == '[3]', ll_copy.head.value == 3, ll_copy.tail.value == 3]
		del ll_copy[0]
		list_ += [str(ll_copy) == '[]', None==None, None==None]

		if all(list_):
			result['ll'] = 'SUCCESS'

		dll_copy = copy.deepcopy(dll)
		list_ = []
		del dll_copy[0]
		list_ += [str(dll_copy) == '[20, 30]', dll_copy.head.value == 20, dll_copy.tail.value == 30]
		del dll_copy[0]
		list_ += [str(dll_copy) == '[30]', dll_copy.head.value == 30, dll_copy.tail.value == 30]
		del dll_copy[0]
		list_ += [str(dll_copy) == '[]', None==None, None==None]

		if all(list_):
			result['dll'] = 'SUCCESS'
		return result

	def test__add__():
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		ll_1 = copy.deepcopy(ll)
		ll_2 = copy.deepcopy(ll)
		ll_3 = ll_1+ll_2
		if str(ll_3) == '[1, 2, 3, 1, 2, 3]':
			result['ll'] = 'SUCCESS'

		dll_1 = copy.deepcopy(dll)
		dll_2 = copy.deepcopy(dll)
		dll_3 = dll_1+dll_2
		if str(dll_3) == '[10, 20, 30, 10, 20, 30]':
			result['dll'] = 'SUCCESS'
		return result

	def test__radd__():
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		new_ll = [7,8,9] + ll
		if isinstance(new_ll, LinkedList) and '[7, 8, 9, 1, 2, 3]' == str(new_ll):
			result['ll'] = 'SUCCESS'


		new_dll = [7,8,9] + dll
		if isinstance(new_dll, DoubleLinkedList) and '[7, 8, 9, 10, 20, 30]' == str(new_dll):
			result['dll'] = 'SUCCESS'
		return result

	def test__iadd__():
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		ll_1 = LinkedList([1,2,3])
		ll_2 = LinkedList([4,5,6])
		ll_1 += ll_2
		if isinstance(ll_1, LinkedList) and str(ll_1) == '[1, 2, 3, 4, 5, 6]':
			result['ll'] = 'SUCCESS'

		dll_1 = DoubleLinkedList([1,2,3])
		dll_2 = DoubleLinkedList([7,8,9])
		dll_1 += dll_2
		if isinstance(dll_1, DoubleLinkedList) and str(dll_1) == '[1, 2, 3, 7, 8, 9]':
			result['dll'] = 'SUCCESS'
		return result

	def test__mul__():
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		list_ = [1,2,3]
		ll_1 = LinkedList(list_)
		new_ll = ll_1*3
		if isinstance(new_ll, LinkedList) and str(new_ll) == str(list_*3):
			result['ll'] = 'SUCCESS'

		list_ = [10,20,30]
		dll_1 = DoubleLinkedList(list_)
		new_dll = dll_1*3
		if isinstance(new_dll, DoubleLinkedList) and str(new_dll) == str(list_*3):
			result['dll'] = 'SUCCESS'
		return result

	def test__rmul__():
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		new_ll = 2*ll
		if isinstance(new_ll, LinkedList) and str(new_ll) == '[1, 2, 3, 1, 2, 3]':
			result['ll'] = 'SUCCESS'

		new_dll = 2*dll
		if isinstance(new_dll, DoubleLinkedList) and str(new_dll) == '[10, 20, 30, 10, 20, 30]':
			result['dll'] = 'SUCCESS'
		return result

	def test__imul__():
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		ll_1 = LinkedList([1,2,3])
		ll_1 *= 2
		if isinstance(ll_1, LinkedList) and str(ll_1) == '[1, 2, 3, 1, 2, 3]':
			result['ll'] = 'SUCCESS'
		
		dll_1 = DoubleLinkedList([10,20,30])
		dll_1 *= 2
		if isinstance(dll_1, DoubleLinkedList) and str(dll_1) == '[10, 20, 30, 10, 20, 30]':
			result['dll'] = 'SUCCESS'	
		return result

	def test_append_empty_list():
		"""Добавление в пустой LinkedList"""
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		list_types = [LinkedList, DoubleLinkedList]
		for list_type in list_types:
			empty_ll = list_type([])
			empty_ll.append(5) 
			if all([empty_ll.head.value == 5, empty_ll.tail.value == 5, empty_ll.len == 1, isinstance(empty_ll, list_type)]):
				if list_type == LinkedList:
					result['ll'] = 'SUCCESS' 
				if list_type == DoubleLinkedList:
					result['dll'] = 'SUCCESS'
		return result

	def test_insert_zero_index():
		"""Вставка по нулевому индексу"""
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		list_types = [LinkedList, DoubleLinkedList]
		for list_type in list_types:
			ll = list_type([1,2,3])
			ll.insert(0, 100)
			if all([ll.head.value == 100, # добавленное значение, крайнее левое
					ll.tail.value == 3, # значение у крайнего правого узла
					ll.len == 4, # дляинна списка
					ll.head.next.value == 1, # значение у следующего узла
					type(ll.head) == list_type.NODE_TYPE, # соответствует ли тип узла головы, типу узлов списка
					type(ll.tail) == list_type.NODE_TYPE, # соответствует ли тип узла хвоста, типу узлов списка
					]):
				if list_type == LinkedList:
					result['ll'] = 'SUCCESS' 
				if list_type == DoubleLinkedList:
					result['dll'] = 'SUCCESS'
		return result

	def test_insert_middle_index():
		"""Вставка по не первому и не последнему индексу"""
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		list_types = [LinkedList, DoubleLinkedList]
		for list_type in list_types:
			ll = list_type([1,2,3])
			ll.insert(1, 100)

			if all([ll[1] == 100, # добавленное значение по индексу 1
					ll.tail.value == 3, # значение у крайнего правого узла
					ll.len == 4, # длинна списка
					ll.head.next.value == 100, # значение у следующего за head узла
					type(ll.head) == list_type.NODE_TYPE, # соответствует ли тип узла головы, типу узлов списка
					type(ll.tail) == list_type.NODE_TYPE, # соответствует ли тип узла хвоста, типу узлов списка
					]):
				if list_type == LinkedList:
					result['ll'] = 'SUCCESS' 
				if list_type == DoubleLinkedList:
					result['dll'] = 'SUCCESS'
		return result

	def test_index():
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		list_types = [LinkedList, DoubleLinkedList]
		for list_type in list_types:
			ll = list_type(['x', 11, 4.5])
			value_error_test = False
			try:
				ll.index('non-exist value')
			except ValueError:
				value_error_test = True

			if all([ll.index('x')==0, ll.index(11)==1, ll.index(4.5)==2, value_error_test]):
				if list_type == LinkedList:
					result['ll'] = 'SUCCESS' 
				if list_type == DoubleLinkedList:
					result['dll'] = 'SUCCESS'
		return result

	def test_remove(): 
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		list_types = [LinkedList, DoubleLinkedList]
		for list_type in list_types:
			ll = list_type(['x', 11, 11, 4.5])
			value_error_test = False
			try:
				ll.remove('non-exist value')
			except ValueError:
				value_error_test = True
			ll.remove(11)
			if all([ll.head.value == 'x', ll.tail.value == 4.5, ll.len == 3, value_error_test]):
				if list_type == LinkedList:
					result['ll'] = 'SUCCESS' 
				if list_type == DoubleLinkedList:
					result['dll'] = 'SUCCESS'
		return result

	def test_count():
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		list_types = [LinkedList, DoubleLinkedList]
		for list_type in list_types:
			ll = list_type([1,2,3,4,5,8,5,5])
			ll.count(5)
			if ll.count(5) == 3:
				if list_type == LinkedList:
					result['ll'] = 'SUCCESS' 
				if list_type == DoubleLinkedList:
					result['dll'] = 'SUCCESS'
		return result

	def test_extend():
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		list_types = [LinkedList, DoubleLinkedList]
		for list_type in list_types:
			ll = list_type([1,2,3])
			list_ = [4,5,6]
			type_error_test = False
			try:
				ll.extend()
			except TypeError:
				type_error_test = True
			ll.extend(list_)
			if all([str(ll) == '[1, 2, 3, 4, 5, 6]', type_error_test]):
				if list_type == LinkedList:
					result['ll'] = 'SUCCESS' 
				if list_type == DoubleLinkedList:
					result['dll'] = 'SUCCESS'

		return result	

	def test_pop():
		result = {'ll': 'FAIL', 'dll': 'FAIL'}
		list_types = [LinkedList, DoubleLinkedList]
		for list_type in list_types:
			ll = list_type([1,2,3])
			ll.pop(0)
			ll.pop()
			print(ll)
			if ll.head.value == ll.tail.value == 2:
				if list_type == LinkedList:
					result['ll'] = 'SUCCESS' 
				if list_type == DoubleLinkedList:
					result['dll'] = 'SUCCESS'
		return result



	test_table = PrettyTable()
	tt = test_table
	tt.field_names = ["elements under test", "LinkedList", "DoubleLinkedList"] # column name
	tt._min_width = {"elements under test" : 40, "LinkedList" : 30, "DoubleLinkedList" : 30} # column width 
	tt.align["elements under test"] = "l" # text-align: left

	tests = [["__str__", {'ll': str(ll), 'dll': str(dll)}],
			 ["__repr__", {'ll': repr(ll), 'dll': repr(dll)}],
			 ["Создание нескольких итераторов", test_several_iterators()],
			 ["Вызов StopIteration", test_stop_iteration()],
			 ["__getitem__", test__getitem__()],
			 ["__setitem__", test__setitem__()],
			 ["__delitem__", test__delitem__()],
			 ["__add__", test__add__()],
			 ["__radd__", test__radd__()],
			 ["__iadd__", test__iadd__() ],
			 ["__mul__", test__mul__()],
			 ["__rmul__", test__rmul__()],
			 ["__imul__", test__imul__()],
			 ["append(): пустой лист", test_append_empty_list()],
			 ["insert(): нулевой индекс", test_insert_zero_index()],
			 ["insert(): не первый и не последний индекс", test_insert_middle_index()],
			 ["index()", test_index()],
			 ["remove()", test_remove()],
			 ["count()", test_count()],
			 ["extend()", test_extend()],
			 ["pop()", test_pop()]]

	for i in tests:
		element = i[0]
		res = i[1]
		tt.add_row([element, res['ll'], res['dll']])

	print(tt)


	








