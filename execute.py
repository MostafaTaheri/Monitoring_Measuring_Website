from monitor import Monitor
import os


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    mnt = Monitor()
    mnt.monitoring('Result', 'https://irantalent.com', 'https://digikala.com')    
