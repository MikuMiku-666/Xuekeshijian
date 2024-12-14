import os

# os.mkdir("./divide/users")
for i in range(500):
    path = "./divide/users/" + str(i)
    if not os.path.exists(path=path):
        os.mkdir(path=path)