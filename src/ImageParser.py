try:
    from PIL import Image
    import PIL.ImageOps

except ImportError:
    import Image
import pytesseract
import os
import re


# Crop and Extracct Data from an Image and Return a set of 2 image playerName and BotArea Images
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
    botresult_img=srcimg.crop(resultbox)
    #botresult_img = resultarea_img.convert('L')
    #resultarea_img.show()

    # Do not merge, it brings error Detection
    #mergeFilteredImage=Image.new('L', (1000, 500),'White')
    #ergeFilteredImage.paste(playernamearea_img)
    #ergeFilteredImage.paste(resultarea_img, (0,100))
    #mergeFilteredImage.show()

    return [playernamearea_img, botresult_img]

def splitBotScore ( scoreLine ):
    words = scoreLine.split()
    botName=words[len(words)-2]
    score=words[len(words)-1]
    score=score.replace('+','').replace(',','')
    return [botName, int(score)]
    #print( "Bot =", botName, " | Score =", score)

def runGuildPlayerNameParser ( text ):
    playername=text[1:4]
    playerguild=text[5:len(text)]
    runTotalResult = 0
    #First Charachter is an opening Bracket
    # 4th is a closing Bracket

    return [playerguild, playername, runTotalResult]

# runResultParser shall have 3 lines
def runResultParser( runText ):
    player1name=""
    player1score=0
    player2name=""
    player2score=0
    player3name=""
    player3score=0
    i=0
    lines = runText.split('\n')
    if ( len(lines) >= 3 ):
        for line in lines:
            # Three Following Lines Shall be player Score
            if (i == 0):
                player1name, player1score = splitBotScore(line)
                #print( "player1name=", player1name )
            if (i == 1):
                player2name, player2score = splitBotScore(line)
                #print( "player2name=", player2name )
            if (i == 2):
                player3name, player3score = splitBotScore(line)
                #print( "player3name=", player3name )
            i+=1
    else:
      print("Failed to parse result, nb lines = ", len(lines) )
      print(runText)

    runResult=[[player1name, player1score],[player2name, player2score],[player3name, player3score]]

    return runResult

def scanAndProcessImgDirectory( dir ):
    with os.scandir( dir ) as entries:
        for entry in entries:
            filename=os.path.abspath(entry)
            runResult=MQProcessRunImageFromFile(filename)
            print("Processing ", filename, " => ", runResult)


def computeRunTotal(playerLine,BotLines):
    player1Score=int(BotLines[0][1])
    player2score=int(BotLines[1][1])
    player3score=int(BotLines[2][1])
    totalScore= player1Score+player2score+player3score
    playerLine[2]=totalScore
    return playerLine

def MQProcessRunImageFromFile( imgPath ):
    #print()
    cropimages = MQCropImage(Image.open(imgPath))
    if (len(cropimages) == 2):
        playername = pytesseract.image_to_string(cropimages[0], config='--psm 6')
        botLines = pytesseract.image_to_string(cropimages[1], config='--psm 6')
        playerLine = runGuildPlayerNameParser(playername)
        botLines = runResultParser(botLines)
        playerLine = computeRunTotal(playerLine, botLines)
        return([playerLine, botLines])
    else:
        print("Failed to get 2 images in result of area boxing")

#def MQProcessRunImageFromURL( imgUrl ):
    # Get Image from URL and store it temporarly

    #img= Image.open()
    # MQProcessRunImageFromFile(

def main():
    # If you don't have tesseract executable in your PATH, include the following:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

    scanAndProcessImgDirectory("../Ressource")

    #imgpath = "../Ressource/Screenshot_20200614-123701_Mighty_Quest.jpg"

    #srcimg = "../Ressource/Screenshot_20200614-102504.png"
    #runResult=MQProcessRunImageFromFile(srcimg)
    #print(runResult)

    #runResult=pytesseract.image_to_string(cropimage,config='--psm 6' )

    #print(runResult)

if __name__ == "__main__":
    main()
