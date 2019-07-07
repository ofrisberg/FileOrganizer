import os
import errno
import csv
import logging
from iterator import Iterator
from virtuallist import VirtualList
from physicallist import PhysicalList
from tuple import Tuple


class TupleList:

    def __init__(self, csv_path, dir_path):

        self._list_p = PhysicalList(dir_path)
        self._list_v = VirtualList(csv_path)
        logging.info('Antal fysiska: '+str(len(self._list_p)))
        logging.info('Antal virtuella: '+str(len(self._list_v)))

        logging.info('Loading tuples...')
        self._nr_missing_virtual = 0
        self._nr_missing_physical = 0
        self._tuples = []
        self._loadTuples()

    def _loadTuples(self):
        self._list_p.sortByName()

        N_p = len(self._list_p)
        N_v = len(self._list_v)
        i_p = 0
        i_v = 0

        while i_p < N_p and i_v < N_v:
            file_p = self._list_p.get(i_p)
            file_v = self._list_v.get(i_v)
            if file_v.getName() == file_p.getName():
                self._tuples.append(Tuple(file_p, file_v))
                i_v += 1
                i_p += 1
            elif file_v.getName() < file_p.getName():
                logging.error("Den virtuella filen till den fysiska '" +
                              file_p.getName()+"' hittades inte")
                i_p += 1
                self._nr_missing_virtual += 1
            else:
                logging.error("Den fysiska filen till den virtuella '" +
                              file_v.getName()+"' hittades inte i '"+self._list_v.getCSVPath()+"'")
                i_v += 1
                self._nr_missing_physical += 1

        while i_p < N_p:
            file_p = self._list_p.get(i_p)
            logging.error("Den virtuella filen till den fysiska '" +
                          file_p.getName()+"' hittades inte")
            i_p += 1
            self._nr_missing_virtual += 1
        while i_v < N_v:
            file_v = self._list_v.get(i_v)
            logging.error("Den fysiska filen till den virtuella '" +
                          file_v.getName()+"' hittades inte i '"+self._list_v.getCSVPath()+"'")
            i_v += 1
            self._nr_missing_physical += 1

    def getNrMissingPhysical(self):
        return self._nr_missing_physical

    def getNrMissingVirtual(self):
        return self._nr_missing_virtual

    def getVirtualList(self):
        return self._list_v

    def getPhysicalList(self):
        return self._list_p


def main():
    logging.basicConfig(level=logging.INFO)
    dir_path = '../../Media/organized'
    csv_path = '../../Media/files.csv'
    tl = TupleList(csv_path, dir_path)


if __name__ == '__main__':
    main()
