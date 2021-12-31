import csv

def sample():
    with open("submissions.csv") as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        l.sort()
        for i in range(100):
            print(l[i])
