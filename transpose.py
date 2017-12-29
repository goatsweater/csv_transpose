from __future__ import print_function
import csv
import argparse
import logging

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# log formatting
formatter = logging.Formatter('%(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# set up the argument parser
parser = argparse.ArgumentParser(description='Transform a set of values from CSV rows to columns')
parser.add_argument('csvfile', help='the source CSV file')
parser.add_argument('hc', metavar='header column', help='column to transpose as headers')
parser.add_argument('vc', metavar='value column', help='column to use as values for headers')
parser.add_argument('destcsv', help='destination CSV file')

def new_headers(file_path, column, vc):
    """Read the CSV file to determine what the new headers are."""
    found_headers = []

    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # skip any header that has already been seen
            if row[column] in found_headers:
                continue

            # never seen this before, record it
            found_headers.append(row[column])

        # formulate the new headers
        skip = (column, vc)
        new_headers = []
        new_headers += [x for x in reader.fieldnames if x not in skip]
        new_headers.extend(found_headers)

    return new_headers

def transpose(file_path, hc, vc):
    """Transpose the CSV data into the new columns."""
    records = []

    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        # keep track of headers to keep
        skip = (hc, vc)
        old_headers = [x for x in reader.fieldnames if x not in skip]

        for row in reader:
            # build a new record
            record = {}
            for col in old_headers:
                record[col] = row[col]

            # transpose the data
            record[row[hc]] = row[vc]

            # save this record
            records.append(record)

    return records

def write_data(out_path, headers, data):
    """Write a new CSV file with data."""
    with open(out_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        writer.writeheader()
        writer.writerows(data)

# mainline
if __name__ == '__main__':
    path = r'/Users/goatsweater/Downloads/cansim1572117230072146132.csv'
    src_name = 'SEX'
    val_name = 'Value'
    dst = r'/Users/goatsweater/Downloads/cansim_t.csv'

    args = parser.parse_args([path, src_name, val_name, dst])

    # get the headers to be added
    headers = new_headers(args.csvfile, args.hc, args.vc)

    # transpose the data
    new_data = transpose(args.csvfile, args.hc, args.vc)

    write_data(args.destcsv, headers, new_data)
