from fpdf import FPDF
from PIL import Image
import time
import os

kindlePath = 'E:\documents'
downloadToKindle = False


def main(title, outfile):
    global pdf
    pdf = FPDF()
    pdf.set_auto_page_break(0)
    print(f'PDFFING: {title}')

    parentFolder = f"{outfile[:outfile.find(title)]}{title}"
    print(parentFolder)
    for folderName in getAllFoldersUnderTitle(parentFolder):
        print(f'----- CHAPTER {folderName} -----')
        formatAllImagesInFolder(f'{parentFolder}\{folderName}')
    convertToPDF(f'{parentFolder}', title)


def getAllFoldersUnderTitle(title):
    return os.listdir(title)


def formatAllImagesInFolder(absolutePath):
    for imageName in getAllFoldersUnderTitle(absolutePath):
        print(f'PDF - Formatting {imageName}')
        imgPath = f'{absolutePath}\{imageName}'
        dimensions = resizeImages(imgPath)
        print(dimensions)
        try:
            pdf.add_page(orientation=dimensions['orientation'])
            pdf.image(imgPath, 0, 0, dimensions['width'], dimensions['height'])
        except RuntimeError:
            print('######################3 INTERLACING TING WTF ##################')


def convertToPDF(absolutePath, title):
    print('Outputting...')
    start = time.time()
    if downloadToKindle is True:
        try:
            pdf.output(kindlePath + f'\{title}' + '.pdf')
        except:
            print('Kindle not connected.')
            pdf.output(absolutePath + '.pdf')
    else:
        pdf.output(absolutePath + '.pdf')
    print("--- %s seconds --- " % (time.time() - start))


def resizeImages(imagePath):
    cover = Image.open(imagePath)
    width, height = cover.size
    # convert pixel in mm with 1px=0.264583 mm
    width, height = float(width * 0.264583), float(height * 0.264583)
    # given we are working with A4 format size
    pdf_size = {'P': {'w': 210, 'h': 270}, 'L': {'w': 270, 'h': 210}}

    # get page orientation from image size
    orientation = 'P' if width < height else 'L'

    #  make sure image size is not greater than the pdf format size
    width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
    height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']

    dimensions = {'orientation': orientation,
                  'width': width,
                  'height': height}
    return dimensions
