import os
import errno
import csv
import logging
from virtual import Virtual


class VirtualList:

    def __init__(self, csv_path):
        if os.path.isfile(csv_path) is False:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), csv_path)
        self._csv_path = csv_path
        self._virtualfiles = []
        self._loadData()

    def _loadData(self):
        filereader = csv.reader(open(self._csv_path), delimiter=",")
        next(filereader)
        for datetime, path, camera, lat, lng, width, height, mbytes, orientation, old_dir, old_file in filereader:
            self._virtualfiles.append(Virtual(
                datetime, path, camera, lat, lng, width, height, mbytes, orientation, old_dir, old_file))

    def __len__(self):
        return len(self._virtualfiles)

    def __iter__(self):
        return iter(self._virtualfiles)

    def getCSVPath(self):
        return self._csv_path

    def get(self, i):
        return self._virtualfiles[i]

    def append(self, v):
        self._virtualfiles.append(v)

    def sort(self):
        tmp = sorted(self._virtualfiles)
        self._virtualfiles = tmp

    def backup(self):
        backup_path = self._csv_path+'.backup'
        if os.path.exists(backup_path):
            os.remove(backup_path)
        os.rename(self._csv_path, backup_path)

    def write(self):
        VirtualList.createEmptyCSV(self._csv_path)
        with open(self._csv_path, 'w', newline='') as f:
            w = csv.writer(f, quoting=csv.QUOTE_ALL)
            w.writerow(["datetime", "path", "camera", "lat", "lng", "width",
                        "height", "mbytes", "orientation", "old_dir", "old_file"])
            for file in self:
                w.writerow([file._datetime, file._path, file._camera, file._lat, file._lng, file._width,
                            file._height, file._mbytes, file._orientation, file._old_dir, file._old_file])

    @staticmethod
    def createEmptyCSV(path):
        if path is None:
            raise RuntimeError('Missing argument with new CSV-file to create')
        if os.path.exists(path):
            raise RuntimeError('Path to new CSV-file already exists')
        with open(path, 'w', newline='') as f:
            w = csv.writer(f, quoting=csv.QUOTE_ALL)
            w.writerow(["datetime", "path", "camera", "lat", "lng", "width",
                        "height", "mbytes", "orientation", "old_dir", "old_file"])


def main():
    logging.basicConfig(level=logging.DEBUG)
    flv = VirtualList('../../Media/files.csv')
    print('Antal:', len(flv))
    for f in flv:
        print(f.getName())


if __name__ == '__main__':
    main()
