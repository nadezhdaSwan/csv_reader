import unittest
import os
from pathlib import Path


class DowloadCSV(unittest.TestCase):

	def test_csv_load_and_save_file(self):
		from miniexcel.load_manager import LoadManager
		from miniexcel.main import work_dir

		load_manader = LoadManager(work_dir)
		data = load_manader.load('biostats.csv')
		self.assertEqual(data[0],['Name', 'Gender', 'Age', 'Height', 'Weight'])

		newfile = 'biostats_new.csv'
		load_manader.save(newfile, data)
		data_new = load_manader.load(newfile)
		self.assertEqual(data,data_new)

		os.remove(Path(work_dir)/Path(newfile))

	





