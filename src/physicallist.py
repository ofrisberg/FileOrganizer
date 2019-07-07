import os
import errno

from iterator import Iterator
from physical import Physical


class PhysicalList:
    def __init__(self, dir_path):
        fi = Iterator()
        fi.setDirectory(dir_path)
        paths = fi.getAll()

        self._files = []
        for path in paths:
            self._files.append(Physical(path))

    def append(self, path):
        self._files.append(Physical(path))

    def __len__(self):
        return len(self._files)

    def __iter__(self):
        return iter(self._files)

    def sortByName(self):
        self._files = sorted(self._files)

    def filterTimestamps(self):
        old = self._files
        self._files = [f for f in old if f.getDatetime() != ""]

    def summary(self):
        self.sortByName()
        for f in self:
            f.loadInfo()
            print(f.getDatetime(), f.getPath())
        print('Total files:', len(self))
        print('Has timestamps:', self.getNrTimestamps())
        print('Has coordinates:', self.getNrCoordinates())
        print('Extensions:', self.getUniqueExtensions())
        print('Cameras:', self.getUniqueCameras())

    def getNrTimestamps(self):
        return sum(f.getDatetime() != "" for f in self)

    def getNrCoordinates(self):
        return sum(f.hasCoordinates() for f in self)

    def getUniqueExtensions(self):
        return {f.getExtension() for f in self}

    def getUniqueCameras(self):
        return {f.getCamera() for f in self}

    def get(self, i):
        return self._files[i]


def main():
    path = '../'
    pl = PhysicalList(path)
    pl.summary()


if __name__ == '__main__':
    main()
