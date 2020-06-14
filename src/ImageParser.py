try:
    from PIL import Image
    import PIL.ImageOps

except ImportError:
    import Image
import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

imgpath= "../Ressource/Screenshot_20200614-123701_Mighty_Quest.jpg"

srcimg=Image.open(imgpath)
srcimgheight=srcimg.height
srcimgwidth=srcimg.width


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

# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# Simple image to string
print(pytesseract.image_to_string(mergeFilteredImage))

# French text image to string
#print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))



# Timeout/terminate the tesseract job after a period of time

# Get bounding box estimates
#print(pytesseract.image_to_boxes(Image.open('test.png')))

# Get verbose data including boxes, confidences, line and page numbers
#print(pytesseract.image_to_data(Image.open(imgpath)))
