import os,errno,logging

class Virtual:
	def __init__(self,datetime,path,camera,lat,lng,width,height,mbytes,orientation,old_dir,old_file):
		self._datetime = datetime
		self._path = path
		self._camera = camera
		self._lat = lat
		self._lng = lng
		self._width = width
		self._height = height
		self._mbytes = mbytes
		self._orientation = orientation
		self._old_dir = old_dir
		self._old_file = old_file
	
	@classmethod
	def constructFromPhysical(cls,f,new_path_part):
		return cls(f.getDatetime(),new_path_part,f.getCamera(),f.getLat(),f.getLng(),f.getWidth(),f.getHeight(),f.getMBytes(),f.getOrientation(),f.getDirName(),f.getName())
	
	def __cmp__(self,other):
		return cmp(self._datetime,other._datetime)
		
	def __eq__(self, other):
		return self._datetime == other._datetime

	def __lt__(self, other):
		return self._datetime < other._datetime
		
	def getName(self):
		return str(os.path.basename(self._path))