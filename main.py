import ImageWriter
import math


# Code designed and written by: Selman Tabet

# File Created: September 29, 9:00PM
# Version 1.7, Oct. 10th, 2017.
# Changelog:
# [CODE]
# - Slight adjustment with Decode License Plate function.
# [STYLE]
# - Updated comments for Vertical Segmentation function.
#
# Modification History:
# Start             End
#--------------V1.0--------------
# 9/29  9:30PM      9/30  3:00AM
# 9/30  12:15PM     9/30  10:00PM
# 10/1  12:00AM     10/1  3:00AM
#--------------V1.1--------------
# 10/4  2:00PM      10/4  3:00PM
#--------------V1.2--------------
# 10/5  3:00PM      10/5  5:00PM
# 10/5  10:30PM     10/6  12:45AM
#--------------V1.3--------------
# 10/6  12:50AM     10/6  2:00AM
#--------------V1.4--------------
# 10/6  2:00AM      10/6  2:15AM
#--------------V1.5--------------
# 10/7  1:45AM      10/7  4:00AM
#--------------V1.6--------------
# 10/10 2:00PM      10/10 9:30PM
#--------------V1.7--------------
# 10/10 9:45PM      10/10 9:55PM


def convertBlackWhite(pic):
    W=ImageWriter.getWidth(pic)
    H=ImageWriter.getHeight(pic)
    for i in range(H): #Go over columns
        for j in range(W): #Go over rows
            tpixel=ImageWriter.getColor(pic,j,i)
            avetpixel=(tpixel[0]+tpixel[1]+tpixel[2])/3 #average out the pixels
            if avetpixel>127: #if bright, turn white, grayscale threshold set to 127.
                ImageWriter.setColor(pic,j,i,[255,255,255])
            else:
                ImageWriter.setColor(pic,j,i,[0,0,0]) #if not (is dim), turn black.


def removeBorder(pic): #This function will remove the border of the plate image
    black=[0,0,0]
    white=[255,255,255]
    for i in range(ImageWriter.getHeight(pic)): #Begin scanning from left to right through each row
        x=0
        scan=ImageWriter.getColor(pic,x,i)
        while scan==white and x<ImageWriter.getWidth(pic): #If black is found, start setting all following colors to white until the last black pixel in the sequence.
            scan=ImageWriter.getColor(pic,x,i)
            x+=1
        while scan==black and x<ImageWriter.getWidth(pic):
            scan=ImageWriter.getColor(pic,x,i)
            ImageWriter.setColor(pic,x,i,white)
            x+=1
    for j in range(ImageWriter.getHeight(pic)): #Begin scanning from right to left through each row
        x=ImageWriter.getWidth(pic)-1
        scan=ImageWriter.getColor(pic,x,j)
        while scan==white and x!=0: #If black is found, start setting all following colors to white until the last black pixel in the sequence.
            scan=ImageWriter.getColor(pic,x,j)
            x-=1
        while scan==black and x!=0:
            scan=ImageWriter.getColor(pic,x,j)
            ImageWriter.setColor(pic,x,j,white)
            x-=1

        
