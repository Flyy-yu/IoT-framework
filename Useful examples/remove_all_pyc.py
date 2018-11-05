#!/usr/bin/env python
import os
import sys

root = os.getcwd()

'''
def ensure_root():
    is_root = os.geteuid() == 0
    if not is_root:
        sys.exit('Must be run as root')
'''

def main():
    #ensure_root()

    for dirpath, dirnames, filenames in os.walk(root):
        pyc_files = set()

        for file in filenames:
            name, ext = os.path.splitext(file)
            if ext == '.pyc':
                pyc_files.add(name)

        for file in pyc_files.intersection(pyc_files):
            delete_file = os.path.join(dirpath, file + '.pyc')
            print 'Removing - {}'.format(delete_file)
            os.remove(delete_file)

if __name__ == '__main__':
    main()