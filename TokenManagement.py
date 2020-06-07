import pickle
import hashlib
import time
class TokenManager():
    def __init__(self):
        self.__tokenFile = "token.data"
        self.data = {}

    def createFile(self):
        data = {}
        with open(self.__tokenFile, "wb") as f:
            pickle.dump(data, f)

    def loadFile(self):
        with open(self.__tokenFile, "rb") as fp:
            self.data = pickle.load(fp)

    def saveFile(self):
        with open(self.__tokenFile, "wb") as fp:
            pickle.dump(self.data, fp)

    def checkToken(self, token: str) -> bool:
        self.loadFile()
        if token in self.data.values():
            return True
        return False

    def genToken(self, forName: str) -> str:
        self.loadFile()
        salt = str(time.time())
        token = hashlib.md5(salt.encode())
        if forName not in self.data.keys():
            self.data[forName] = token.hexdigest()
            self.saveFile()
            return token
        return ''

    def printAll(self):
        self.loadFile()
        print(self.data)

    def getTokenName(self, token: str) -> str:
        self.loadFile()
        if not self.checkToken(token):
            return False
        for key, xtoken in self.data.items():
            if xtoken == token:
                return key
        return False