try:
    from PIL import Image
    import PIL.ImageOps

except ImportError:
    import Image
import pytesseract
import os


# Crop and Extracct Data from an Image and Return another image containing Relevant Data
def MQCropImage ( srcimg ):
    srcimgheight = srcimg.height
    srcimgwidth = srcimg.width

    ## Extract PlayerNameArea from Img
    # PLAYER NAME BOX : HEIGHT  START 20/2220 = 0.01 - END 75/2220 = 0.04
    areaboxplayernameheightstart=0.01
    areaboxplayernameheightend=0.03
    # PLAYER NAME BOX : WIDTH   START 150/1080 = 0.13 - END 575/1080 = 0.5
    areaboxplayernamewidthstart=0.14
    areaboxplayernamewidthend=0.5

    playernamebox=(srcimgwidth*areaboxplayernamewidthstart, srcimgheight*areaboxplayernameheightstart, srcimgwidth*areaboxplayernamewidthend, srcimgheight*areaboxplayernameheightend)
    playernamearea_img=srcimg.crop(playernamebox)
    playernamearea_img = PIL.ImageOps.invert(playernamearea_img)
    playernamearea_img = playernamearea_img.convert('L')
    #playernamearea_img.show()

    # Extract Result from Img
    # Result BOX : HEIGHT  START 885/2220 = 0.01 - END 1070/2220 = 0.04
    areaboxresultheightstart=0.4
    areaboxresultheightend=0.48
    # PLAYER NAME BOX : WIDTH   START 60/1080 = 0.13 - END 880/1080 = 0.5
    areaboxresultwidthstart=0.055
    areaboxresultwidthend=0.90

    resultbox=(srcimgwidth*areaboxresultwidthstart, srcimgheight*areaboxresultheightstart, srcimgwidth*areaboxresultwidthend, srcimgheight*areaboxresultheightend)
    resultarea_img=srcimg.crop(resultbox)
    resultarea_img = resultarea_img.convert('L')
    #resultarea_img.show()


    mergeFilteredImage=Image.new('L', (1000, 500),'White')
    mergeFilteredImage.paste(playernamearea_img)
    mergeFilteredImage.paste(resultarea_img, (0,100))
    #mergeFilteredImage.show()
    return mergeFilteredImage

def scanAndProcessImgDirectory( dir ):
    with os.scandir( dir ) as entries:
        for entry in entries:
            filename=os.path.abspath(entry)
            print("Processing ", filename)
            srcimg = Image.open(filename)
            runResult=pytesseract.image_to_string(MQCropImage(srcimg))
            print( runResult )


def main():
    # If you don't have tesseract executable in your PATH, include the following:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

    scanAndProcessImgDirectory("../Ressource")

    #imgpath = "../Ressource/Screenshot_20200614-123701_Mighty_Quest.jpg"

    #srcimg = Image.open(imgpath)

    #runResult=pytesseract.image_to_string(MQCropImage(srcimg))

    #print(runResult)

if __name__ == "__main__":
    main()
