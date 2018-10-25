import os,argparse,logging

from virtuallist import VirtualList
from physicallist import PhysicalList
from tuplelist import TupleList
from rename2creationtime import Rename2Creationtime
from merge import Merge

class FileOrganizer:

	def __init__(self):
		self._args = self._getArgs()
		self._setLogging()
		
	## Get command line arguments with argparse
	def _getArgs(self):
		argparser = argparse.ArgumentParser()
		argparser.add_argument('action', default=None, help="print_config/create_csv/check_corruption/src_stats/rename2creation/merge")
		argparser.add_argument('-s', '--src-dir', default=None, help="Source directory")
		argparser.add_argument('-d', '--dst-dir', default=None, help="Destination directory")
		argparser.add_argument('-c', '--csv-file', default=None, help="CSV file")
		argparser.add_argument('-p', '--preview', action='store_true', help="Preview changes without performing them")
		argparser.add_argument('-l', '--logging-level', default="warning", help="debug/info/warning/error/critical, default='warning'")
		return argparser.parse_args()
		
	## Set logging level
	def _setLogging(self):
		ll = self._args.logging_level
		if ll == "critical": level = logging.CRITICAL
		elif ll == "error": level = logging.ERROR
		elif ll == "warning": level = logging.WARNING
		elif ll == "info": level = logging.INFO
		elif ll == "debug": level = logging.DEBUG
		else: level = logging.WARNING
		logging.basicConfig(format="%(levelname)s: %(message)s",level=level)
		
	def printConfig(self):
		print('Source directory:', self._args.src_dir)
		print('Destination directory:', self._args.dst_dir)
		print('Preview:', self._args.preview)
		print('Logging level:', self._args.logging_level)
		
	def createEmptyCSV(self):
		try:
			VirtualList.createEmptyCSV(self._args.csv_file)
		except RuntimeError as e:
			logging.error(e)
	
	def checkCorruption(self):
		if self._args.dst_dir is None:
			logging.error('Destination directory not set')
		elif self._args.csv_file is None:
			logging.error('CSV file not set')
		else:
			tl = TupleList(self._args.csv_file,self._args.dst_dir)
			print('Antal saknade virtuella:',tl.getNrMissingVirtual())
			print('Antal saknade fysiska:',tl.getNrMissingPhysical())
		
	def checkSourceStats(self):
		if self._args.src_dir is None:
			logging.error('Source directory not set')
		else:
			pl = PhysicalList(self._args.src_dir)
			pl.summary()
			
	def rename2creation(self):
		if self._args.src_dir is None:
			logging.error('Source directory not set')
		else:
			r = Rename2Creationtime(self._args.src_dir)
			r.rename(self._args.preview)
			
	def merge(self):
		if self._args.src_dir is None:
			logging.error('Source directory not set')
		elif self._args.csv_file is None:
			logging.error('CSV file not set')
		elif self._args.dst_dir is None:
			logging.error('Destination directory not set')
		else:
			m = Merge(self._args.csv_file,self._args.src_dir,self._args.dst_dir)
			m.merge(self._args.preview)
		
	def getAction(self):
		return self._args.action
		
def main():
	fo = FileOrganizer()
	action = fo.getAction()
	
	if action is None:
		logging.error('No action specified')
	elif action == 'print_config':
		fo.printConfig()
	elif action == 'create_csv':
		fo.createEmptyCSV()
	elif action == 'check_corruption':
		fo.checkCorruption()
	elif action == 'src_stats':
		fo.checkSourceStats()
	elif action == 'rename2creation':
		fo.rename2creation()
	elif action == 'merge':
		fo.merge()
	
	
if __name__ == '__main__':
	main()
	