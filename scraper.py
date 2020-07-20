#Danbooru scraper by Mr. Funny
#This is following some example code but that code was broken
#So I figured I would take it and fix it
#Feel free to put this on r/badcode

from __future__ import unicode_literals #what?
from pybooru import Danbooru
from random import randint
import urllib.request
import os
import random

def collect(tags, pages):
    try:
        #authentication
        client = Danbooru('danbooru', username="cum_chalice", api_key="12d62QBEC2XbxnEoEV6iRu1G")
        
        #Global variables to make the download function happy
        global fileurl
        global posts
        
        #getting max page, tags, and creating output.txt
        randompage = int(input("What are the maximum amount of pages? "))
        chosenpage = random.choice(range(0, randompage)) #chooses a random page between 1 and the specified max page, prevents empty files
        posts = client.post_list(tags=tags, page=chosenpage, limit=200) #seems to be a hardcoded limit of 200, documentation says 100?

        output = open("output.txt", "a+") #creates output.txt if it doesn't exist, appends to output.txt if it does exist
        output.write("From page " + str(chosenpage) + " with tag(s) " + tags + ": \n") #writes page number and tag(s) before links

        #getting links... i think?
        for post in posts:
            try:
                fileurl = post['file_url']
            except:
                fileurl = post['source']
            #writing links
            output.write(fileurl + "\n") #outputs URLs to output.txt
        print("Done! Written links to output.txt... hopefully")
    except Exception as err:
        print(err)
        raise err #doesn't really do shit honestly unless something goes catastrophically wrong

def download():
    try:
        os.mkdir("images") #Created directory called images, downloaded images get stored here
    except OSError: #Not sure if this works on Windows
        print("Creating images directory failed or directory already exists.")
    else:
        print("Successfully created images directory")
        
    print("Now downloading the images. This may take a few minutes...")
    
    for post in posts: #Downloading the images AAAAAAAA THIS WAS PAINFUL
        try:
            randnumber = randint(1, 9999999999) #Gets a random filename with random numbers, low chance of duplicate file names, but not zero
            urllib.request.urlretrieve(post['file_url'], "images/{0}.jpg".format(randnumber)) #Downloads the image from the url, placing them in the images directory
        except Exception as err: #Prints error to console and continues downloading
            print(err)
            continue

def main():
    tags = input("What tag(s) do you want? ") #can only input 2 tags at a time due to standard account (you can put in your own account/api key if you have an upgraded account)
    collect(tags=tags + " rating:s", pages=1000) #rating:s gets only SFW posts, remove rating:s to also get NSFW
    download()

main()