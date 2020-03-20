from ImageWriter import*
# Task 1
# Code designed and written by: Selmane Tabet
# Andrew ID: stabet
# File Created: October 10, 1:55PM
# Modification History:
#Originally created on Octorber 8, 12:45PM but the file got destroyed due to sudden PC data loss, recreated a new version.
# Start             End
# 10/10  1:55PM     10/10 2:40PM
# 10/10  3:30PM     10/10 5:30PM
# 10/11  5:00PM     10/11 9:50PM


def convertBlackWhite(pic):
    Height=getHeight(pic)        #Retrieve height in pixels
    Width=getWidth(pic)          #Retrieve width in pixels
    for x in range(0,Height):    #Goes over every pixel row
        for i in range(0,Width): #Goes over every pixel column
            Color=getColor(pic,i,x) #Retrieve pixel color in RGB form
            ColorAverage=(Color[0]+Color[1]+Color[2])/3 #Read average color in the pixel
            if ColorAverage>125: #If the average leans more towards black, make it black
                setColor(pic,i,x,[255,255,255])
            else:
                setColor(pic,i,x,[0,0,0]) #Set to white otherwise.

#Task 2

def removeBorder(pic):
    Black=[0,0,0]
    White=[255,255,255]
    for Height in range(getHeight(pic)):         #Loop across the whole height
        Width=0
        while getColor(pic,Width,Height)==White: #Skip the whites
            Width+=1
        while getColor(pic,Width,Height)==Black: #Overwrite the blacks
            Width+=1
            setColor(pic,Width,Height,White)
            Width+=1


#Task 3
            
def horizontalSegmentation(pic):
    InitialHeight=0
    inBlob=False
    Black=[0,0,0]
    White=[255,255,255]
    HList=[]
    BlobCount=0
    BlobSize=0
    maxBlob=0
    for Height in range(getHeight(pic)):
        Width=0
        while getColor(pic,Width,Height)==White and inBlob is False: #Scan for blob
            Width+=1
        if getColor(pic,Width,Height)==Black and inBlob is False:    #Detecting the first blob
            inBlob=True
            InitialHeight=Height
        if getColor(pic,Width,Height)==White and inBlob is True:     #End of blob
            inBlob=False
            FinalHeight=Height
            Size=FinalHeight-InitialHeight
            HList.append(Size)                                       #Append to the list of blob sizes
            HList.sort()
            HList.reverse()
            if Size>=HList[0]:                                       #Check if this is the biggest blob yet
                maxBlob=Size
                Result=[InitialHeight,FinalHeight]
    return Result


#Task 4

def verticalSegmentation(pic,StartRow,EndRow,Column):
    Black=[0,0,0]
    White=[255,255,255]
    FirstRow=EndRow
    InitialColumn=0
    BlackSize=0
    while BlackSize<5 or Column<getWidth(pic):           #While loop in case the program goes over a small dot (noise)
        InitialColumn=0
        BlackSize=0
        while EndRow<StartRow:                           #Scan for black
           while getColor(pic,Column,EndRow)==White:
                EndRow+=1
           if InitialColumn==0:                          #Assign value for starting column
                InitialColumn=Column
           Column+=1
           EndRow=FirstRow
        FinalColumn=Column                               #Assign value for finishing column
        BlackSize=FinalColumn-InitialColumn
        Column+=1
        EndRow=FirstRow
    return [InitialColumn,FinalColumn] 


#Task 5

