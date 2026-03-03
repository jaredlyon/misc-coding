import random as rand
from typing import List, Optional

class CuckooHash24:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.bucket_size = 4
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.table = [None] * init_size


	def get_rand_idx_from_bucket(self, bucket_idx: int, table_id: int) -> int:
		rand.seed(int(str(bucket_idx) + str(table_id)))
		return rand.randint(0, self.bucket_size - 1)
	

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size - 1)
	

	def get_table_contents(self) -> List[List[Optional[List[int]]]]:
		return [self.table]


	def insert(self, key: int) -> bool:
		curr_key = key
		evictions = 0
		
		while evictions <= self.CYCLE_THRESHOLD:
			hash0 = self.hash_func(curr_key, 0)
			bucket0 = self.table[hash0]
			hash1 = self.hash_func(curr_key, 1)
			bucket1 = self.table[hash1]
			
			if bucket0 is None:
				self.table[hash0] = [curr_key]
				return True
			elif len(bucket0) < self.bucket_size:
				bucket0.append(curr_key)
				return True
			
			if bucket1 is None:
				self.table[hash1] = [curr_key]
				return True
			elif len(bucket1) < self.bucket_size:
				bucket1.append(curr_key)
				return True

			bucket_spot = self.get_rand_idx_from_bucket(hash0, 0)
			temp_key = bucket0[bucket_spot]
			bucket0[bucket_spot] = curr_key
			curr_key = temp_key
			evictions += 1
		
		return False
	

	def lookup(self, key: int) -> bool:
		hash0 = self.hash_func(key, 0)
		bucket = self.table[hash0]
		if bucket is not None and key in bucket:
			return True
		
		hash1 = self.hash_func(key, 1)
		bucket = self.table[hash1]
		if bucket is not None and key in bucket:
			return True
		
		return False
	

	def delete(self, key: int) -> None:
		hash0 = self.hash_func(key, 0)
		bucket = self.table[hash0]
		if bucket is not None and key in bucket:
			bucket.remove(key)
			if len(bucket) == 0:
				self.table[hash0] = None
			return
		
		hash1 = self.hash_func(key, 1)
		bucket = self.table[hash1]
		if bucket is not None and key in bucket:
			bucket.remove(key)
			if len(bucket) == 0:
				self.table[hash1] = None
			return
		

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		
		old = []
		for bucket in self.table:
			if bucket is not None:
				for key in bucket:
					old.append(key)

		self.table = [None] * new_table_size

		for key in old:
			self.insert(key)