import os


def findExtension(folderPath: str, extension: str) -> list:
    files = [os.path.join(root, filename) 
                for root, _, filenames in os.walk(folderPath) 
                    for filename in filenames if filename.endswith(extension)]

    return files