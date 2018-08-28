from threading import Thread
from db.mongo import Mongo
from utils.benchmark import Benchmark


def checkDBConnection():
    db = Mongo();
    
def init_process_result():

    print("Start process")


if __name__ == '__main__':
    bm = Benchmark()
    print("!Launching Classifier Demo for benchmark Computer power!")
    bm.profileFunc(checkDBConnection)