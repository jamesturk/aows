
memory:
    rm output.bin memray-flamegraph-output.html
    poetry run memray run -o output.bin -m scraping_experiments.parsing.memory_benchmark
    poetry run memray flamegraph output.bin
    open memray-flamegraph-output.html