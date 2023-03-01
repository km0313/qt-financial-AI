from PIL import Image,ImageDraw,ImageFont
import random
class memegenerator():

    def __init__(self,output_dir) -> None:
        self.out_dir=output_dir

    def make_meme(self,img_path,txt,author,width=500):
        try:
            img = Image.open(img_path)
        except Exception as ex:
            print(f'Exception: {ex}')
        else:
            img=Image.open(img_path)
            ratio=width/float(img.size[0])
            height=int(ratio*float(img.size[1]))
            img=img.resize((width,height),Image.Resampling.NEAREST)

            draw=ImageDraw.Draw(img)
            font = ImageFont.truetype(font='./font/LilitaOne-Regular.ttf', size=int(height/20))
            draw.text(xy=(10,30),text=f"{txt}-{author}",font=font)
            out_path = f'{self.out_dir}/{random.randint(0, 1000000)}.jpeg'
            img.save(out_path)
            return out_path
    
if __name__=='__main__':
    meme=memegenerator('./tmp.jpg')
    meme.make_meme('Lesson 7. Project - Starter Code/_data/photos/dog/xander_1.jpg','hello','world')
'''
if message is not None:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./fonts/LilitaOne-Regular.ttf', size=20)
        draw.text((10, 30), message, font=font, fill='white')
    
    img.save(out_path)
    return out_path

if __name__=='__main__':
    print(generate_postcard('./imgs/img.jpg', 
                            './imgs/out.jpg',
                            'woof!',
                            (450, 900, 900, 1300),
                            200))
'''