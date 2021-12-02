import praw
import time
import requests
import argparse
import os
import json

def main():
    dirPath = os.path.dirname(os.path.realpath(__file__))
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-x", required=True, help="Your credentials file. See the readme for help on formatting it correctly.")
    argParser.add_argument("-s", required=True, help="The subreddit your collection belongs to.")
    argParser.add_argument("-c", required=True, help="The ID of your collection. This is the end part of the URL (Without the slashes).")
    argParser.add_argument("-d", help="The directory to download files to. Will be downloaded in the same folder as the script by default.")
    args = argParser.parse_args()
    
    with open(args.x, "r") as credentialsFile:
        credentials = json.load(credentialsFile)


    reddit = praw.Reddit(
    client_id=credentials["client_id"],
    client_secret=credentials["client_secret"],
    password=credentials["password"],
    user_agent="Collection Downloader",
    username=credentials["username"]
    )


    print("Logged in as", reddit.user.me())


    collection = reddit.subreddit(args.s).collections(args.c)

    if not args.d:
        directory = dirPath+"/"+args.s+"_"+collection.title+"/"
    else:
        directory = args.d+"/"+args.s+"_"+collection.title+"/"
    
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
        print("Waiting for", limiter, "seconds\n\n")
        time.sleep(limiter)

    print("Collection Finished Downloading")


if __name__ == "__main__":
    main()