def horizontalSegmentation(pic): #picture must have NO BORDERS AT ALL, this will find the starting row and the last row in which the plate number exist.
    black=[0,0,0]
    white=[255,255,255]
    inBlob=False #Initialize variables
    sblob=0 #start of a blob
    result=[] #to store the biggest blob size found yet along with its starting row
    for i in range(ImageWriter.getHeight(pic)): #iterate through all rows
        x=0 #start from left to right when iterating though reach row
        scan=ImageWriter.getColor(pic,x,i)
        getout=0 #This variable helps in defining conditions for the while loop, check below.
        if inBlob==False:
            if scan==black: #if first pixel is black, blob found.
                inBlob=True
                sblob=i
            else: #Otherwise, it must be white
                while scan==white and x<(ImageWriter.getWidth(pic)-1) and inBlob==False and getout==0: #if white, keep going till a blob is found
                    scan=ImageWriter.getColor(pic,x,i)
                    if ImageWriter.getColor(pic,x+1,i)==black: #check neighboring pixel, if black, the current row is part of the blob
                        inBlob=True
                        sblob=i
                        getout=1
                    else:
                        x+=1
        else: #Executed mid-blob/right after blob
            if scan==black: #If first pixel is black, blob found.
                inBlob=True
            else:
                while scan==white and x<(ImageWriter.getWidth(pic)-1) and inBlob==True and getout==0: #getout is necessary here to stop the loop from iterating any further if a black pixel was found in the current row as there is no need to scan any further.
                    scan=ImageWriter.getColor(pic,x,i)
                    if ImageWriter.getColor(pic,x+1,i)==black: #check neighboring pixel, if black, the current row is part of the blob
                        inBlob=True
                        getout=1
                    else:
                        x+=1
                if x==ImageWriter.getWidth(pic)-1 and getout==0: #If we have iterated through the entire row and no black was found, x should be the last pixel.
                    inBlob=False #Current row is not a blob, means that we have already exited the blob we were just scanning
                    blobsize=i-sblob #Calculate the size of the blob
                    if len(result)==0: #If no result was taken yet, just write it in without comparison.
                        result=[sblob,blobsize]
                    elif blobsize>result[1]: #Otherwise, compare to the previous blob size.
                        result=[sblob,blobsize]
    return result

def verticalSegmentation(pic,startrow,endrow,col): #This function will identify the beginning and end columns of the upcoming digit.
    black=[0,0,0] #Initialize variables
    white=[255,255,255]
    blobstart=0 #This is for the first column in the next digit
    pcolor=white #Set previous color to white (assumption)
    digstarted=False #We have not reached a digit yet
    tcol=ImageWriter.getWidth(pic)
    while col<tcol:
        ccolor=white #Assume that there is no black pixel found in the current column.
        row=startrow #Start from the top
        while ccolor==white and row<endrow: #Scan through until a black pixel is found.
            ccolor=ImageWriter.getColor(pic,col,row)
            row+=1
        if ccolor!=pcolor and digstarted==False: #If black and we are not in a digit yet, this means that we just entered a digit.
            digstarted=True
            blobstart=col
            pcolor=ccolor #Changes to black
            col+=1
        elif ccolor!=pcolor and digstarted==True: #If white, then we just exited the digit
            if col-blobstart>5: #Check if not noise.
                return [blobstart,col]
            else:
                pcolor=white #Ignore the small noise.
                col+=1
        else:
            col+=1 #If all fails, we have not come across a black pixel, or we found a black pixel but we are still not at the end of the digit.
                
            
            
                    

