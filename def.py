    Height=0
    Black=[0,0,0]
    White=[255,255,255]
    BlobCount=0
    BlobList=[]
    for Height in range(getHeight(pic)):
        Width=0
        while getColor(pic,Width,Height)==White:
            Width+=1
        if getColor(pic,Width,Height)==Black:
            BlobCount+=1
        else:
            BlobList.append(BlobCount)
            BlobCount=0
        continue
