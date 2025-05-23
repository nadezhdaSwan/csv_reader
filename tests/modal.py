import unittest
import os
from pathlib import Path

from miniexcel.load_manager import LoadManager
from miniexcel.main import work_dir



class DowloadCSV(unittest.TestCase):

	def test_csv_load_and_save_file(self):

		load_manader = LoadManager(work_dir)
		data = load_manader.load('biostats.csv')

		self.assertEqual(data[0],['Name', 'Gender', 'Age', 'Height', 'Weight'])

		newfile = 'biostats_new.csv'
		load_manader.save(newfile, data)
		data_new = load_manader.load(newfile)
		self.assertEqual(data,data_new)

		os.remove(Path(work_dir)/Path(newfile))

	def test_open_not_csv(self):
		load_manader = LoadManager(work_dir)
		data = load_manader.load('error_file.txt')
		self.assertEqual(data,[[]])

	def test_open_empty_csv(self):
		load_manader = LoadManager(work_dir)
		data = load_manader.load('empty.csv')
		self.assertEqual(data,[[]])

	def test_open_wrong_delimiter(self):
		load_manader = LoadManager(work_dir)
		data = load_manader.load('wrong_delim.csv')
		self.assertEqual(data,[['7;8;9'], ['40']])



	def test_open_wrong_file(self):
		load_manader = LoadManager(work_dir)
		data = load_manader.load('wrong_file.csv')
		#print(data)



