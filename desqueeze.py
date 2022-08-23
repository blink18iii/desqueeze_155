# create a script to choose images and desqueeze them from 1.55
from tkinter import filedialog
from tkinter import Tk
from PIL import Image
import os
import PIL

print('select image files:')
root = Tk()
root.filename = filedialog.askopenfilenames(initialdir="/", title="Select files", filetypes=(("image files", "*.jpg"), ("all files", "*.*")))

print('where to save de-squeezed image files:')
root2 = Tk()
root2.withdraw()
folder_selected = filedialog.askdirectory()


for i in root.filename:
    img = Image.open(i)
    width, height = img.size
    if width == 4032 and height == 3024:
        new_image = img.resize((6250, 3024), PIL.Image.Resampling.LANCZOS)
        new_image.save(folder_selected + '/' 'desq_' + os.path.basename(i), quality=100)
    else:
        new_image = img.resize((3024, 6250), PIL.Image.Resampling.LANCZOS)
        new_image.save(folder_selected + '/' 'desq_' + os.path.basename(i), quality=100)

# open selected folder
os.startfile(folder_selected)
print('done')
