import numpy as np
from skimage import io
from skimage.util import view_as_blocks
from scipy.fftpack import dct, idct

MATRIX_SIZE = 8

class Image():
	def __init__(self, file):
		self.__img = io.imread(file)
		self.__usable_height = (self.__img.shape[0] // 8) * 8
		self.__usable_width = (self.__img.shape[1] // 8) * 8

	@staticmethod
	def forward_dct(block):
		return(dct(dct(block, axis=0), axis=1))

	@staticmethod
	def inverse_dct(dct_matrix):
		return(idct(idct(dct_matrix, axis=0), axis=1)/(2*MATRIX_SIZE)**2)

	@property
	def image(self):
		return(self.__img)

	@property
	def usable_height(self):
		return(self.__usable_height)

	@property
	def usable_width(self):
		return(self.__usable_width)

	def calculate_max_size(self):
		return((self.__usable_height // 8) * (self.__usable_width // 8) * 3)

	def block_split(self, channel):
		return(view_as_blocks(self.__img[0:self.__usable_height, 0:self.__usable_width, channel], block_shape=(MATRIX_SIZE, MATRIX_SIZE)))

	def overwrite_image(self, temp, channel):
		self.__img[0:self.__usable_height, 0:self.__usable_width, channel] = temp

	def save_image(self, file_name):
		io.imsave(file_name, self.__img)