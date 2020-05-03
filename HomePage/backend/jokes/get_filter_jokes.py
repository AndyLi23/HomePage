from csv import reader
from random import randint


def get_jokes():
    print("start jokes")
    with open("HomePage/backend/jokes/jokes.csv", "r") as fin:
        re = reader(fin)
        ans = []
        for row in re:
            ans.append(row)
    l = []
    for i in range(5):
        l.append(ans[randint(0, len(ans))])
    print("end jokes")
    return l
