import os, glob

class Iterator:
	def __init__(self):
		self._dir = os.getcwd()
		self._rec = True
		self._disallowed_ext = ['.db','','.pyc']
		
	def setDirectory(self,dir): 
		if os.path.isdir(dir) is False:
			raise NotADirectoryError(errno.ENOENT, os.strerror(errno.ENOENT), dir)
		self._dir = dir
		
	def setRecursive(self,rec): 
		self._rec = rec
		
	def setDisallowedExtensions(self,arr):
		self._disallowed_ext = arr
		
	def getAll(self):
		files = glob.glob(os.path.join(self._dir,'**'),recursive=self._rec)
		arr = []
		for file in files:
			if self._filter(file):
				arr.append(file)
		return arr
		
	def _filter(self,path):
		if os.path.isfile(path) is False:
			return False
		ext = os.path.splitext(path)[1]
		if ext in self._disallowed_ext:
			return False
		return True

def main():
	fi = Iterator()
	fi.setDirectory('../')
	print(fi.getAll())
	
if __name__ == '__main__':
	main()