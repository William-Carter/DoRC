# Requirements:
- praw
- requests

<br />
<br/>

# Credentials
Go to https://www.reddit.com/prefs/apps and create a new app for use with this program. 

You're making a **script**, so select that option.

You'll need to set the Redirect URI to something even though it's pointless for scripts, http://localhost:8080 is a good option.

Once you've done that, you'll have both the client ID

![Client ID](/images/clientID.png)

And the client secret

![Client Secret](/images/clientSecret.png)

You can then insert both of these into the credentials.json file in their respective spots.

You'll also need to put your reddit username and password in. Reddit requires that you log in as an account to use their API.

If for whatever reason you don't have the credentials.json file, the format is as follows:
```json
{
    "client_id":"",
    "client_secret":"",
    "username":"",
    "password":""
}

```
Once your credentials.json file is complete, you can pass it into the program.

<br />
<br/>

# Usage
The program has four arguments:

    -x     Your credential file

    -s     The name of the subreddit your collection belongs to

    -c     The ID of your collection

    -d     A custom directory to download the images to (Can be left blank)

```
python downloadCollection.py -x yourCredentialsFileHere.json -s subredditName -c collectionID -d C:\Path\To\Download\To\
```

You can find the ID of a collection in the URL
![Collection URL](/images/collectionID.png)

<br/>

Working example:
```
python downloadCollection.py -x credentials.json -s pengu -c a5b7f72e-cf19-4745-8e6b-983a06feff74 -d %USERPROFILE%/Downloads/
```
Saves the collection to the user's download folder.
