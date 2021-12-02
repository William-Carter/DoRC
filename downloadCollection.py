from logging import exception
from re import sub
import praw
import time
import prawcore
import requests
import argparse
import os
import json
dirPath = os.path.dirname(os.path.realpath(__file__))

def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-x", required=True, help="Your credentials file. See the readme for help on formatting it correctly.")
    argParser.add_argument("-s", required=True, help="The subreddit your collection belongs to.")
    argParser.add_argument("-c", required=True, help="The ID of your collection. This is the end part of the URL (Without the slashes).")
    argParser.add_argument("-d", help="The directory to download files to. Will be downloaded in the same folder as the script by default.")
    args = argParser.parse_args()

    if not os.path.isfile(args.x):
        raise Exception("Credential file does not exist!")

    

    if not os.path.isdir(args.d):
        raise Exception("Invalid Directory")


    with open(args.x, "r") as credentialsFile:
        credentials = json.load(credentialsFile)

    if not (("password" in credentials) and ("username" in credentials) and ("client_id" in credentials) and ("client_secret" in credentials)):
        raise Exception("Credential file is incomplete!")

    downloadCollection(credentials["client_id"], credentials["client_secret"], credentials["username"], credentials["password"], args.s, args.c, args.d)
    

def downloadCollection(clientID, clientSecret, username, password, subreddit, collectionID, dlDirectory=""):
    reddit = praw.Reddit(
    client_id=clientID,
    client_secret=clientSecret,
    password=password,
    user_agent="Collection Downloader",
    username=username
    )

    try:
        print("Logged in as", reddit.user.me())
    except prawcore.exceptions.OAuthException:
        raise Exception("Invalid Login!")

    collection = reddit.subreddit(subreddit).collections(collectionID)
    try:
        collection.title
    except:
        raise Exception("Collection and/or subreddit is incorrect")


    if not dlDirectory:
        directory = dirPath+"/"+subreddit+"_"+collection.title+"/"
    else:
        directory = dlDirectory+"/"+subreddit+"_"+collection.title+"/"
    
    if not os.path.isdir(directory):
        os.makedirs(directory)

    for link in collection.sorted_links:
        print(list(collection.sorted_links).index(link)+1, "of", len(collection.sorted_links))
        timeAtStartOfRequest = time.time()
        print("Requesting", link)
        submission = reddit.submission(id=link)
        response = requests.get(submission.url)


        filename = directory+str(link)+".jpg"
        print("Writing to", filename)
        with open(filename, "wb") as f:
            f.write(response.content)
        print("Downloaded", os.path.getsize(filename), "bytes of data")
        
        # Prevent the 60 request per minute limit from being exceededs
        limiter = max(1-(time.time()-timeAtStartOfRequest), 0)
        print("Waiting for", round(limiter, 2), "seconds\n\n")
        time.sleep(limiter)

    print("Collection Finished Downloading")


if __name__ == "__main__":
    main()