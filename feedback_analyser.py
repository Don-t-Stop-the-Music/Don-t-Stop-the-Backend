
def feed_analyser_proc(freq_in, low_bandwidth_output):
    while True:
        print(f"dequeued {len(freq_in.get())} frequency ranges")
    None