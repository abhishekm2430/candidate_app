from os.path import dirname
def from_root_path(path):
    return dirname(__file__) + '/../' + path