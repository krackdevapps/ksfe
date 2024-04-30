import os
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import cv2 as cv
import numpy as np
import math
import signal

def signal_handler(sig, frame):
    print("\nBye")
    exit(0)
signal.signal(signal.SIGINT, signal_handler)

class KracktonSearchFaceEngine:
    def __init__(self):
        self.folder_path = input("path of folder to search:")
        self.textSearch =  input("word to search in images PNG in folder:")
        self.results_first_step = []

    def extracTextFromImg(self):
        print("Krackton search face engine")
        print("Extracting text of images...")
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                if file.lower().endswith('.png'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as file:
                        image = Image.open(file)
                        texto = pytesseract.image_to_string(image)
                        estructure = {
                            "img": image,
                            "txt": texto,
                            "fileName": os.path.basename(file_path),
                        }
                        self.results_first_step .append(estructure)

        return self.results_first_step 

    def search(self):
        print("Search text in images...")
        searchResults = {"textSearch":   self.textSearch, "images": []}
        results_first_step = self.results_first_step
        textSearchLower =   self.textSearch.lower()
        for container in results_first_step:
            txt = container["txt"]
            img = container["img"]
            fileName = container["fileName"]
            if textSearchLower in txt.lower():
                estructure = {"fileName": fileName, "img": img}
                searchResults["images"].append(estructure)
        self.searchResults = searchResults

    def filterFaces(self, img):
        results = []
        img_cv = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
        gray_img = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)
        face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)
        # Extraer las caras detectadas y mostrarlas
        for x, y, w, h in faces:
            cara = img.crop((x, y, x + w, y + h))
            results.append(cara)
        return results

    def resultsIterator(self):
        listImages = self.searchResults["images"]
        if len(listImages) == 0:
            return print("Results not found")
        for imgDetails in listImages:
            self.constructorSheet(imgDetails)

    def constructorSheet(self, imgDetails):

        img = imgDetails["img"]
        fileName = imgDetails["fileName"]
        print("Searching faces in image {}...".format(fileName))

        facesFounded = self.filterFaces(img)
        thumbnail_size = (
            100,
            100,
        )

        numbersColumns = 5
        sheet_width = thumbnail_size[0] * 5
        space_size_text = 40
        sheet_height = space_size_text
        modeImg = "RGB"
        if len(facesFounded) > 0:
            modeImg = facesFounded[0].mode
            if len(facesFounded) <= numbersColumns:
                sheet_height += thumbnail_size[0]
            else:
                total_elementos = len(facesFounded)
                numero_filas = math.ceil(total_elementos / numbersColumns)
                sheet_height += thumbnail_size[0] * numero_filas
        else:
            sheet_height = space_size_text * 2

        contact_sheet = Image.new(modeImg, (sheet_width, sheet_height))

        font_size = 22
        true_type_font = "files/fanwood-webfont.ttf"
        draw = ImageDraw.Draw(contact_sheet)
        font = ImageFont.truetype(true_type_font, font_size)
        text = "Results found in file {}".format(fileName)
        text_position = (0, 10)
        background_box = [(0, 0), (500, space_size_text)]
        draw.rectangle(background_box, fill="white")
        draw.text(text_position, text, fill="black", font=font)

        if len(facesFounded) == 0:
            text2 = "But there were no faces in that file!"
            text_position2 = (0, 50) 
            background_box2 = [(0, 40), (500, (space_size_text * 2))]
            draw.rectangle(background_box2, fill="white")
            draw.text(text_position2, text2, fill="black", font=font)

        x_img = 0
        y_img = space_size_text

        for img in facesFounded:
            img.thumbnail(thumbnail_size)
            contact_sheet.paste(img, (x_img, y_img))
            x_img += thumbnail_size[0]

            if x_img >= sheet_width:
                x_img = 0
                y_img += thumbnail_size[1]
        # To render in jupiter use display(contact_sheet), in local machine use contact_sheet.show()
        contact_sheet.show()


ksfe = KracktonSearchFaceEngine()
ksfe.extracTextFromImg()
ksfe.search()
ksfe.resultsIterator()


