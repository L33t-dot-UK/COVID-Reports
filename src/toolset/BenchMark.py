
#[COMPLETED V1.0.0]
class Benchmark:
    '''
    This class was used to benchmark various functions during development
    Benchmark code has been left in the toolset however setBench has been
    set to False in most cases
    '''
    import time

    def __init__(self):
        self.toPrintBench = True
        self.startTime = self.time.time()
        
    def benchStart(self):
        self.startTime = self.time.time()
        if self.toPrintBench:
            print("--BENCHMARK STARTED--")
        
    def benchEnd(self, printedText):
        endTime = self.time.time() - self.startTime
        if self.toPrintBench:
            print("--BENCHMARK-- Time for Benchmark " + printedText + " : " + str(endTime))

    def setBench(self, toPrint):
        self.toPrintBench = toPrint