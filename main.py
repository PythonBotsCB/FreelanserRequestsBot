from handlers.navigations import *
from config import *

def main():
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()