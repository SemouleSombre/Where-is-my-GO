# Import the necessary modules
import json
from walking import GetDrives, walking

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
