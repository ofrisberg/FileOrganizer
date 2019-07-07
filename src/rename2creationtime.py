import os
import errno
import logging
import platform
import datetime
from physicallist import PhysicalList


class Rename2Creationtime:
    def __init__(self, dir_path):
        self._pl = PhysicalList(dir_path)

    def rename(self, preview=True):
        for f in self._pl:
            old_path = f.getPath()
            dt = self.getCreationDate(old_path)
            head = os.path.split(old_path)[0]
            new_path = os.path.join(head, self.getNewName(f, dt))

            if preview:
                print(old_path)
                print(new_path)
            else:
                os.rename(old_path, new_path)

    def getNewName(self, f, dt):
        dt_url = self.datetime2url(dt)
        new_name = dt_url+'-'+f.getName()
        return new_name

    def getCreationDate(self, path):
        if platform.system() == 'Windows':
            return self.secondsToDatetime(os.path.getctime(path))
        else:
            stat = os.stat(path)
        try:
            return self.secondsToDatetime(stat.st_birthtime)
        except AttributeError:
            return self.secondsToDatetime(stat.st_mtime)

    def datetime2url(self, dt):
        str = dt.replace('-', '')
        str = str.replace(':', '')
        return str.replace(' ', '_')

    def secondsToDatetime(self, seconds):
        dt = round(float(seconds))
        dt = datetime.datetime.utcfromtimestamp(dt)
        dt = dt.isoformat()
        return dt.replace('T', ' ')


def main():
    logging.basicConfig(level=logging.INFO)

    path = '../../r_plots'
    r = Rename2Creationtime(path)
    r.rename()


if __name__ == '__main__':
    main()
