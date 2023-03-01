import random
import os
import requests
from flask import Flask, render_template, abort, request
from QuoteEngine import ingestor
from MemeEngine import memegenerator


app = Flask(__name__)

meme = memegenerator('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # TODO: Use the Ingestor class to parse all files in the
    # quote_files variable
    quotes=[]
    for file in quote_files:
        if ingestor.parse(file) is not None:
            quotes.append(ingestor.parse(file))
    

    images_path = "./_data/photos/dog/"

    # TODO: Use the pythons standard library os class to find all
    # images within the images images_path directory
    imgs=[]
    for paths in os.listdir(images_path):
        imgs.append(os.path.join(images_path,paths))


    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """
    quotes, imgs = setup()
    quotes_list = random.choice(quotes)
    quote = random.choice(quotes_list)
    img=random.choice(imgs)
    # @TODO:
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    # @TODO:
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    # 3. Remove the temporary saved image.

    image_url = request.form['image_url']
    body = request.form['body']
    author = request.form['author']
    img = requests.get(image_url)
    path = None
    try:
        img_file = f'tmp/{random.randint(0, 100000000)}.jpg'
        open(img_file, 'wb').write(img.content)
    except:
        print("Could not load image")
        path = meme.make_meme('./_data/photos/dog/xander_1.jpg', "This is a default quote", "Stanley Dukor")
    else:
        path = meme.make_meme(img_file, body, author)
        os.remove(img_file)
    finally:
        return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
