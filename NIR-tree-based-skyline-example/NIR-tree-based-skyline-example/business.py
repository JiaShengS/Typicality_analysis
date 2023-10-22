# -*- coding: utf-8 -*-
import json
import gc
import codecs
import random
import re

import nltk

# nltk.download('stopwords')
# from nltk.corpus import stopwords

# noise = set(stopwords.words("english"))

# r='[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'


# file = codecs.open("businessWithoutRow.txt","w","utf-8")
# file = codecs.open("query.txt","w","utf-8")
file = codecs.open("business100.txt","w","utf-8")
with codecs.open('business.json','r') as f:

    rowNum = 100
    row=0
    # file.write('text\n')
    for line in f.readlines():
        #file = open("business.txt","w")
        # line = re.sub(r'[{}]+'.format(r), '', line)

        if row < rowNum:
            item = json.loads(line)
            business_id = item["business_id"]
            name=item["name"]
            latitude = item["latitude"]
            longitude = item["longitude"]
            city = item["city"]
            state = item["state"]
            categories = item["categories"]
            stars = item["stars"]
            row = row + 1
            attr1 = round(random.uniform(0,1),2)
            attr2 = round(random.uniform(0,1),2)
            # attr3 = round(random.uniform(0,1),2)

            # str=business_id+" "+name+" "+latitude+" "+longitude+" "+categories
            file.write("%s^%s^%s^%s %s %s^%s^%s\n" % (row,latitude,longitude,name,city,' '.join(categories),attr1,attr2));
            # file.write(
            #     "%s^%s^%s %s %s\n" % (longitude, latitude, name, city, ' '.join(categories)));
            #
            # file.write("%s@%s@" % (
            #  name, '@'.join(categories)))

            # file.write("%s|%s|%s\n" % (row, latitude, longitude));

    file.close()
f.close()
gc.collect()



