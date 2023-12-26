import os
import errno
import logging
import exifread
import re
from datetime import datetime, timedelta
from PIL import Image


class Physical:
    def __init__(self, path):
        if os.path.isfile(path) is False:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), path)
        self._path = path
        self._filename = os.path.basename(self._path)
        self._dirname = os.path.basename(
            os.path.dirname(os.path.abspath(self._path)))
        self._mbytes = os.stat(self._path).st_size / \
            1000000  # os.path.getsize(self._path)
        self._ext = os.path.splitext(self._filename)[1]
        self._camera = ""
        self._orientation = ""
        self._lat = 0
        self._lng = 0
        self._width = 0
        self._height = 0
        self._datetime = ""
        self._is_loaded = False

    def __cmp__(self, other):
        return cmp(self._filename, other._filename)

    def __eq__(self, other):
        return self._filename == other._filename

    def __lt__(self, other):
        return self._filename < other._filename

    def loadInfo(self):
        if self._is_loaded:
            return

        try:
            im = Image.open(self._path)
            self._width, self._height = im.size
        except IOError:
            pass

        exif = exifread.process_file(open(self._path, 'rb'))
        if 'EXIF DateTimeOriginal' in exif:
            self._datetime = datetime.strptime(
                str(exif['EXIF DateTimeOriginal']), "%Y:%m:%d %H:%M:%S")
            self._datetime = self._datetime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            self._datetime = self._getDatetimeFromName()
            if self._datetime == "":
                self._datetime = self._getDatetimeIphoneClip()

        if 'Image Make' in exif:
            self._camera = exif['Image Make']
        if 'Image Orientation' in exif:
            self._orientation = str(exif['Image Orientation'])
        if 'GPS GPSLatitude' in exif:
            self._lat = str(exif['GPS GPSLatitude'])
        if 'GPS GPSLongitude' in exif:
            self._lng = str(exif['GPS GPSLongitude'])
        self._is_loaded = True

    def _getDatetimeFromName(self):
        strr = self._filename.rpartition('.')[0]
        match = re.search(
            '(^|_|-)(19|20)(\d\d)(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(-|_|)([01][0-9]|[2][0-3])([0-5][0-9])([012345][0-9])($|_|-)', strr)
        if match:
            return match.group(2)+match.group(3)+"-"+match.group(4)+"-"+match.group(5)+" "+match.group(7)+":"+match.group(8)+":" + match.group(9)
        else:
            return ""

    def _getDatetimeIphoneClip(self):
        if self._ext in [".MOV",".mov"]:
            imgpath = os.path.dirname(os.path.abspath(self._path))
            imgname = os.path.splitext(self._filename)[0]+".jpg"
            imgpath = os.path.join(imgpath,imgname)
            if os.path.isfile(imgpath) is False: return ""
            physicalImg = Physical(imgpath)
            physicalImg.loadInfo()
            return physicalImg.getDatetime()
        return ""

    def info(self):
        print('Filename: '+str(self._filename))
        print('Directory: '+str(self._dirname))
        print('MBytes: '+str(self._mbytes))
        print('Ext: '+str(self._ext))

    def printExifTags(self, tags):
        for tag in tags:
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                print("Key: %s, value %s" % (tag, tags[tag]))

    def hasCoordinates(self):
        return (self._lat != 0 and self._lng != 0)

    """ Getters """

    def getName(self): return str(self._filename).lower()
    def getDirName(self): return str(self._dirname)
    def getExtension(self): return str(self._ext)
    def getDatetime(self): return str(self._datetime)
    def getPath(self): return str(self._path)
    def getCamera(self): return str(self._camera)
    def getLat(self): return str(self._lat)
    def getLng(self): return str(self._lng)
    def getWidth(self): return str(self._width)
    def getHeight(self): return str(self._height)
    def getMBytes(self): return str(self._mbytes)
    def getOrientation(self): return str(self._orientation)


def main():
    logging.basicConfig(level=logging.INFO)
    f = Physical('../README.md')
    f.info()


if __name__ == '__main__':
    main()
