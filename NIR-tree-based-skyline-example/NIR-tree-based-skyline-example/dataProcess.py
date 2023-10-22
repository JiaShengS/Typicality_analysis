# -*- coding: utf-8 -*-
import json
import gc
import codecs
import random
import re
import pandas as pd
import numpy as np

file = codecs.open("CrimeData400test.csv","w","utf-8")
with codecs.open('Crimes_2001_to_present.csv','r') as f:
    '''
    ID,
    Case Number,
    Date,
    Block,
    IUCR,
    Primary Type,
    Description,
    Location Description,
    Arrest,
    Domestic,
    Beat,
    District,
    Ward,
    Community Area,
    FBI Code,
    X Coordinate,
    Y Coordinate,
    Year,
    Updated On,
    Latitude,
    Longitude,
    Location

    '''
    rowNum = 400
    row = 0
    # file.write('lat,lon\n')
    str1 = ''
    count = 0
    for line in f.readlines():
        data = line.split(',')
        ID = data[0],
        # print(ID)
        CaseNumber = data[1],
        # print(CaseNumber)
        Date = data[2],
        Block = data[3],
        IUCR = data[4],
        PrimaryType = data[5],
        Description = data[6],
        LocationDescription = data[7],
        Arrest = data[8],

        Domestic = data[9],

        Beat = data[10],

        District = data[11],

        Ward = data[12],

        CommunityArea = data[13],
        # print(CommunityArea[0])
        FBICode = data[14],
        XCoordinate = data[15],
        YCoordinate = data[16],
        Year = data[17],
        UpdatedOn = data[18],
        Latitude = data[19],
        Longitude = data[20],
        Location = data[21],

        attr1 = round(random.uniform(0, 1), 2)
        attr2 = round(random.uniform(0, 1), 2)

        # str1 = ID[0]+","+Longitude[0] + "," + Latitude[0] +","+CaseNumber[0] +","+ Date[0]+","+ Block[0] \
        #        + "," +IUCR[0]+","+PrimaryType[0]+","+Description[0]+","+LocationDescription[0]+","+Year[0]+","+\
        #        Arrest[0]+","+Domestic[0]+","+Beat[0]+","+District[0]+","+XCoordinate[0]+","+YCoordinate[0]+","+\
        #        Ward[0]+","+CommunityArea[0]+","+str(attr1)+","+str(attr2)
        str1 = "".join(ID)+"," + "".join(Longitude) +"," + "".join(Latitude)+"," + "".join(CaseNumber)+"," +\
               "".join(Date)+"," +\
               "".join(Block)+"," + "".join(IUCR)+"," + "".join(PrimaryType)+"," + "".join(Description)+"," +\
               "".join(LocationDescription)+"," + "".join(Year)+"," + "".join(Arrest)+"," + \
               "".join(Domestic) + "," + "".join(Beat) + "," + "".join(District) + "," + \
               "".join(XCoordinate) + "," + "".join(YCoordinate) + "," + "".join(Ward) + "," + \
               "".join(CommunityArea)+"," + "".join(str(attr1))+"," + "".join(str(attr2))
        # print(str1)
        if count <= rowNum:
            if str(XCoordinate[0]) != '':
                count += 1
                str1 = str1.replace("TRUE", '1')
                str1 = str1.replace("FALSE", '0')
                file.write(str1 + "\n")

