import os

def findExtension(folderPath:str, extension:str):
    files = []

    for root, _, files in os.path.walk(folderPath):
        for file in files:
            if file.endswith(extension):
                files.append(os.path.join(root, file))

    return files
