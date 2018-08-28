#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
.. module:: machine_learning
    :plataform: Unix, Linux
    :synopsis: Classify worlds for build doc
.. moduleauthor: Jefferson Puchalski <jefferson.morpheustecnologia.com> 
"""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



import re
import os
import time
from pymongo import MongoClient

import numpy as np
import tflearn
import tensorflow as tf
import random
import subprocess
import nltk
from nltk.stem.rslp import RSLPStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from multiprocessing import Process, Lock
from pymongo.errors import ConnectionFailure
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.errors import OperationFailure
import signal
import sys
import threading

"""
    Loging File handle
"""
import logging

# create logger
logger = logging.getLogger('log_classify')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

"""
# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
"""


class ClassifyWords():
    """ 
        This class get a database with messages or conversations and perform lexial analisys and some classificiations.
    """

    def __init__(self):
        """Init constructor. Create database and stemmer instances.
        raises excpetion on fail to create instances
        
        :raises: Exception
        
        """
        try:
            self.stemmer = nltk.PorterStemmer()
            self.client = MongoClient('mongodb://localhost:27017/')
        except Exception as ex:
            print(bcolors.FAIL + "We cant create client instance, \nplease check your configuration and try again\nError Code: %s" + bcolors.ENDC, ex.value)
        finally:
            print(bcolors.OKGREEN +
                  "Client instance was sucessfull created!" + bcolors.ENDC)
        
        self.lock = Lock()

    def setFields(self):
        """Set all fields for classification words and download nltk.

        """
        self.db = self.client.b2b
        self.ai_intents = self.db.mensagens
        self.words = []
        self.classes = []
        self.documents = []

        nltk.download('punkt')
        nltk.download('stopwords')

        self.english_stopwords = set(stopwords.words('english'))
        self.portuguese_stopwords = set(stopwords.words('portuguese'))

    def tokenizeData(self, regex="[\w']+", limit=250000):
        """ Tokenize all data from ai_intents.
        :param regex: Regex for use in spliting the words and take of punctuation
        :type regex: str.
        :para limit: Limit of amount of iteration on db data
        :type limit: int.

        .. note::
            This function NEVER can called from Main thread. This need called from a MTA (Multi Thread Apatament)
            Ex.:
            
            from multiprocessing import Process
            p = Process(target=rdn.tokenizeData, args=())
            p.start()
            p.join()
        """

        # tokenizer will parse words and leave out punctuation
        self.tokenizer = RegexpTokenizer(r'[a-zA-Z]{3,}')
        count = 0

        # Python mango is not forksafe so we need  create after thread start
        clientFrk = MongoClient('mongodb://localhost:27017/')

        db = clientFrk.b2b
        ai_intentions = db.mensagens
        
        print("\n")  # clean lines
        print("We find " + str(ai_intentions.count(({"$and": [{"datahora": {"$gte": '2018-01-01'}}, {"user": { "$ne" : 'Super M'}}]}))) + " registers, Do you wanna iterate all they? ")
        start_time = time.time()
        try:
            # loop through each pattern for each intent, use batch_size with 10 for timederror out problems
            for intent in ai_intentions.find({"$and": [{"datahora": {"$gte": '2018-01-01'}}, {"user": { "$ne" : 'Super M'}}]}).batch_size(10):
                tokens = self.tokenizer.tokenize(intent['msg'])  # tokenize pattern
                self.words.extend(tokens)  # add tokens to list
                for pattern in intent['msg']:
                    #print(pattern)
                    tokens = self.tokenizer.tokenize(pattern)  # tokenize pattern
                    #words =words.extend(tokens)  # add tokens to list
                    # add tokens to document for specified intent
                    self.documents.append((tokens, intent['msg']))
                    # add intent name to classes list
                    if intent['msg'] not in self.classes:
                        self.classes.append(intent['msg'])
                    percent = (count / limit * 100)
                    print("Processed: %.0f%%" % (percent), sep=' ', end='\r')
                    if count == limit:
                        break
                count += 1
                if count == limit:
                    print(len(self.words), "words", self.words)
                    self.ToJSON(self.words, 'unprocess_data.json')
                    break
            elapsed_time = time.time() - start_time
            print('Time elapsed (hh:mm:ss.ms) {}'.format(elapsed_time))
            time.sleep(1000)
            print(bcolors.OKBLUE + "Now Steaming words" + bcolors.ENDC)
            self.steamAndSaveToJson()
        except OperationFailure as e:
            print(bcolors.FAIL + "Error, A server has Timedout\nReason: " +
                  e.details + bcolors.ENDC)
            exit(0)
        

    def steamAndSaveToJson(self):
        """ Steam all words and save to given JSON
        .. note::
            If Your are calling this inside a MTA, You need explicity call in same Process or Thread.
            or the results can be messed with data racing condition.

        """
        # stem each word, change to lower case and remove duplicates
        self.words = [self.stemmer.stem(
            w.lower()) for w in self.words if w not in self.portuguese_stopwords]
        self.words = sorted(list(set(self.words)))
        if __debug__:
            self.printSumary()
            try:
                self.ToJSON(self.words, 'final_data.json')
            except Exception as e:
                print(bcolors.FAIL +
                      "Error in saving JSON file!\n Reason %s" % e.value)
        else:
            try:
                self.ToJSON(self.words, 'final_data.json')
            except Exception as e:
                print(bcolors.FAIL +
                      "Error in saving JSON file!\n Reason %s" % e.value)

    def printSumary(self):
        """ Print all inforamtions about Classify Process
        """
        print(len(self.documents), "documents")
        print(len(self.classes), "classes", self.classes)
        print(len(self.words), "words", self.words)

    def ToJSON(self, WordListArray, filename):
        import json
        with open(filename, 'w') as outfile:
            json.dump(WordListArray, outfile)

    def WordCount(self, _file):
        from collections import Counter

        with open(_file, 'r', encoding="utf-8") as outfile:
            wordcount = Counter(outfile.read().split())
        formatedList = []

        for item in wordcount.items():
            if len(item) > 1:
                print("size:{1},text:{0}".format(*item))
                str = ("\"size\":{1},\"text\":{0}".format(*item))
                formatedList.append(str)
        print(formatedList)
        formatedList = list(filter(("\\").__ne__, formatedList))

        list_sort = sorted(formatedList)
        top20CountFinalY = list_sort[-100:]

        self.ToJSON(formatedList, 'Count.json')
        self.ToJSON(top20CountFinalY, 'top100-Count.json')

    def plotTop20(self, yLimit, WorldListJsonFiltred):
        """ UNDOCUMENTED - TODO NEED SEE IF WE WILL USE IT
        """
        import matplotlib.pyplot as plt
        from collections import Counter
        import numpy as np
        import json

        data_x = []
        with open(WorldListJsonFiltred) as outfile:
            data_x = json.load(outfile)

        c_x = Counter(data_x)

        plt.xlim(0, 20)
        plt.ylim(0, yLimit)

        top20CountY = c_x.values()
        top20CountX = c_x.keys()

        print("Re-Arange arrays")

        top20CountSorted = sorted(top20CountY)
        top20CountFinalY = top20CountSorted[-100:]

        top20CountSorted = sorted(top20CountX)
        top20FiltredX = []

        for x in top20CountSorted:
            if len(x) > 1:
                top20FiltredX.append(x)

        top20CountFinalX = top20FiltredX[-100:]

        self.ToJSON(top20CountFinalX, 'top100.json')

        print(top20CountFinalX)

        print(top20CountFinalX)
        print(top20CountFinalY)

        labels = top20CountFinalX
        print(tuple(labels))

        y_pos = np.arange(len(tuple(labels)))
        print(y_pos)

        plt.bar(y_pos, top20CountFinalY, align='center', alpha=0.5)
        plt.xticks(y_pos, tuple(labels))

        plt.ylabel('Contagem')
        plt.title('Top 20 Palavras mais Usadas')

        plt.savefig('top20.jpg')
        plt.show()

    def plotWorldList(self, wordlistX, wordlistY):
        """ UNDOCUMENTED - TODO NEED SEE IF WE WILL USE IT
        """
        import matplotlib.pyplot as plt
        from collections import Counter
        import json

        # import json and count his keys and values to plot
        data_x = []
        with open(wordlistX) as outfile:
            data_x = json.load(outfile)

        data_y = []
        with open(wordlistY) as outfile:
            data_y = json.load(outfile)

        # implict COunt all data in Y and X
        c_x = Counter(data_x)
        c_y = Counter(data_y)

        # change axes ranges
        plt.ylim(0, 1000)

        # add title
        plt.title('Relationship Between Conversation and Word Count')

        # add x and y labels
        plt.xlabel('WordCount')
        plt.ylabel('Message Count')

        print(c_x.values())

        lists = sorted(c_x.items())  # sorted by key, return a list of tuples

        x, y = zip(*lists)  # unpack a list of pairs into two tuples

        # Plot x and Y axis
        plt.plot(x, y, color="blue")
        #plt.bar(c_x.values(), c_x.values())

        plt.savefig('plot.jpg')

    def bagMontage(self, documents):
        self.data_set = []
        count = 0
        if type(documents) != type(dict) and type(documents) != type(list):
            print (bcolors.FAIL + "We cant iterate in given variable" + bcolors.ENDC)
        
        # training set, bag of words for each sentence
        for document in documents:
            bag = []
            
            # stem the pattern words for each document element
            pattern_words = document[0]
            pattern_words = [self.stemmer.stem(word.lower()) for word in pattern_words]
            
            # create a bag of words array
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)

            self.data_set.append(bag)
            count +=1
            percent = (count / len(documents) * 100)
            print("Processed: %.0f%%" % (percent), sep=' ', end='\r')

        """print("data_set", self.data_set)"""
    
    def jsonToList(self, in_json):
        import json

        with open(in_json, 'w') as outfile:
            return json.loads(outfile)
    
        
    def startProcess(self):
        """Start all classify words process in MTA
        .. note::
            This is MTA so a SIGTERM handler will be added for non block main process problem.
        """

        if __debug__:
            print("We are log all values to a single log file")
        else:
            print("No log files")

        print("Starting some sanatize words")
        print("This action will be held in MTA")

        print('Checking if we have processed data in JSON files...')

        from pathlib import Path

        json_unprocessed = Path("final_data.json")
        json_processed = Path("unprocess_data.json")

        if json_processed.is_file() and json_unprocessed.is_file():
            r = input(
                bcolors.HEADER + "We have fie, do you whant reprocess? [Yy/Nn]: " + bcolors.ENDC)
            if r.lower() == 'y':
                rdn.plotTop20(80000, 'unprocess_data.json')
                exit(0)

        self.setFields()

        p = Process(target=rdn.tokenizeData, args=())
        CPUCores = len(os.sched_getaffinity(0))
        print(bcolors.WARNING + "Amount of Cores avaliable for Interation: %d" %
              CPUCores + bcolors.ENDC)

        p.start()

        def signal_handler(sig, frame):
            print('You pressed Ctrl+C!')
            p.terminate()
            pBag.terminate()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        print(bcolors.OKBLUE + "Processing List please be patient..."
              + bcolors.ENDC, sep=' ', end='\r')
        p.join()

        asnwer = input(bcolors.OKGREEN +
                       "Do you wish create the bag's world list?[Y/N]: " + bcolors.ENDC)
        if asnwer.lower() == 'y':
            print(bcolors.BOLD + "Creating Bag list..." + bcolors.ENDC)
            
            # Creating thread and send bagMontage to It - Not creating in process becouse of low intense work here
            pBag = Process(target=self.bagMontage, name="BagProcess", args=(self.jsonToList(self.db.mensagens)))
            
            pBag.start()
            pBag.join()

        else:
            print(bcolors.WARNING + "Skip baging wordlist creation")
        
        print(bcolors.OKGREEN +
              "Process list was sucessfull!\nNow Print all results" + bcolors.ENDC)

        asnwer = input(bcolors.OKGREEN +
                       "Do you wish plot the world list?[Y/N]: " + bcolors.ENDC)

        rdn.WordCount('unprocess_data.json')

        if asnwer.lower() == 'y':
            self.plotWorldList('unprocess_data.json', 'final_data.json')
        else:
            print("Exiting...")


rdn = ClassifyWords()
try:
    rdn.WordCount('unprocess_data.json')
except IOError:
    print (bcolors.FAIL + "file not fount"+ bcolors.ENDC)


rdn.startProcess()

# Creating thread and send bagMontage to It - Not creating in process becouse of low intense work here
#pBag = Process(target=rdn.bagMontage, name="BagProcess", args=(rdn.jsonToList(rdn.db.mensagens)))
            
#pBag.start()

#pBag.join()



#rdn.bagMontage()
#rdn.startProcess()