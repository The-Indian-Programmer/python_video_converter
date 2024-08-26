# 

import uuid


def isEmpty(value):
    if value == None or value == "":
        return True
    if value == []:
        return True
    if value == {}:
        return True
    if value == 0:
        return True
    if value == False:
        return True
        
    return False


def getFilePath(files):
    
    fileName = files['file_field']
    
    extension = fileName.name.split('.')[-1]
    newFileName = str(uuid.uuid4()) + '.' + extension
    
    path = 'media/uploads/'
    # // return the folder name and file name both
    
    return {
        'path': path,
        'fileName': newFileName
        }
    
