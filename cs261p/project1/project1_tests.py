import requirements
import random as rand

# Instructions
# Some test cases for the CuckooHash class can be found below.
#
# Note that the test cases here are just to give an idea of how we will test your submissions, so passing these tests does not mean that your code is correct.
# It is a good idea to try and create different test cases with different table sizes to fully test your implementation.

def cuckoo_hash_tests():
	print("starting test 1")

	input_size, table_size = 10, 10
	nums = [i for i in range(input_size)]
	
	c = requirements.CuckooHash(table_size)
	for num in nums:
		print("inserting %d" % num)
		no_cycle = c.insert(num)
		if no_cycle == False:
			print("error: cycle should not exist")

	for num in nums[:5]:
		print("deleting %d" % num)
		c.delete(num)
		if c.lookup(num):
			print("error: %d should not exist in cuckoo hash" %num)

	ref_ans = [[None, None, 7, None, 6, None, None, 8, None, 9], [None, None, None, None, 5, None, None, None, None, None]]

	if not c.get_table_contents() == ref_ans:
		print("test 1 table contents incorrect")
		return

	print("\ntest 1 table contents correct")

	print("\n\nstarting test 2")

	input_size, table_size = 20, 10
	nums = [i for i in range(input_size)]

	c = requirements.CuckooHash(table_size)
	for num in nums:
		# there should be a cycle when inserting 15
		print("inserting %d" % num)
		no_cycle = c.insert(num)
		if no_cycle == False:
			print("found cycle when inserting %d" %num)
			break

	ref_ans = [[2, None, 14, None, 12, 13, 10, 5, None, 9], [None, 8, 0, 15, 7, 11, 3, 4, None, 1]]

	if not c.get_table_contents() == ref_ans:
		print("test 2 table contents incorrect")
		return

	c.rehash(20)
	ref_ans = [[None, None, 12, None, 4, None, None, 13, None, 14, None, None, 1, None, None, 11, None, 3, 0, 9], [None, None, 8, 5, None, 15, None, None, None, None, None, 10, None, None, None, None, None, None, 2, 7]]

	if not c.get_table_contents() == ref_ans:
		print("test 2 table contents incorrect")
		return

	print("\ntest 2 table contents correct")

	print("\nstarting test 3")

	keys = [16, 708, 310, 728, 613, 204, 154, 642, 607, 938,
	        273, 643, 980, 697, 976, 288, 176, 204, 759, 749]

	c = requirements.CuckooHash(10)

	for k in keys:
		ok = c.insert(k)
		if not ok:
			print(f"cycle detected when inserting {k}, rehashing")
			c.rehash(c.table_size * 2)
			ok = c.insert(k)
			if not ok:
				print(f"failed to insert {k} even after rehash")
				return

	print("\nfinal table contents:")
	tables = c.get_table_contents()
	for t_id, table in enumerate(tables):
		print(f"table {t_id}:")
		for idx, bucket in enumerate(table):
			print(f"  {idx}: {bucket}")
	
	print("test 3 complete")

	print("starting test 4")

	keys = [583, 130, 124, 816, 700, 604, 672, 470, 237, 709,
	        600, 53, 866, 568, 838, 879, 989, 491, 679, 679]

	c = requirements.CuckooHash(10)

	for k in keys:
		ok = c.insert(k)
		if not ok:
			print(f"cycle detected when inserting {k}, rehashing")
			c.rehash(c.table_size * 2)
			ok = c.insert(k)
			if not ok:
				print(f"failed to insert {k} even after rehash")
				return

	print("\nfinal table contents:")
	tables = c.get_table_contents()
	for t_id, table in enumerate(tables):
		print(f"table {t_id}:")
		for idx, bucket in enumerate(table):
			print(f"  {idx}: {bucket}")

	print("test 4 complete")

if __name__ == '__main__':
	cuckoo_hash_tests()

