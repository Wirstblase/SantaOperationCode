'''
current stats: ~52 de ore -  2 miliarde de scrisori
~2 milioane de scrisori -> 188 secunde
sa le multumiti lui Suflea si lui Laur =))
'''
import re
import json
import codecs
import time
import os
import base64
import google_images_download
import random
from PIL import Image
from pathlib import Path
import pycountry_convert as pc

start_time = time.time()
secvname = ["My name is ", "I am ", "I'm ", "Im"]
secvaddress = ['exp:', 'expeditor:', "Exp:", 'Expeditor:']
secvgifts = ['This year I want ', 'I want to receive ', 'I wish to get ', 'I would like ', 'I would love ',
             'I would like to receive ', 'I wish for ', 'I would like to get ', 'My wish is to receive ']


def find_and_add_name(letter):
    for txt in secvname:
        if re.search(txt, letter) != None:
            x = re.search(txt, letter).span()
            i = x[1]
            if letter[i].isupper():
                n = ''
                while letter[i] != ',' and letter[i] != '.':
                    n = n + letter[i]
                    i += 1
                    if letter[i] == ' ':
                        if letter[i + 1].isupper() == False:
                            break
        #print("--- %s seconds NAME---" % (time.time() - start_time))
        #n = n.split("'","")
        return n


def find_and_add_address(letter):
    for txt in secvaddress:
        if re.search(txt, letter) != None:
            x = re.search(txt, letter).span()
            i = x[1]
            if letter[i] == " ":
                a = letter[i + 1:len(letter)]
            else:
                a = letter[i:len(letter)]
    if a.find(', nr.'):
        a = a.replace('str. ', '').replace(', nr. ', ',')
    if a.find(' nr.'):
        a = a.replace('str. ', '').replace(' nr. ', ',')
    l = re.split(',', a)
    for i in range(len(l)):
        l[i] = l[i].strip()
        l[i] = l[i].replace("'","")

        l[3] = l[3].replace("'","")
        #print("--- %s seconds ADDRESS ---" % (time.time() - start_time))
        return l


def find_and_add_gifts(letter):
    for txt in secvgifts:
        i = letter.rfind(txt)
        if i != -1:
            a = len(txt)
            q = a + i
            g = ""
            while letter[q] not in ['?', '.', '!', '\n']:
                g = g + letter[q]
                q += 1
            if re.search(' and ', g) != None:
                g = re.sub(' and', ',', g)
    g = g.replace(' a ', '').replace(' an ', '')
    l = re.split(',', g)
    for i in range(len(l)):
        l[i] = l[i].lstrip('a').lstrip('n')
        l[i] = l[i].strip()
        l[i] = l[i].replace("'","")
    for i in range(len(l)):
        if len(l[i])<=2:
            l[i]="candy"
    #print("--- %s seconds GIFTS ---" % (time.time() - start_time))
    return l


def find_and_add_color(letter):
    i = letter.find('colour')
    if i != -1:
        a = len('colour')
        q = a + i
        g = ""
        while letter[q] not in ['?', '.', '!', '\n', ',']:
            g = g + letter[q]
            q += 1
    else:
        return None
    #print("--- %s seconds COLOR ---" % (time.time() - start_time))
    return g.strip()


#L = []


def dictionary(letter):
    d = {'name': '',
         'address': '',
         'gifts': '',
         'color': None}
    try:
        d['name'] = find_and_add_name(letter)
    except:
        pass
    d['address'] = find_and_add_address(letter)
    d['gifts'] = find_and_add_gifts(letter)
    d['color'] = find_and_add_color(letter)
    #print("--- %s seconds DICTIONARY ---" % (time.time() - start_time))
    return d


a = Path(__file__)
found = 0
i = len(str(a)) - 1
b = str(a)
while found == 0:
    if b[i] != os.sep:
        b = b[0:i]
    else:
        found = 1
    i -= 1
b = b + "input"

txt_folder = Path(b).rglob('*.txt')
files = [x for x in txt_folder]


'''for name in files:
    with open(name, 'r+') as f:
        l = f.read()
        l = l.replace("\n", "").replace("\r", "").replace("exp:", " exp: ").replace(" , ", ",")
        a = re.split('n\*r=[0-9]+', l)
        while a[0] == '':
            a.pop(0)
            if (a[0] == ''):
                print('nu e bine')
        for line in a:
            L.append(dictionary(line))
            pass'''

def processedLetter(l):
    l = l.replace("\n", "").replace("\r", "").replace("exp:", " exp: ").replace(" , ", ",")
    a = []
    a = re.split('n\*r=[0-9]+', l)

    varr = ""
    
    while a[0] == '':
        a.pop(0)

    #print(a)

    #print("--- %s seconds starts generating dictionary ---" % (time.time() - start_time))

    L = []
        #if (a[0] == ''):
        #    print('nu e bine')
    for line in a:
        L.append(dictionary(line))
        #varr = varr + str(dictionary(line)) + ","

        

    #print("--- %s seconds done generating dictionary ---" % (time.time() - start_time))

        
        #print("END")
    #varr = varr.replace("'","\"")
    #print("--- %s seconds PROCESSEDLETTER ---" % (time.time() - start_time))
    #return dictionary(a[0])
    return L

    

