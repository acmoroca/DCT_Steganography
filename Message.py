class Message:
    def __init__(self, plaintext, block_size = 16):
        self._plaintext = plaintext
        self._block_size = block_size
        self._matrix = None

    @property
    def plaintext(self):
        return(self._plaintext)

    @property
    def matrix(self):
        return(self._matrix)

    @property
    def block_size(self):
        return(self._block_size)

class Key(Message):
    def __init__(self, plaintext, block_size = 16):
        super().__init__(plaintext, block_size)
        self._plaintext = self.__padding()
        self._matrix = self.__convert_to_matrix()

    def __convert_to_matrix(self):
        matrix = list(*map(lambda x: [ord(i) for i in x], self._plaintext))
        matrix = [matrix[x:x + 4] for x in range(0, len(matrix), 4)]
        return(matrix)

    def __padding(self):
        return((len(self._plaintext) % self._block_size != 0) * ([(self._block_size - len(self._plaintext) % self._block_size) * "\x00"  + self._plaintext]) + (len(self._plaintext) % self._block_size == 0) * ([self._plaintext]))

    def __validate_length(self):
        while len(self._plaintext) != self._block_size:
            self._plaintext = input("Please enter a key that is made of {} bytes : ".format(self._block_size))

class Plaintext(Message):
    def __init__(self, plaintext, block_size = 16):
        super().__init__(plaintext, block_size)
        self._plaintext = self.__padding()
        self._matrix = self.__convert_to_matrix()

    def __padding(self):
        return((len(self._plaintext) % self._block_size != 0) * ([(self._block_size - len(self._plaintext) % self._block_size) * "\x00"  + self._plaintext]) + (len(self._plaintext) % self._block_size == 0) * ([self._plaintext]))

    def __convert_to_matrix(self):
        matrix = list(*map(lambda x: [ord(i) for i in x], self._plaintext))
        matrix = [matrix[x:x + 4] for x in range(0, len(matrix), 4)]
        return(matrix)
