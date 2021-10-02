class LinkedListIterator:
	"""Итератор для LinkedList"""
	def __init__(self, head, len_):
		self.next_node = head # узел содержит ссылки на все остальные узлы
		self.len = len_ # длинна LinkedList
		self.counter = 1 # счетчик количества проходов


	def __iter__(self):
		return self

	def __next__(self):
		if self.counter > self.len: # количество проходов больше элементов в списке
			raise StopIteration
		else:
			current_node = self.next_node # текущий узел равен следующему
			self.next_node = current_node.next # следующий узел равен атрибуту next текущего
			self.counter += 1 # увеличиваем счетчик
		return current_node.value