def decodeCharacter(pic,startrow,endrow,startcol,endcol):
    Black=[0,0,0]
    White=[255,255,255]
    HalfWidth=startcol,endcol
    HalfHeight=startrow-endrow
    BlackCounter=0
    WhiteCounter=0
    Counter=0
    for w1 in range(HalfWidth):                         #Assuming upper left quadrant is Q1, upper right is Q2, lower left is Q3 and lower right is Q4
        for h1 in range(HalfHeight):                    #Start with Q3
            if getColor(pic,w1,h1)==Black:
                BlackCounter+=1
                Counter+=1
            if getColor(pic,w1,h1)==White:
                WhiteCounter+=1
                Counter+=1
    Q3=BlackCounter/Counter
    BlackCounter=0
    WhiteCounter=0
    Counter=0
    for w2 in range(HalfWidth):                         #for Q1
        for h2 in range(HalfHeight,startrow):
            if getColor(pic,w2,h2)==Black:
                BlackCounter+=1
                Counter+=1
            if getColor(pic,w2,h2)==White:
                WhiteCounter+=1
                Counter+=1
    Q1=BlackCounter/Counter
    BlackCounter=0
    WhiteCounter=0
    Counter=0
    for w3 in range(HalfWidth,endcol):                  #for Q4
        for h3 in range(HalfHeight):
            if getColor(pic,w3,h3)==Black:
                BlackCounter+=1
                Counter+=1
            if getColor(pic,w3,h3)==White:
                WhiteCounter+=1
                Counter+=1
    Q4=BlackCounter/Counter
    BlackCounter=0
    WhiteCounter=0
    Counter=0
    for w4 in range(HalfWidth,endcol):                  #for Q2
        for h4 in range(HalfHeight,startrow):
            if getColor(pic,w4,h4)==Black:
                BlackCounter+=1
                Counter+=1
            if getColor(pic,w4,h4)==White:
                WhiteCounter+=1
                Counter+=1
    Q2=BlackCounter/Counter
    QList=[Q1,Q2,Q3,Q4]                                 #Quadrant black ratio list
    Zero=[0.21,0.31,0.27,0.26]                          #List of quadrant black ratios for all digits
    One=[0.16,0.58,0.12,0.54]
    Two=[0.38,0.8,0.33,0.23]
    Three=[0.47,0.58,0.34,0]
    Four=[0.1,0.58,0.72,0.32]
    Five=[0.52,0.37,0.59,0.51]
    Six=[0.45,0.44,0.04,0.43]
    Seven=[0.33,0.37,0.25,0.25]
    Eight=[0.22,0.26,0.4,0.36]
    Nine=[0.52,0.8,0.22,0.55]
    SumDifZero=sum(Zero-QList)/4
    SumDifOne=sum(One-QList)/4
    SumDifTwo=sum(Two-QList)/4
    SumDifThree=sum(Three-QList)/4
    SumDifFour=sum(Four-QList)/4
    SumDifFive=sum(Five-QList)/4
    SumDifSix=sum(Six-QList)/4
    SumDifSeven=sum(Seven-QList)/4
    SumDifEight=sum(Eight-QList)/4
    SumDifNine=sum(Nine-QList)/4
    List=[SumDifZero,SumDifOne,SumDifTwo,SumDifThree,SumDifFour,SumDifFive,SumDifSix,SumDifSeven,SumDifEight,SumDifNine]
    List.sort()                                         #Finding the smallest sum of differences of quadrant ratios, giving the closest approximation to the number displayed
    if List[0]==SumDifZero:
        return 0
    if List[0]==SumDifOne:
        return 1
    if List[0]==SumDifTwo:
        return 2
    if List[0]==SumDifThree:
        return 3
    if List[0]==SumDifFour:
        return 4
    if List[0]==SumDifFive:
        return 5
    if List[0]==SumDifSix:
        return 6
    if List[0]==SumDifSeven:
        return 7
    if List[0]==SumDifEight:
        return 8
    if List[0]==SumDifNine:
        return 9

#Task 6

def decodeLicensePlate(filename):
    picture=loadPicture(filename)
    convertBlackWhite(picture)
    removeBorder(picture)
    hs=horizontalSegmentation(picture)
    Start=hs[1]                                             #Mark horizontal segments
    End=hs[0]
    vs1=verticalSegmentation(picture,Start,End,0)
    Column2start=vs1[0]                                     #Mark vertical segments for all numbers
    Column2=vs1[1]
    vs2=verticalSegmentation(picture,Start,End,Column2)
    Column3start=vs2[0]
    Column3=vs2[1]
    vs3=verticalSegmentation(picture,Start,End,Column3)
    Column4start=vs3[0]
    Column4=vs3[1]
    vs4=verticalSegmentation(picture,Start,End,Column4)
    Column5start=vs4[0]
    Column5=vs4[1]
    vs5=verticalSegmentation(picture,Start,End,Column5)
    Column6start=vs5[0]
    Column6=vs5[1]
    vs6=verticalSegmentation(picture,Start,End,Column6)
    Column7start=vs6[0]
    Column7=vs6[1]
    N1=decodeCharacter(pic,Start,End,Column2start,Column2)  #Decode each character enclosed in the segments
    N2=decodeCharacter(pic,Start,End,Column3start,Column3)
    N3=decodeCharacter(pic,Start,End,Column4start,Column4)
    N4=decodeCharacter(pic,Start,End,Column5start,Column5)
    N5=decodeCharacter(pic,Start,End,Column6start,Column6)
    N6=decodeCharacter(pic,Start,End,Column7start,Column7)
    PlateNumber="".join([N1,N2,N3,N4,N5,N6])                #Join a list containing the six numbers into an empty string to form a string containing the plate number
    return PlateNumber
