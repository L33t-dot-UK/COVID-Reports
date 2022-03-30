class Benchmark:
    '''
    Benchmarks functions timing how long it takes for lines of code to execute. Used in development when apraising execution time of loops and read cycles when accessing csv files.
    '''

    
    import time
    
    
    def __init__(self):
        self.to_print_bench = True
        self.startTime = self.time.time()

        #self.file = open("reports/benchmark.txt", "w")


    def bench_start(self):
        '''
        Starts the benchmark counter, call this at the start of your code.
        '''
        self.startTime = self.time.time()
        if self.to_print_bench:
            print("--BENCHMARK STARTED--")
        

    def bench_end(self, printed_text):
        """
        Stops the benchmark counter, call this at the end of your code.

        Args:
            :printed_text: String value, This will be the label assigned to the benchmark when printed to the console.
        """

        endTime = self.time.time() - self.startTime
        if self.to_print_bench:
            #self.file.write("--BENCHMARK-- Time for Benchmark " + printed_text + " : " + str(endTime) + "\n")
            print("--BENCHMARK-- Time for Benchmark " + printed_text + " : " + str(endTime))


    def set_bench(self, to_print):
        '''
        Decides if the benchmark results should be printed to the console, instead of deleting benchmark code you can set this to false at the start of your script.

        Args:
            :to_print: Boolean value denoting whether to print benchmark results.
        '''
        self.to_print_bench = to_print
