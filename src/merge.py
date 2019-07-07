import os
import errno
import csv
import logging
from datetime import datetime, timedelta
# Remove the not needed ones below
from iterator import Iterator
from virtual import Virtual
from virtuallist import VirtualList
from physicallist import PhysicalList
from tuplelist import TupleList


class Merge:

    def __init__(self, csv_path, src_dir, dst_dir):
        self._nl = PhysicalList(src_dir)
        self._tl = TupleList(csv_path, dst_dir)
        self._vlist = self._tl.getVirtualList()
        self._dst_dir = dst_dir

    def merge(self, preview=True):
        if self._tl.getNrMissingPhysical() > 0 or self._tl.getNrMissingVirtual() > 0:
            return logging.error('Fix corruption problem before merging')
        logging.info('Nr files: '+str(len(self._nl)))
        for f in self._nl:
            f.loadInfo()
        self._nl.filterTimestamps()
        logging.info('Nr files after timestamp filter: '+str(len(self._nl)))

        for f in self._nl:
            new_path_full, new_path_part = self.getNewPath(f)
            if os.path.exists(new_path_full):
                logging.error('New path for '+f.getName() +
                              ' already exists ('+new_path_part+')')
            else:
                self._physicalMerge(f, new_path_full, new_path_part, preview)
        self._virtualMerge(preview)

    def _physicalMerge(self, f, new_path_full, new_path_part, preview):
        if preview:
            print('Should have renamed', f.getPath(), 'to', new_path_full)
        else:
            logging.info('Renaming '+f.getPath()+' to '+new_path_full)
            os.renames(f.getPath(), new_path_full)
        self._vlist.append(Virtual.constructFromPhysical(f, new_path_part))

    def _virtualMerge(self, preview):
        if preview:
            return print("Should have updated the CSV file, total nr files:", len(self._vlist))
        self._vlist.sort()
        self._vlist.backup()
        self._vlist.write()

    def getNewPath(self, f):
        dt = datetime.strptime(f.getDatetime(), "%Y-%m-%d %H:%M:%S")
        part = dt.strftime("%Y/%Y-%m/%Y%m%d%H%M%S")+f.getExtension()
        return (os.path.join(self._dst_dir, part), part)


def main():
    logging.basicConfig(level=logging.INFO)

    csv_path = '../../Media/files.csv'
    from_path = '../../r_plots'
    to_path = '../../Media/organized'

    m = Merge(csv_path, from_path, to_path)
    m.merge()


if __name__ == '__main__':
    main()