scrisoare = ""
print("execution started")

errcounter = 0

out_file = open('./output.json', 'w+')
out_file.write("[")

chunki = 0 #Lau's baby <3 we love chunki
maxchunksize = 10000

#out_file = open('./output.json', 'a+')

for name in files:
    with open(name, 'r+') as f:
        reset = 1
        
        while True:
        
            l = f.readline()
            
        
            if "n*r" in l:
                reset = 1
                chunki = chunki+1


            if(reset == 1): #done loading a letter
                
                if(errcounter == 1 and chunki > maxchunksize):

                    #print(scrisoare)
                    #print("--- %s seconds starts processing ---" % (time.time() - start_time))
                        
                    lett = processedLetter(scrisoare)
                    outputt = str(lett).replace("\"","").replace("'","\"")

                    #print("--- %s seconds done processing ---" % (time.time() - start_time))
                    out_file.write(outputt)
                    out_file.write(",")
                    print("--- %s seconds written 10k to file ---" % (time.time() - start_time))

                    #print(lett)

                    scrisoare = ""
                    chunki = 0
                    
                    #print("--- %s seconds AFTERWRITE ---" % (time.time() - start_time))
                
                reset = 0
                errcounter = 1
        
            #print("TEST")

                
            #print("--- %s seconds before append---" % (time.time() - start_time))
            scrisoare = scrisoare + l
            #print("--- %s seconds after append ---" % (time.time() - start_time))

            if not l:
                break

out_file.close()


import os
with open('./output.json', 'rb+') as filehandle:
    filehandle.seek(-1, os.SEEK_END)

    '''while(filehandle.read(1) & 0xC0 == 0x80):
        filehandle.seek(-2,os.SEEK_CUR)

    filehandle.seek(-1,os.SEEK_CUR)'''
    filehandle.truncate()


out_file = open('./output.json', 'a+')
out_file.write("]")
out_file.close()


print("DONE WRITING OUTPUT FILE")
        


#out_file = open('./output.json', 'w+')
#json.dump(L, out_file, indent=2)
#out_file.close()


# print("--- %s seconds ---" % (time.time() - start_time))
##for dicti in L:
##  print(dicti)

