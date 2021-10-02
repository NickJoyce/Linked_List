import sys

import weakref 

class Node():
	def __init__(self, value, next_=None):
		self.value = value
		self.next = None 

	def __repr__(self):
		return f'{self.__class__.__name__}({self.value}, {self.next})'

	def __str__(self):
		return f'{self.value}'

	# def __del__(self):
	# 	print('Вызван метод \"__del__\"')

	@classmethod
	def is_valid(cls, node):
		if not isinstance(node, (cls, type(None))):
			raise TypeError

	@property
	def next(self):
		return self._next

	@next.setter
	def next(self, node):
		self.is_valid(node)
		self._next = node



class DoubleLinkedNode(Node):
	def __init__(self, value, next_=None, prev=None):
		super().__init__(value, next_)
		self.prev = None

	def __repr__(self):
		return f'{self.__class__.__name__}({self.value}, {self.next}, {self.prev})'

	@property
	def prev(self):
		return None if self._prev is None else self._prev # при получении знаения атрибута prev
														  # вернуть None если self._prev = None?
														  # иначе вернуть self._prev

	@prev.setter
	def prev(self, prev):
		self.is_valid(prev)
		self._prev = None if prev is None else weakref.ref(prev) # при установке значения атрибута prev
																 # self._prev = None если присваемое значение None
																 # если присваиваемое значение не None создаем слабую ссылку

if __name__ == "__main__":
	print("__________class Node__________")
	node1, node2, node3  = Node(10), Node(20), Node(30)
	print('Значения узлов (выводится __str__):')
	print(node1, node2, node3, '\n')

	node_list = [node1, node2, node3]
	print('Узлы в списке (выводится __repr__):')
	print(node_list, '\n')

	# запись атрибута next
	node1.next = node2
	node2.next = node3

	print('Узлы в списке c добавленными атрибутами next:')
	print(node_list, '\n')


	print("__________class DoubleLinkedNode__________")
	node1, node2, node3  = DoubleLinkedNode(100), DoubleLinkedNode(200), DoubleLinkedNode(300)
	print(node1, node2, node3, '\n')

	node_list = [node1, node2, node3]
	print('Узлы в списке (выводится __repr__):')
	print(node_list, '\n')


	# запись атрибутов next и prev
	node1.next = node2
	node2.prev = node1
	node2.next = node3
	node3.prev = node2

	print('Узлы в списке c добавленными атрибутами next и prev:')
	print(node_list, '\n')

	for node in node_list: # количество ссылок на объект
		node_ref = 1
		next_ref = 1
		getrefcount_ref = 1
		node_in_loop_ref = 1
		print(sys.getrefcount(node) - node_ref - next_ref - getrefcount_ref - node_in_loop_ref)


	







