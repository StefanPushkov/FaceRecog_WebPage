import os

raw_data = "/Data/"
BASE_DIR = 'FaceRecog_WebPage'

VideoOut_file = 'C:/Storage/Rand/Data/out.avi'

def get_base_dir_by_name(name):
    path = os.getcwd()
    lastchar = path.find(name) + len(name)
    return os.getcwd()[0:lastchar]

base_dir = get_base_dir_by_name(BASE_DIR).replace("\\","/")
print(base_dir)