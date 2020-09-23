import csv 

def save_to_csv(fname, lst):
    with open(fname, mode='a') as csvfile:
        writer = csv.writer(csvfile, delimiter = ';')
        writer.writerow(lst)

def find_user_data_in_csv(fname, usr):
    with open(fname, mode='r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';')
        for row in reader:
            if row[0] == usr:
                return row

def read_first_row(fname):
    with open(fname, mode = 'r') as csvreader:
        reader = csv.reader(csvreader, delimiter = ';')
        return next(reader)