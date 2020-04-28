import csv
from random import randint


def get_jokes():
    with open("backend/jokes/jokes.csv", "r") as fin:
        reader = csv.reader(fin)
        ans = []
        for row in reader:
            ans.append(row)
    l = []
    for i in range(5):
        l.append(ans[randint(0, len(ans))])
    return l
