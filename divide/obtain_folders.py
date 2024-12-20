import os

# os.mkdir("./divide/users")
for i in range(287):
    path = "./divide/films/" + str(i)
    if not os.path.exists(path=path):
        os.mkdir(path=path)