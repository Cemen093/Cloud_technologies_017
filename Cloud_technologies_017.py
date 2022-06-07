from urllib.request import urlopen

from functools import partial

import io
import logging
import requests
from io import BytesIO
from PIL import Image, ImageTk, ImageDraw
import tkinter
import json

logger = logging.getLogger(__name__)

imageKey = 0
url = "https://pixabay.com/api/?" + "key=23798924-17f42c690434b5dec74a9c318" + "&image_type=photo&pretty=true"

print(url)

# Create window app
root = tkinter.Tk()
root.title("Pixabay Window App")

# Make workspace
frame = tkinter.Frame(root)
frame.grid()

# Handle for update text from Query
def searched(textInQuery):
    print("\nStart work for search images")
    tmpTextInQuery = textInQuery.get()
    print(tmpTextInQuery)
    # Get Image from new JSON url
    global url
    url = "https://pixabay.com/api/?key=" + APIKEY + "&q=" + tmpTextInQuery + "&image_type=photo&pretty=true"
    response = urlopen(url)
    data_json = json.loads(response.read())
    print(data_json)
    for key, value in data_json.items():
        print(key, value)
    data_json_hits = data_json["hits"]
    print(data_json_hits)
    print(data_json_hits[0])
    urlImage = data_json_hits[0]["largeImageURL"]
    urlImageHeight = data_json_hits[0]["imageHeight"]
    urlImageWidth = data_json_hits[0]["imageWidth"]
    print(urlImage)
    print(urlImageHeight, urlImageWidth)
    # Add Image on Window App
    response = requests.get(urlImage)
    newImage = Image.open(BytesIO(response.content))
    newPhoto = ImageTk.PhotoImage(newImage)
    canvas.itemconfigure(image, image=newPhoto)
    global imageKey
    imageKey = 0
    root.mainloop()

def rightImage():
    print("\nStart work for images forward")
    global imageKey
    imageKey = imageKey + 1
    # Get Image from new JSON url
    global url
    print(url)
    response = urlopen(url)
    data_json = json.loads(response.read())
    print(data_json)
    for key, value in data_json.items():
        print(key, value)
    data_json_hits = data_json["hits"]
    print(data_json_hits)
    print(data_json_hits[imageKey])
    urlImage = data_json_hits[imageKey]["largeImageURL"]
    urlImageHeight = data_json_hits[imageKey]["imageHeight"]
    urlImageWidth = data_json_hits[imageKey]["imageWidth"]
    print(urlImage)
    print(urlImageHeight, urlImageWidth)
    # Add Image on Window App
    response = requests.get(urlImage)
    newImage = Image.open(BytesIO(response.content))
    newPhoto = ImageTk.PhotoImage(newImage)
    canvas.itemconfigure(image, image=newPhoto)
    root.mainloop()

def leftImage():
    pass

# Add Elements on Form
queryText = tkinter.StringVar()
label = tkinter.Label(frame, text="Введите ваш запрос: ").grid(row=1, column=1)
query = tkinter.Entry(frame, width=50, textvariable=queryText).grid(row=1, column=2)
searched = partial(searched, queryText)
but = tkinter.Button(frame, text="Поиск", command=searched).grid(row=1, column=3)
butLeft = tkinter.Button(frame, text="<<<", command=leftImage).grid(row=2, column=1)
butRight = tkinter.Button(frame, text=">>>", command=rightImage).grid(row=2, column=2)


# Dropdown menu of likes
# Create a Tkinter variable
tkvar = tkinter.StringVar(root)

# Dictionary with options
choices = { '>100','>300','>500' }
tkvar.set('>100') # set the default option

popupMenu = tkinter.OptionMenu(frame, tkvar, *choices)
tkinter.Label(frame, text="Choose a quantity of likes").grid(row = 3, column = 1)
popupMenu.grid(row = 4, column =1)

# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )

# Dropdown menu of comments
# Create a Tkinter variable
tkvarComments = tkinter.StringVar(root)

# Dictionary with options
choicesComments = { '>100','>300','>500' }
tkvar.set('>100') # set the default option

popupMenuComments = tkinter.OptionMenu(frame, tkvar, *choices)
tkinter.Label(frame, text="Choose a quantity of comments").grid(row = 3, column = 2)
popupMenuComments.grid(row = 4, column =2)

# on change dropdown value
def change_dropdownComments(*args):
    print( tkvar.get() )

# link function to change dropdown
tkvar.trace('w', change_dropdownComments)

# JSON Get Image parameters
url = "https://pixabay.com/api/?key=" + APIKEY + "&image_type=photo&pretty=true"
response = urlopen(url)
data_json = json.loads(response.read())
print(data_json)
for key, value in data_json.items():
    print(key, value)
data_json_hits = data_json["hits"]
print(data_json_hits)
print(data_json_hits[0])
urlImage = data_json_hits[0]["largeImageURL"]
urlImageHeight = data_json_hits[0]["imageHeight"]
urlImageWidth = data_json_hits[0]["imageWidth"]
print(urlImage)
print(urlImageHeight, urlImageWidth)

# Add Image on Window App
canvas = tkinter.Canvas(root, height=urlImageHeight, width=urlImageWidth)
response = requests.get(urlImage)
image = Image.open(BytesIO(response.content))
photo = ImageTk.PhotoImage(image)
image = canvas.create_image(0, 0, anchor='nw', image=photo)
canvas.grid(row=1, column=3)

# Root Update Frame
root.mainloop()

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

