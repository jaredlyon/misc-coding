# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash24:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.bucket_size = 4
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def get_rand_idx_from_bucket(self, bucket_idx: int, table_id: int) -> int:
		# you must use this function when you need to displace a random key from a bucket during insertion (see the description in requirements.py). 
		# this function randomly chooses an index from a given bucket for a given table. this ensures that the random 
		# index chosen by your code and our test script match.
		# 
		# for example, if you are inserting some key x into table 0, and hash_func(x, 0) returns 5, and the bucket in index 5 of table 0 already has 4 elements,
		# you will call get_rand_bucket_index(5, 0) to determine which key from that bucket to displace, i.e. if get_random_bucket_index(5, 0) returns 2, you
		# will displace the key at index 2 in that bucket.
		rand.seed(int(str(bucket_idx) + str(table_id)))
		return rand.randint(0, self.bucket_size-1)

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[List[int]]]]:
		# the buckets should be implemented as lists. Table cells with no elements should still have None entries.
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
			zero_bucket = self.tables[0][zero_table_hash]
			
			if zero_bucket is None:
				self.tables[0][zero_table_hash] = [curr_key]
				return True
			elif len(zero_bucket) < self.bucket_size:
				zero_bucket.append(curr_key)
				return True
			else:
				bucket_idx = self.get_rand_idx_from_bucket(zero_table_hash, 0)
				temp_key = zero_bucket[bucket_idx]
				zero_bucket[bucket_idx] = curr_key
				curr_key = temp_key
				evictions += 1
			
			if evictions > self.CYCLE_THRESHOLD:
				loop = False
				return False
			
			# 1 table
			one_table_hash = self.hash_func(curr_key, 1)
			one_bucket = self.tables[1][one_table_hash]
			
			if one_bucket is None:
				self.tables[1][one_table_hash] = [curr_key]
				return True
			elif len(one_bucket) < self.bucket_size:
				one_bucket.append(curr_key)
				return True
			else:
				bucket_idx = self.get_rand_idx_from_bucket(one_table_hash, 1)
				temp_key = one_bucket[bucket_idx]
				one_bucket[bucket_idx] = curr_key
				curr_key = temp_key
				evictions += 1

			if evictions > self.CYCLE_THRESHOLD:
				loop = False
				return False
		
		return False
		

	def lookup(self, key: int) -> bool:
		# 0 table
		zero_table_hash = self.hash_func(key, 0)
		bucket = self.tables[0][zero_table_hash]
		if bucket is not None and key in bucket:
			return True
		
		# 1 table
		one_table_hash = self.hash_func(key, 1)
		bucket = self.tables[1][one_table_hash]
		if bucket is not None and key in bucket:
			return True
		
		return False
		

	def delete(self, key: int) -> None:
		# 0 table
		zero_table_hash = self.hash_func(key, 0)
		bucket = self.tables[0][zero_table_hash]
		if bucket is not None and key in bucket:
			bucket.remove(key)
			if len(bucket) == 0:
				self.tables[0][zero_table_hash] = None
			return
		
		# 1 table
		one_table_hash = self.hash_func(key, 1)
		bucket = self.tables[1][one_table_hash]
		if bucket is not None and key in bucket:
			bucket.remove(key)
			if len(bucket) == 0:
				self.tables[1][one_table_hash] = None
			return
		

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
				
		# old = []
		# for table in self.tables:
		# 	for element in table:
		# 		if element is not None:
		# 			old.append(element)
		
		# self.tables = [[None]*new_table_size for _ in range(2)]
		
		# for element in old:
		# 	self.insert(element)

		old = []
		for table in self.tables:
			for bucket in table:
				if bucket is not None:
					for key in bucket:
						old.append(key)

		self.tables = [[None] * new_table_size for _ in range(2)]

		for key in old:
			self.insert(key)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define