def decodeCharacter(pic,startrow,endrow,startcol,endcol):
    black=[0,0,0]
    white=[255,255,255]
    h=range(startcol,endcol)
    v=range(startrow,endrow)
    q1l=float(len(h))/2
    if q1l%2!=0:
        q1l=h[int(q1l-0.5)]
    else:
        return h[int(q1l)]
    q1b=float(len(v))/2
    if q1b%2!=0:
        q1b=v[int(q1b-0.5)]
    else:
        return v[int(q1b)]
    q2t=q1b #Those are to define each quadrant's borders to make it easier to write the foor loop limits.
    q2l=q1l
    q4r=q1l
    q3t=q2t
    q3r=q1l
    q4b=q1b
    blackcountq1=0 #Those are for counting the black and white pixels in each quadrant.
    whitecountq1=0
    blackcountq2=0
    whitecountq2=0
    blackcountq3=0
    whitecountq3=0
    blackcountq4=0
    whitecountq4=0
    
    for i in range(q1l,endcol): #Scan through each row and column of each quadrant and count the amoung of white and black pixels in quadrant.
        for j in range(startrow,q1b):
            scan=ImageWriter.getColor(pic,i,j)
            if scan==black:
                blackcountq1+=1
            else:
                whitecountq1+=1
    
    for i in range(q2l,endcol):
        for j in range(q2t,endrow):
            scan=ImageWriter.getColor(pic,i,j)
            if scan==black:
                blackcountq2+=1
            else:
                whitecountq2+=1

    for i in range(startcol,q3r):
        for j in range(q3t,endrow):
            scan=ImageWriter.getColor(pic,i,j)
            if scan==black:
                blackcountq3+=1
            else:
                whitecountq3+=1

    for i in range(startcol,q4r):
        for j in range(startrow,q4b):
            scan=ImageWriter.getColor(pic,i,j)
            if scan==black:
                blackcountq4+=1
            else:
                whitecountq4+=1
    quadrant=blackcountq1+whitecountq1 #Calculate quadrant area (total number of all pixels in one quadrant).
    Q1=(float(blackcountq1)/quadrant) #Calculate the black ratio of each quadrant and bundle them into a list.
    Q2=(float(blackcountq2)/quadrant)
    Q3=(float(blackcountq3)/quadrant)
    Q4=(float(blackcountq4)/quadrant)
    qlist=[Q1,Q2,Q3,Q4]
    zeroq=[0.21,0.26,0.27,0.31] #Quadrant ratios, in order of inverted cartesian plane convention.
    oneq=[0.16,0.54,0.12,0.58]
    twoq=[0.38,0.23,0.33,0.8]
    threeq=[0.47,0.0,0.34,0.58]
    fourq=[0.1,0.32,0.72,0.58]
    fiveq=[0.52,0.51,0.59,0.37]
    sixq=[0.45,0.43,0.04,0.44]
    sevenq=[0.33,0.25,0.25,0.37]
    eightq=[0.22,0.36,0.4,0.26]
    nineq=[0.52,0.55,0.22,0.8]
    zero=[]
    one=[]
    two=[]
    three=[]
    four=[]
    five=[]
    six=[]
    seven=[]
    eight=[]
    nine=[]
    result=[]
    for i in range(len(qlist)): #Find the difference between each element of quadrant list ratios and each number, sum the difference, then return the lowest value of the result list. The lowest value returned is the sum of the least different character in terms of quadrant ratios.
        zero.append(math.fabs(qlist[i]-zeroq[i]))
    result.append(sum(zero))
    for j in range(len(qlist)):
        one.append(math.fabs(qlist[j]-oneq[j]))
    result.append(sum(one))
    for k in range(len(qlist)):
        two.append(math.fabs(qlist[k]-twoq[k]))
    result.append(sum(two))
    for l in range(len(qlist)):
        three.append(math.fabs(qlist[l]-threeq[l]))
    result.append(sum(three))
    for m in range(len(qlist)):
        four.append(math.fabs(qlist[m]-fourq[m]))
    result.append(sum(four))
    for n in range(len(qlist)):
        five.append(math.fabs(qlist[n]-fiveq[n]))
    result.append(sum(five))
    for o in range(len(qlist)):
        six.append(math.fabs(qlist[o]-sixq[o]))
    result.append(sum(six))
    for p in range(len(qlist)):
        seven.append(math.fabs(qlist[p]-sevenq[p]))
    result.append(sum(seven))
    for q in range(len(qlist)):
        eight.append(math.fabs(qlist[q]-eightq[q]))
    result.append(sum(eight))
    for r in range(len(qlist)):
        nine.append(math.fabs(qlist[r]-nineq[r]))
    result.append(sum(nine))
    return result.index(min(result))


def decodeLicensePlate(filename):
    result=[]
    pic=ImageWriter.loadPicture(filename)
    convertBlackWhite(pic)
    removeBorder(pic)
    rows=horizontalSegmentation(pic)
    j=0
    for i in range(6): #Scan for six characters
        cols=verticalSegmentation(pic,rows[0],rows[1],j) #Use the result from Horizontal Segmentation function for this.
        digit=decodeCharacter(pic,rows[0],rows[1],cols[0],cols[1]) #Use the result from Horizontal Segmentation and Vertical Segmentation functions for this.
        result.append(digit)
        j=(cols[1]+1) #Set it to the empty column and loop to find the next character.
    result= map(str,result)
    return "".join(result) #Return the result as a string.
