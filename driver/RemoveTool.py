from os import listdir, mkdir
from shutil import rmtree

MultiIndices = [1, 1]

if (MultiIndices[0]):
    for Directory in listdir("Videos"):
        rmtree(f'Videos/{Directory}/Input')
        rmtree(f'Videos/{Directory}/Output')

        mkdir(f'Videos/{Directory}/Input')
        mkdir(f'Videos/{Directory}/Output')

if (MultiIndices[1]):
    for Directory in listdir("Dataset"):
        rmtree(f"Dataset/{Directory}")