# There's no guarantee that this program will work.
import random
import sys

with open(sys.argv[1]) as f:

    inputs = f.readlines()

    random_data = random.sample(range(len(inputs)), int(len(inputs) * 0.75))

    train = []
    for i in random_data:
        train.append(inputs[i])
        inputs[i] = 0

    test = [i for i in inputs if not i == 0]

    with open("train.txt", "w") as f:
        f.writelines(train)
    with open("valid.txt", "w") as f:
        f.writelines(test)
