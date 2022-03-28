class Benchmark:
    '''
    Benchmarks functions when developing code. Used to test the performance of various functions during development.
    '''
    import time


    def __init__(self):
        self.to_print_bench = True
        self.startTime = self.time.time()

        #self.file = open("reports/benchmark.txt", "w")


    def bench_start(self):
        '''
        Starts the benchmark counter.
        '''
        self.startTime = self.time.time()
        if self.to_print_bench:
            print("--BENCHMARK STARTED--")
        

    def bench_end(self, printed_text):
        """
        Stops the benchmark counter

        Args:
            printed_text: String value, This will be the label assigned to the benchmark when printed to the console.
        """

        endTime = self.time.time() - self.startTime
        if self.to_print_bench:
            #self.file.write("--BENCHMARK-- Time for Benchmark " + printed_text + " : " + str(endTime) + "\n")
            print("--BENCHMARK-- Time for Benchmark " + printed_text + " : " + str(endTime))


    def set_bench(self, to_print):
        '''
        Sets if the benchmark results should be printed to the console

        Args:
            to_print: Boolean value denoting whether to print benchmark results
        '''
        self.to_print_bench = to_print
