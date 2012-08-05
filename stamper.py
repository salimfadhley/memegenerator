import Image, ImageEnhance, ImageDraw, ImageFont
import os

def top_text_pos(imagesize,textsize,margin):
    xcoord = imagesize[0]/2-textsize[0]/2
    ycoord = margin[1]
    return (xcoord,ycoord)
    
def bottom_text_pos(imagesize,textsize,margin):
    xcoord = imagesize[0]/2-textsize[0]/2
    ycoord = imagesize[1]-textsize[1]-margin[1]
    return (xcoord,ycoord)

def meme_stamp(image_path, toptext, bottomtext, color="white"):
    
    font=ImageFont.truetype("Impact.ttf", 26)
    im = Image.open(os.getcwd() + image_path)
    
    # Gotta capitalize dat text!
    toptext = toptext.upper()
    bottomtext = bottomtext.upper()
    
    # Dat picture margin
    margin=(5,5)
    
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    
    # Make a layer. yep. awesome comment.
    textlayer = Image.new("RGBA", im.size, (0,0,0,0))
    textdraw = ImageDraw.Draw(textlayer)
    
    # Find centered locations for top and bottom text
    toptextsize = textdraw.textsize(toptext, font=font)
    bottomtextsize = textdraw.textsize(bottomtext, font=font)
    toppos = top_text_pos(im.size,toptextsize,margin)
    bottompos = bottom_text_pos(im.size,bottomtextsize,margin)
    
    # Draw dat text
    textdraw.text(toppos, toptext, font=font, fill=color)
    textdraw.text(bottompos, bottomtext, font=font, fill=color)

    # Return dat image
    return Image.composite(textlayer, im, textlayer)


def main():
    meme = meme_stamp("/static/img/allthememes.jpg","make","all the memes")
    meme.show()
    meme.save(os.getcwd() + "/static/img/allthememes-memed.jpg","JPEG")
    

if __name__ == "__main__":
    main()
