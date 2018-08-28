#!/usr/bin/env python
import cProfile

class Benchmark(object):

    def __init__(self, *args, **kargs):
        print ("Status: ")

    def profileFunc(self,func):
        cProfile.run(func)

    def test(self, loop = [0,1000]):
        for i in loop:
            print ("Loop %s from %s" % (i, loop ) )
    