def show_bounding_boxes(image_bytes, box_sets, colors):
    image = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)
    for boxes, color in zip(box_sets, colors):
        for box in boxes:
            left = image.width * box['Left']
            top = image.height * box['Top']
            right = (image.width * box['Width']) + left
            bottom = (image.height * box['Height']) + top
            draw.rectangle([left, top, right, bottom], outline=color, width=3)
    image.show()


def show_polygons(image_bytes, polygons, color):
    image = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)
    for polygon in polygons:
        draw.polygon([
            (image.width * point['X'], image.height * point['Y']) for point in polygon],
            outline=color)
    image.show()


class RekognitionFace:
    def __init__(self, face, timestamp=None):
        self.bounding_box = face.get('BoundingBox')
        self.confidence = face.get('Confidence')
        self.landmarks = face.get('Landmarks')
        self.pose = face.get('Pose')
        self.quality = face.get('Quality')
        age_range = face.get('AgeRange')
        if age_range is not None:
            self.age_range = (age_range.get('Low'), age_range.get('High'))
        else:
            self.age_range = None
        self.smile = face.get('Smile', {}).get('Value')
        self.eyeglasses = face.get('Eyeglasses', {}).get('Value')
        self.sunglasses = face.get('Sunglasses', {}).get('Value')
        self.gender = face.get('Gender', {}).get('Value', None)
        self.beard = face.get('Beard', {}).get('Value')
        self.mustache = face.get('Mustache', {}).get('Value')
        self.eyes_open = face.get('EyesOpen', {}).get('Value')
        self.mouth_open = face.get('MouthOpen', {}).get('Value')
        self.emotions = [emo.get('Type') for emo in face.get('Emotions', [])
                         if emo.get('Confidence', 0) > 50]
        self.face_id = face.get('FaceId')
        self.image_id = face.get('ImageId')
        self.timestamp = timestamp

    def to_dict(self):
        rendering = {}
        if self.bounding_box is not None:
            rendering['bounding_box'] = self.bounding_box
        if self.age_range is not None:
            rendering['age'] = f'{self.age_range[0]} - {self.age_range[1]}'
        if self.gender is not None:
            rendering['gender'] = self.gender
        if self.emotions:
            rendering['emotions'] = self.emotions
        if self.face_id is not None:
            rendering['face_id'] = self.face_id
        if self.image_id is not None:
            rendering['image_id'] = self.image_id
        if self.timestamp is not None:
            rendering['timestamp'] = self.timestamp
        has = []
        if self.smile:
            has.append('smile')
        if self.eyeglasses:
            has.append('eyeglasses')
        if self.sunglasses:
            has.append('sunglasses')
        if self.beard:
            has.append('beard')
        if self.mustache:
            has.append('mustache')
        if self.eyes_open:
            has.append('open eyes')
        if self.mouth_open:
            has.append('open mouth')
        if has:
            rendering['has'] = has
        return rendering


class RekognitionCelebrity:
    def __init__(self, celebrity, timestamp=None):
        self.info_urls = celebrity.get('Urls')
        self.name = celebrity.get('Name')
        self.id = celebrity.get('Id')
        self.face = RekognitionFace(celebrity.get('Face'))
        self.confidence = celebrity.get('MatchConfidence')
        self.bounding_box = celebrity.get('BoundingBox')
        self.timestamp = timestamp

    def to_dict(self):
        rendering = self.face.to_dict()
        if self.name is not None:
            rendering['name'] = self.name
        if self.info_urls:
            rendering['info URLs'] = self.info_urls
        if self.timestamp is not None:
            rendering['timestamp'] = self.timestamp
        return rendering


class RekognitionPerson:
    def __init__(self, person, timestamp=None):
        self.index = person.get('Index')
        self.bounding_box = person.get('BoundingBox')
        face = person.get('Face')
        self.face = RekognitionFace(face) if face is not None else None
        self.timestamp = timestamp

    def to_dict(self):
        rendering = self.face.to_dict() if self.face is not None else {}
        if self.index is not None:
            rendering['index'] = self.index
        if self.bounding_box is not None:
            rendering['bounding_box'] = self.bounding_box
        if self.timestamp is not None:
            rendering['timestamp'] = self.timestamp
        return rendering


class RekognitionLabel:
    def __init__(self, label, timestamp=None):
        self.name = label.get('Name')
        self.confidence = label.get('Confidence')
        self.instances = label.get('Instances')
        self.parents = label.get('Parents')
        self.timestamp = timestamp

    def to_dict(self):
        rendering = {}
        if self.name is not None:
            rendering['name'] = self.name
        if self.timestamp is not None:
            rendering['timestamp'] = self.timestamp
        return rendering


class RekognitionModerationLabel:
    def __init__(self, label, timestamp=None):
        self.name = label.get('Name')
        self.confidence = label.get('Confidence')
        self.parent_name = label.get('ParentName')
        self.timestamp = timestamp

    def to_dict(self):
        rendering = {}
        if self.name is not None:
            rendering['name'] = self.name
        if self.parent_name is not None:
            rendering['parent_name'] = self.parent_name
        if self.timestamp is not None:
            rendering['timestamp'] = self.timestamp
        return rendering


class RekognitionText:
    def __init__(self, text_data):
        self.text = text_data.get('DetectedText')
        self.kind = text_data.get('Type')
        self.id = text_data.get('Id')
        self.parent_id = text_data.get('ParentId')
        self.confidence = text_data.get('Confidence')
        self.geometry = text_data.get('Geometry')

    def to_dict(self):
        rendering = {}
        if self.text is not None:
            rendering['text'] = self.text
        if self.kind is not None:
            rendering['kind'] = self.kind
        if self.geometry is not None:
            rendering['polygon'] = self.geometry.get('Polygon')
        return rendering