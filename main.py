import os
import win32api
import copy


WALKS = {
    'Name':"",
    'Path':"",
    'Size':None,
    'Step':0,
    'Content' : []
}

def GetDrives() -> list:
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]

def defineSize(list_of_elements):
    size = 0
    for element in list_of_elements:
        size += element['Size']
    return size

def walking(path, step=0):
    head = copy.deepcopy(WALKS)
    metadata = []
    head['Name'] = path
    head['Path'] = path
    head['Step'] = step
    head['Content'] = []
    try:
        files = os.listdir(path)
    except PermissionError as e:
        print(f"Unable to search here : {path} : {e}")
        head['Size'] = 0
        return head
    
    
    for index, element in enumerate(files):
        metadata.append(copy.deepcopy(WALKS))
        itexist = os.path.exists(f"{path}/{element}")
        if not itexist:
                metadata[index]['Name'] = element
                metadata[index]['Path'] = f"{path}/{element}"
                metadata[index]['Size'] = 0
                metadata[index]['Step'] = step+1
        else:
            isFile = os.path.isfile(f"{path}/{element}")
            if isFile:
                # print(f"{element} is a file")
                metadata[index]['Name'] = element
                metadata[index]['Path'] = f"{path}/{element}"
                metadata[index]['Size'] = os.path.getsize(f"{path}/{element}")
                metadata[index]['Step'] = step+1
            else:
                # print(walking(f"{path}/{element}", step+1))
                metadata[index] = walking(f"{path}/{element}", step+1)
    head['Content'] = metadata
    # print(head)
    head['Size'] = defineSize(metadata)
    # print(head)
    return head

def Main():
    drives = GetDrives()
    if drives != []:
        PC = []
        for drive in drives:
            PC.append(walking(drive))
        
        f = open('data.json', 'wb')
        f.write(PC)
        f.close()



if __name__ == "__main__":
    Main()
