import os
from gsheet import *

def chunkarray(array: list, size: int):
  """Return a list of specified sized lists from a list"""
  return [array[i:i + size] for i in range(0, len(array), size)]

def isFileEmpty(file=str):
    filesize = os.stat(file)
    if filesize == 0:
        return True
    else:
        return False

sheet = gsheet()
