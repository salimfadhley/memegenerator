from PIL import Image
import glob, os

size = 128, 128

search_target = os.getcwd() + "/static/img/base_memes/*.jpg"
save_path = os.getcwd() + "/static/img/base_memes/thumbnails/"

for infile in glob.glob(search_target):
    fname, ext = os.path.splitext(infile)
    im = Image.open(infile)
    im = im.copy()
    name = fname.split("/")[-1]
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(save_path + name + ".jpg","JPEG")
