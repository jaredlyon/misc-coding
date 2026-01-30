import requirements
import random as rand

# Instructions
# Some test cases for the CuckooHash24 class can be found below.
#
# Note that the test cases here are just to give an idea of how we will test your submissions, so passing these tests does not mean that your code is correct.
# It is a good idea to try and create different test cases with different table sizes to fully test your implementation.

def cuckoo_hash_tests():
	print("starting test 1")

	input_size, table_size = 10, 10
	nums = [i for i in range(input_size)]
	
	c = requirements.CuckooHash24(table_size)
	for num in nums:
		no_cycle = c.insert(num)
		if no_cycle == False:
			print("error: cycle should not exist")

	for num in nums[:5]:
		print("deleting %d" % num)
		c.delete(num)
		if c.lookup(num):
			print("error: %d should not exist in cuckoo hash" %num)

	ref_ans = [[None, None, [7], None, [6], None, None, [5, 8], None, [9]], [None, None, None, None, None, None, None, None, None, None]]

	if not c.get_table_contents() == ref_ans:
		print("test 1 table contents incorrect")
		return
	print("\ntest 1 table contents correct")

	print("\n\nstarting test 2")

	input_size, table_size = 20, 10
	nums = [i for i in range(input_size*4)]

	c = requirements.CuckooHash24(table_size)
	for num in nums:
		# there should be a cycle when inserting 71
		no_cycle = c.insert(num)
		if no_cycle == False:
			print("found cycle when inserting %d" %num)
			break

	ref_ans = [[[2, 11, 16, 44], [68, 39, 47, 53], [1, 7, 14, 30], [27, 36, 62, 55], [4, 6, 12, 49], [13, 18, 22, 69], [0, 10, 40, 35], [59, 8, 20, 23], [26, 28, 63, 43], [3, 54, 32, 41]], [[24], [37, 29, 67, 70], [25, 46, 45, 64], [15, 33, 56, 38], [5, 52, 48, 66], [21, 58, 60], [31, 34, 9, 61], [17, 42], [19, 51], [50, 57, 65]]]

	if not c.get_table_contents() == ref_ans:
		print("test 2 table contents incorrect")
		return
	
	c.rehash(20)
	ref_ans = [[[39, 47, 37, 38], [19], [68, 12, 49, 18], [62, 22, 21, 24], [4, 40, 20, 56], [44, 42], [36, 54, 32], [13], [48, 58, 34, 51], [16, 50, 55, 23], [45, 66, 60], [59, 33, 52], [2, 17, 1, 7], [61, 65], [6, 57], [11, 35, 26, 31], [27, 25], [30, 3, 5], [69, 0, 8], [10, 64, 9]], [[28], None, None, [14], None, [15], None, [46], None, None, None, [43, 70], None, [63], None, [29, 67], None, None, [41], [53]]]

	if not c.get_table_contents() == ref_ans:
		print("test 2 table contents incorrect")
		return
	print("\ntest 2 table contents correct")

	print("\nstarting test 3")

	c = requirements.CuckooHash24(10)

	for i in range(50):
		ok = c.insert(67)
		if not ok:
			break
	else:
		print("test 3 seems wrong - cycle threshold should have been hit")

	if not c.lookup(67):
		print("test 3 seems wrong - there should still be data")

	print("test 3 complete")

	print("\nstarting test 4")

	c = requirements.CuckooHash24(10)
	inserted = []

	for i in range(100):
		ok = c.insert(i)
		if not ok:
			c.rehash(20)
			ok = c.insert(i)
			if not ok:
				print("test 4 seems wrong - could not insert after rehash")
				return
		inserted.append(i)

	for k in inserted:
		if not c.lookup(k):
			print(f"test 4 seems wrong - could not find key {k}")

	print("test 4 complete")

	print("\nstarting test 5")

	table_size = 10
	c = requirements.CuckooHash24(table_size)

	i = 0
	while i < 80:
		gud = c.insert(i)
		if not gud:
			c.rehash(c.table_size * 2) # trigger rehash
			print(f"rehash at {i} - this should match test 6")
			continue
		i += 1

	tables = c.get_table_contents()

	for table in enumerate(tables):
		for bucket in enumerate(table):
			if bucket is not None and len(bucket) > 4:
				print(f"test 5 seems wrong - bigg bucket")
				return

	print("test 5 complete")

	print("\nstarting test 6")

	c = requirements.CuckooHash24(10)

	count = 0
	for i in range(80):
		if not c.insert(i):
			print(f"test 6 cycle detected at insert {i}")
			break
		count += 1

	print(f"test 6 complete - {count} inserts before cycle")

	print("\nstarting test 7")

	keys = [16, 708, 310, 728, 613, 204, 154, 642, 607, 938,
	        273, 643, 980, 697, 976, 288, 176, 204, 759, 749]

	c = requirements.CuckooHash24(10)

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
	
	print("test 7 complete")

	print("starting test 8")

	keys = [583, 130, 124, 816, 700, 604, 672, 470, 237, 709,
	        600, 53, 866, 568, 838, 879, 989, 491, 679, 679]

	c = requirements.CuckooHash24(10)

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

	print("test 8 complete")

if __name__ == '__main__':
	cuckoo_hash_tests()

