import os


def list_mp3_files(path):
    result = []
    os.getcwd()
    for i in os.listdir(path):
        if i.endswith(".mp3"):
            result.append(i)
    return result

