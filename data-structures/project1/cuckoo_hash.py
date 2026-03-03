# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[int]]]:
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		curr_key = key
		evictions = 0
		loop = True
		
		while loop == True:
			# 0 table
			zero_table_hash = self.hash_func(curr_key, 0)
			if self.tables[0][zero_table_hash] is None:
				self.tables[0][zero_table_hash] = curr_key
				return True
			else:
				temp_key = self.tables[0][zero_table_hash]
				self.tables[0][zero_table_hash] = curr_key
				curr_key = temp_key
				evictions += 1
			
			if evictions > self.CYCLE_THRESHOLD:
				loop = False
				return False
			
			# 1 table
			one_table_hash = self.hash_func(curr_key, 1)
			if self.tables[1][one_table_hash] is None:
				self.tables[1][one_table_hash] = curr_key
				return True
			else:
				temp_key = self.tables[1][one_table_hash]
				self.tables[1][one_table_hash] = curr_key
				curr_key = temp_key
				evictions += 1

			if evictions > self.CYCLE_THRESHOLD:
				loop = False
				return False
		
		return False

	def lookup(self, key: int) -> bool:
		# 0 table
		zero_table_hash = self.hash_func(key, 0)
		if self.tables[0][zero_table_hash] == key:
			return True
		
		# 1 table
		one_table_hash = self.hash_func(key, 1)
		if self.tables[1][one_table_hash] == key:
			return True
		
		return False
		

	def delete(self, key: int) -> None:
		# 0 table
		zero_table_hash = self.hash_func(key, 0)
		if self.tables[0][zero_table_hash] == key:
			self.tables[0][zero_table_hash] = None
			return
		
		# 1 table
		one_table_hash = self.hash_func(key, 1)
		if self.tables[1][one_table_hash] == key:
			self.tables[1][one_table_hash] = None
			return
		
		return

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		
		old = []
		for table in self.tables:
			for element in table:
				if element is not None:
					old.append(element)
		
		self.tables = [[None]*new_table_size for _ in range(2)]
		
		for element in old:
			self.insert(element)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define