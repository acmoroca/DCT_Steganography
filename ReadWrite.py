import numpy as np
import binascii
from math import ceil
from Image import *
from AES import *

y1, x1 = 4, 5
y2, x2 = 5, 4
THRESHOLD = 25

class Reader():
	def __init__(self, file, key = ""):
		self._file = file
		try:
			self._Image_object = Image(file)
			if self._Image_object.image.shape[0] < 8 or self._Image_object.image.shape[1] < 8:
				return("Image too small, must be at least 8 by 8")
		except:
			return("Unsupported image format or no such file exists")
		self._key = key
		if self._key != "":
			self._AES = AES(key)

	def process_image(self):
		if self.__identify_file_type() == -1:
			return("Error : File is not a png")
		self.__length = self.__identify_length()
		max_size = self._Image_object.calculate_max_size() // 3
		if 0 < self.__length <= (max_size):
			self.__msg = self.__read_message(2)
		elif max_size < self.__length <= (2 * max_size):
			temp = self.__length
			self.__length = max_size
			self.__msg = self.__read_message(2)
			self.__length = temp - max_size
			self.__msg += self.__read_message(1)
		elif (2 * max_size) < self.__length <= (3 * max_size):
			temp = self.__length
			self.__length = max_size
			self.__msg = self.__read_message(2)
			self.__msg += self.__read_message(1)
			self.__length = temp - (2 * max_size)
			self.__msg += self.__read_message(0)
		else:
			return("Error : Identified data length is greater than maximum or 0")
		self.__msg = self.__process_message()
		if self._key != "":
			self.__msg = self._AES.decrypt(self.__msg)
		return(self.__msg)

	def __read_binary_file(self):
		try:
			binfile = open(self._file, "rb")
			data = binfile.read()
			hex_str = str(binascii.hexlify(data))
			binfile.close()
		except IOError:
			print("Error encountered while trying to read {}".format(self._file))
			raise SystemExit
		return(hex_str)

	def __identify_file_type(self):
		extension = self._file.find(".png")
		return(extension)

	def __identify_length(self):
		hex_str = self.__read_binary_file()
		end_of_png = hex_str.find("0000000049454e44ae426082")
		length = hex_str[end_of_png + 24:-1]
		return(int(length, 16))

	def __read_message(self, channel):
		blocks = self._Image_object.block_split(channel)
		if blocks.shape[1] < blocks.shape[0]:
			i = [(index // blocks.shape[1]) for index in range(self.__length)]
			j = [(index % blocks.shape[1]) for index in range(self.__length)]
		else:
			i = [(index % blocks.shape[0]) for index in range(self.__length)]
			j = [(index // blocks.shape[0]) for index in range(self.__length)]
		return([self._read_bit(blocks[i[index], j[index]]) for index in range(self.__length)])

	def _read_bit(self, block):
		dct_matrix = self._Image_object.forward_dct(block)
		return(0 if self._absolute_difference(dct_matrix) > 0 else 1)

	def _absolute_difference(self, dct_matrix):
		return(abs(dct_matrix[y1, x1]) - abs(dct_matrix[y2, x2]))

	def __process_message(self):
		self.__msg = map(str, self.__msg)
		self.__msg = "".join(self.__msg)
		ascii_message = ""
		for i in range(0, len(self.__msg), 8):
			ascii_message += chr(int("0" + self.__msg[i:i+8], 2))
		return(ascii_message)

class Writer(Reader):
	def __init__(self, file, msg, key = ""):
		super().__init__(file, key)
		if self._key != "":
			self.__msg = self._AES.encrypt(msg)
			self.__msg = self.__process_message(self.__msg)
		else:
			self.__msg = self.__process_message(msg)
		self.__length = len(self.__msg)

	def __process_message(self, msg):
		msg = [format(ord(char), "#010b")[2:] for char in msg]
		msg = [[int(char) for char in bits] for bits in msg]
		msg = [item for sublist in msg for item in sublist]
		return(msg)

	def process_image(self):
		max_size = self._Image_object.calculate_max_size() // 3
		if 0 < self.__length <= (max_size):
			result = self.__hide_message(self.__msg, 2)
			self._Image_object.overwrite_image(result, 2)
		elif max_size < self.__length <= (2 * max_size):
			message_part = self.__msg[0:max_size]
			result = self.__hide_message(message_part, 2)
			self._Image_object.overwrite_image(result, 2)
			message_part = self.__msg[max_size:]
			result = self.__hide_message(message_part, 1)
			self._Image_object.overwrite_image(result, 1)
		elif (2 * max_size) < self.__length <= (3 * max_size):
			message_part = self.__msg[0:max_size]
			result = self.__hide_message(message_part, 2)
			self._Image_object.overwrite_image(result, 2)
			message_part = self.__msg[max_size:2 * max_size]
			result = self.__hide_message(message_part, 1)
			self._Image_object.overwrite_image(result, 1)
			message_part = self.__msg[2 * max_size:]
			result = self.__hide_message(message_part, 0)
			self._Image_object.overwrite_image(result, 0)
		else:
			return("Error : Data too large to hide in file or 0")
		self.__save()
		return("Done!")

	def __hide_message(self, message_part, channel):
		temp = self._Image_object.image.copy()[0:self._Image_object.usable_height, 0:self._Image_object.usable_width, channel]
		blocks = self._Image_object.block_split(channel)
		if blocks.shape[1] < blocks.shape[0]:
			i = [(index // blocks.shape[1]) for index in range(len(message_part))]
			j = [(index % blocks.shape[1]) for index in range(len(message_part))]
		else:
			i = [(index % blocks.shape[0]) for index in range(len(message_part))]
			j = [(index // blocks.shape[0]) for index in range(len(message_part))]
		for index, bit in enumerate(message_part):
			y = i[index]
			x = j[index]
			block = blocks[y, x]
			temp[y*MATRIX_SIZE: (y+1)*MATRIX_SIZE, x*MATRIX_SIZE: (x+1)*MATRIX_SIZE] = self.__hide_bit(block, int(bit))
		return(temp)

	def __hide_bit(self, block, bit):
		temp = block.copy()
		dct_matrix = self._Image_object.forward_dct(temp)
		while not self.__check_validity(dct_matrix, bit, THRESHOLD) or (bit != self._read_bit(temp)):
			dct_matrix = self.__change_difference(dct_matrix, bit)
			temp = self.__round_array(self._Image_object.inverse_dct(dct_matrix))
		return(temp)

	def __check_validity(self, dct_matrix, bit, threshold):
		difference = self._absolute_difference(dct_matrix)
		if (bit == 0) and (difference > threshold):
			return(True)
		elif (bit == 1) and (difference < -threshold):
			return(True)
		else:
			return(False)

	def __change_difference(self, dct_matrix, bit):
		temp = dct_matrix.copy()
		if bit == 0:
			temp[y1, x1] = self.__increase_mag(temp[y1, x1])
			temp[y2, x2] = self.__decrease_mag(temp[y2, x2])
		elif bit == 1:
			temp[y1, x1] = self.__decrease_mag(temp[y1, x1])
			temp[y2, x2] = self.__increase_mag(temp[y2, x2])
		return(temp)

	def __decrease_mag(self, element):
		if np.abs(element) <= 1:
			return(0)
		else:
			return(element - 1 if element >= 0 else element + 1)

	def __increase_mag(self, element):
		return(element + 1 if element >= 0 else element - 1)

	def __round_array(self, arr):
		return(np.uint8(np.round(np.clip(arr, 0, 255), 0)))

	def __save(self):
		path_index = self._file[::-1].find("/")
		path = self._file[:len(self._file) - path_index]
		filename = self._file[len(path):]
		format_index = filename.find(".")
		self._file = path + "hidden_" +filename[:format_index] + ".png"
		self._Image_object.save_image(self._file)
		self.__append_to_binary_file()

	def __append_to_binary_file(self):
		try:
			binfile = open(self._file, "ab")
			number_of_bytes = ceil(self.__length.bit_length() / 8)
			byte_stream = self.__length.to_bytes(number_of_bytes, "big") 
			binfile.write(byte_stream)
			binfile.close()
		except IOError:
			print("Error encountered while writing to {}".format(self._file))
			raise SystemExit

"""
London by William Blake
I wander thro' each charter'd street,
Near where the charter'd Thames does flow. 
And mark in every face I meet
Marks of weakness, marks of woe.

In every cry of every Man,
In every Infants cry of fear,
In every voice: in every ban,
The mind-forg'd manacles I hear 

How the Chimney-sweepers cry
Every blackning Church appalls, 
And the hapless Soldiers sigh
Runs in blood down Palace walls 

But most thro' midnight streets I hear
How the youthful Harlots curse
Blasts the new-born Infants ear 
And blights with plagues the Marriage hearse
"""