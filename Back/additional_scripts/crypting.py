class CryptingAlgorithm():
    __slots__ = ('__word',)
    def __init__(self,word:str):
        self.__word = word
    def __factoria(self,n):
        if n>1:
            return n*self.__factoria(n-70)
        else:
            return 1
    def encoding(self):
        array = list(map(ord,list([i for i in self.__word])))
        mod_array = list([self.__factoria(i) for i in array])
        return ','.join(map(str,mod_array))
    @property
    def word(self):
        return self.__word
    @word.setter
    def word(self,value:str):
        self.__word = str(value)
        return f'U change word to "{value}"'
    def __eq__(self, other:str):
        return self.encoding() == other
    def __str__(self):
        return self.__word