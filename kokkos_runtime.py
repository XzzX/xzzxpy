#! /usr/bin/env python3


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('filename', type=str, help='kokkos performance dump')
    parser.add_argument('-n', type=int, help='number of entries in output', default = 5)
    args = parser.parse_args()
    
    import json
    with open(args.filename, 'r') as fin:
        perf_data = json.load(fin)['kokkos-kernel-data']
        
    def extract_column(perf_data, col):
        return [x[col] for x in perf_data['kernel-perf-info']]
    
    sizes = extract_column(perf_data, 'total-time')
    labels = extract_column(perf_data, 'kernel-name')
    
    import pandas as pd
    frame = pd.DataFrame({'kernel-name': extract_column(perf_data, 'kernel-name'),
                         'total-time': extract_column(perf_data, 'total-time'),
                         'fraction': extract_column(perf_data, 'total-time'),
                         'call-count': extract_column(perf_data, 'call-count'),
                         'time-per-call': extract_column(perf_data, 'time-per-call'),
                         'kernel-type': extract_column(perf_data, 'kernel-type')})
    total_time = frame['total-time'].sum()
    frame['fraction'] /= total_time
    frame = frame.sort_values('total-time', ascending=False)
    
    print(frame[:args.n])

if __name__ == '__main__':
    main()
