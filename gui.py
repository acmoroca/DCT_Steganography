from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from ReadWrite import *

root = Tk()
root.title("STEGOsaur")
root.resizable(False, False)
root.geometry('275x150')

def select_file():
	filetypes = (
		("PNG files", "*.png *.PNG"),
		("JPEG files", "*.jpg *.jpeg *.JPG *.JPEG"),
		("HEIC files", "*.heic *.HEIC")
		)
	global filename
	filename = filedialog.askopenfilename(
		title='Open a file',
		initialdir='/',
		filetypes=filetypes
		)

def write():
	message = message_entry.get()
	key = key_entry.get()
	message_entry.delete(0, "end")
	key_entry.delete(0, "end")
	write = Writer(filename, message, key).process_image()
	del(write)

def read():
	key = key_entry.get()
	key_entry.delete(0, "end")
	read = Reader(filename, key).process_image()
	tkinter.messagebox.showinfo(title = "Message", message = read)
	del(read)

message_label = Label(
	root, 
	text = "Message"
	)
message_entry = Entry(
	root,
	width = 25,
	borderwidth = 5
	)
key_label = Label(
	root,
	text = "Key"
	)
key_entry = Entry(
	root,
	width = 25,
	borderwidth = 5
	)
cover_file_label = Label(
	root,
	text = "Cover File"
	)
open_button = Button(
	root,
	text = "Open File",
	command = select_file
	)
read_button = Button(
	root,
	text = "Read",
	command = read
	)
write_button = Button(
	root,
	text = "Write",
	command = write
	)

message_label.grid(row = 0, column = 0)
message_entry.grid(row = 0, column = 1, padx = 1, pady = 1)
key_label.grid(row = 1, column = 0)
key_entry.grid(row = 1, column = 1, padx = 1, pady = 1)
cover_file_label.grid(row = 2, column = 0)
open_button.grid(row = 2, column = 1)
read_button.grid(row = 3, column = 1)
write_button.grid(row = 4, column = 1)

root.mainloop()