'''
class Child:

    def __init__(self, name, address, gifts_wish, color):
        self.name = name
        self.address = address
        self.gifts_wish = gifts_wish
        self.color = color


def create_children_array(fileName):  # reads JSON input and creates an array of children
    children = []
    with open(fileName, 'rb') as reading_output:
        reading_dict = json.load(reading_output)
        for elem in reading_dict:
            child = Child(elem['name'], elem['address'], elem['gifts'], elem['color'])
            children.append(child)

    return children


def get_gift(giftName):  # removes "a" or "an" from string
    stringList = giftName.split()
    newString = ""
    for i in stringList:
        if (i != "a" and i != "an"):
            if (newString == ""):
                newString += i
            else:
                newString += (" " + i)
    return newString


#STATS
def AddPresents(child, country_stats):  # adds all presents (from current child) to its respective country
    Country = child.address
    Country = Country[len(child.address) - 1]
    Presents = child.gifts_wish
    if Country in country_stats:
        for i in Presents:
            giftName = get_gift(i)
            for j in country_stats[Country]:
                ok = 0
                if giftName == j[0]:
                    j[1] += 1
                    ok = 1
                    break
            if ok == 0:
                country_stats[Country].append([giftName, int(1)])
    else:
        country_stats[Country] = []
        for i in Presents:
            giftName = get_gift(i)
            country_stats[Country].append([giftName, int(1)])
    return country_stats


#STATS
def gift_stats(childList, filename_w1, filename_w2):  # generates both gift stats worldwide and top 3 per country
    stats = dict()
    country_stats = dict()

    for child in childList:
        country_stats = AddPresents(child, country_stats)
        for j in child.gifts_wish:
            giftName = get_gift(j)
            if giftName in stats:
                stats[giftName] += 1
            else:
                stats[giftName] = 1

    for i in country_stats:
        nr1 = ["Nr. 1: ", 'NONE', int(0)]
        nr2 = ["Nr. 2: ", 'NONE', int(0)]
        nr3 = ["Nr. 3: ", 'NONE', int(0)]
        for j in country_stats[i]:
            if j[1] >= nr1[2]:
                nr3[1] = nr2[1]
                nr3[2] = nr2[2]

                nr2[1] = nr1[1]
                nr2[2] = nr1[2]

                nr1[1] = j[0]
                nr1[2] = j[1]
            elif j[1] >= nr2[2]:
                nr3[1] = nr2[1]
                nr3[2] = nr2[2]

                nr2[1] = j[0]
                nr2[2] = j[1]
            elif j[1] >= nr3[2]:
                nr3[1] = j[0]
                nr3[2] = j[1]

        if nr2[1] == 'NONE':
            country_stats[i] = [nr1]
        elif nr3[1] == 'NONE':
            country_stats[i] = [nr1, nr2]
        else:
            country_stats[i] = [nr1, nr2, nr3]

    stats = dict(sorted(stats.items(), key=lambda item: item[1], reverse=True))
    with open(filename_w1, 'w') as file:
        json.dump(stats, file, indent=4)
    with open(filename_w2, 'w') as file:
        json.dump(country_stats, file, indent=4)


def country_to_continent(country_name):
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name


def sortByCountry(children):
    return sorted(children, key=lambda x: (x.address[-1], x.address[-2]))


childList = create_children_array("output.json")  # list of children, contains every child (object)

gift_stats(childList, 'gift_stats.json',
           'country_stats.json')  # creates two json files, each containing one of the necessary statistics

sortByCountry(childList)  # sorts every child by continent, country and city

# for child in childList:
#    print(child.name,child.address,child.gifts_wish,child.color)

class Gift:
    def __init__(self, name=None, color=None):
        self.color = color
        self.name = name

    def get_image(self):

        def downloadimages(query):
            response = google_images_download.googleimagesdownload()
            search_queries = []
            # keywords is the search query
            # format is the image file format
            # limit is the number of images to be downloaded
            # print urs is to print the image file url
            # size is the image size which can
            # be specified manually ("large, medium, icon")
            # aspect ratio denotes the height width ratio
            # of images to download. ("tall, square, wide, panoramic")
            arguments = {"keywords": query,
                         "format": "jpg",
                         "limit": 1,
                         "print_urls": True,
                         "aspect_ratio": "panoramic",
                         "no_directory": True,
                         "prefix": query}
            try:
                response.download(arguments)

                # Handling File NotFound Error
            except FileNotFoundError:
                arguments = {"keywords": query,
                             "format": "jpg",
                             "limit": 4,
                             "print_urls": True,
                             "size": "medium"}

            # Providing arguments for the searched query
            try:
                # Downloading the photos based
                # on the given arguments
                response.download(arguments)
            except:
                pass

        def resize_image(an_img):
            basewidth = 450
            img = Image.open(an_img)
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img.save(an_img)

        if len(self.name) != 0:
            for i in self.name:
                downloadimages(i)
                resize_image(os.getcwd() + os.sep + "downloads" + os.sep + i + ".jpg")

            for i in self.name:
                with open("downloads" + os.sep + i + ".jpg", "rb") as f:
                    encoded_string = base64.b64encode(f.read())
                    os.remove(f.name)
                    return encoded_string


gift_list = [] #Breaking news now it only contains one gift

for child in childList: 
    gift_list.append(Gift(child.gifts_wish, child.color))


def compress(images):
    for image in images:
        img = Image.open(image)
        img.save("packedgift" + image, optimize=True,
                 quality=80)  # The quality percentage can be changed. Every picture behaves differently, but we suggest a quality ranging from 30-80


def Encrypt(imagelist):  # not required
    global key

    for image in imagelist:
        pathimg = os.path.abspath(image)

        fin = open(pathimg, 'rb')
        image1 = fin.read()
        fin.close()
        image1 = bytearray(image1)

        key = random.randint(1, 254)
        for index, values in enumerate(image1):
            image1[index] = values ^ key

        fin = open(pathimg, 'wb')
        fin.write(image1)

        fin.close()


def Decrypt(imagelist, key):  # not required

    for image in imagelist:

        pathimg = os.path.abspath(image)

        fin = open(pathimg, 'rb')
        image1 = fin.read()
        fin.close()

        image1 = bytearray(image1)

        for index, values in enumerate(image1):
            image1[index] = key ^ values

        fin = open(pathimg, 'wb')
        fin.write(image1)

        fin.close()


class Delivery:
    # just pack togheter the main memory cores
    def __init__(self, gifts, kids):
        self.gifts = gifts
        self.kids = kids
        self.status = "Status: Delivered"


# instantiate the class

Result = []

for i in range(len(gift_list) - 1):
    Result.append(Delivery(gift_list[i], childList[i]))

# intermediary dictionary for structured operation
FinalDict = {}

# parsed list output
final_list = []

# read the raw kids object from the delivery object
for i in Result:
    FinalDict["name"] = i.kids.name
    FinalDict["address"] = i.kids.address
    FinalDict["gifts"] = i.kids.gifts_wish
    final_list.append(FinalDict)
    FinalDict = {}

# link the input dictionary to the final list

for i in range(len(final_list)):
    final_list[i]["image"] = Result[i].gifts.name
    final_list[i]["color"] = Result[i].gifts.color


# open the output file
g = open('output.txt', 'w')

# just throw the parsed list at it
for i in final_list:
    g.write("Child: {0}, Address: {1}, Gift: {3} {2}\n".format(i["name"], i["address"], i["gifts"], i["color"]))

# cease operation
g.close()'''


print("--- %s seconds ---" % (time.time() - start_time))
# print(gift_list[0].get_image())
