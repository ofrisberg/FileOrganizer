import os
import errno
import csv
import logging


class Tuple:

    def __init__(self, file_p, file_v):
        self.file_p = file_p
        self.file_v = file_v
