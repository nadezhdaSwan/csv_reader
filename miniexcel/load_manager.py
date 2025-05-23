from pathlib import Path
import csv
from typing import List
import wx

class LoadManager():
	"""docstring for LoadManager"""
	def __init__(self, workdir: str):
		self.workdir = Path(workdir)

	def load(self, filename: str) -> List[List[str]]:
		with open(self.workdir / Path(filename)) as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			data = [[cell.strip() for cell in row] for row in reader]
			if data==[]:
				return [[]]
			else:
				return data



	def save(self, filename: str, data: List[List[str]]):
		with open(self.workdir / Path(filename), mode='w') as csvfile:
			csvfile_writer = csv.writer(csvfile, delimiter=',')
			for row in data:
				csvfile_writer.writerow(row)

