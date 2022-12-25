parsing-speed:
    poetry run python -m aows.parsing.speed

parsing-speed6:
    poetry run python -m aows.parsing.benchmark6

parsing-memory:
    poetry run python -m aows.parsing.memory

memray:
    rm output.bin memray-flamegraph-output.html || true
    poetry run memray run -o output.bin -m aows.parsing.memory
    poetry run memray flamegraph output.bin
    open memray-flamegraph-output.html
