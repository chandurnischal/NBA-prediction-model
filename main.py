import os
from datetime import datetime, time

def main():
    now = datetime.now().time()
    check = time(9, 0)

    if now >= check:
        os.system("python processing/process.py")
    else:
        print("Database up to date.")
        
    os.system("python app/app.py")


if __name__ == "__main__":
    main()
