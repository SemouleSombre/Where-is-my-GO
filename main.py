# Import the necessary modules
import os
import copy
import json
import win32api
import pandas as pd
import numpy as np

# Create the form of each element
WALKS = {
    'Name':"",      # Name of the file or folder
    'Path':"",      # Path of the file or folder
    'Size':None,    # Size of the file or folder
    'Step':0,       # Step of the walk
    'Content' : []  # all elements in the folder (uniquely for folders)
}

def GetDrives() -> list:
    """
    Get all drives of the computer
    Returns:
        list: List of the names of the drives
    """
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    return drives

def defineSize(list_of_elements)->int:
    """
    Define the size of the folder

    Args:
        list_of_elements (class): List of the elements in the folder

    Returns:
        int: sum of the size of all elements in the folder
    """
    size = 0
    for element in list_of_elements:
        size += element['Size']
    return size

def walking(path:str, step:int=0):
    """_summary_

    Args:
        path (_type_): _description_
        step (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
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
                metadata[index]['Name'] = element
                metadata[index]['Path'] = f"{path}/{element}"
                metadata[index]['Size'] = os.path.getsize(f"{path}/{element}")
                metadata[index]['Step'] = step+1
            else:
                metadata[index] = walking(f"{path}/{element}", step+1)
    head['Content'] = metadata
    head['Size'] = defineSize(metadata)
    return head

def Main():
    """
    Main function of the program
    Get all drives of the computer and walk through them
    Save the result in a json file
    """
    drives = GetDrives()
    if drives != []:
        PC = []
        for drive in drives:
            PC.append(walking(drive))
        PC = {'This PC' : PC}
        with open('PC.json', 'w') as f:
            json.dump(PC, f, indent=4)

if __name__ == "__main__":
    Main()
