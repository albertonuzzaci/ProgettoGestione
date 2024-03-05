import os
import opendatasets as od
import yaml
import sys
from io import StringIO


class myDataset():
    
    def __init__(self, url: str, dirName: str, user: str, key: str):
        self.url = url
        self.dirName = dirName
        self.__user_ = user
        self.__key_ = key
    
    def setupDataset(self): 
        filesCurrentDir = os.listdir()
        if (self.dirName in filesCurrentDir):
            raise Exception("Dataset already downloaded")
        else: 
            sys.stdin = StringIO(self.__user_ +'\n'+self.__key_)
            od.download(self.url)
            newDataset = set(os.listdir()) ^ set(filesCurrentDir)
            try:
                os.rename(list(newDataset)[0], self.dirName)
            except FileNotFoundError:
                print(f"Directory '{newDataset}' doesn't exists.")
            except FileExistsError:
                print(f"Directory '{self.dirName}' already exists.")


if __name__ == "__main__":
    with open('config.yaml','r') as file:
        config_data = yaml.safe_load(file)

    data = myDataset(
        config_data['DATASET']['URL'], 
        config_data['DATASET']['DATADIR'],
        config_data['DATASET']['USERNAME'],
        config_data['DATASET']['KEY']
    )
    
    data.setupDataset()
