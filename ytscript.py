import requests
import json
import time
import os

# set directory to path of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1118295987312672939/mdv4SNLEOK3_mYncLvfrN4I9Qo6uGrB3X3F1VWqRQ36tomaFDN-L3S4OnmaZiXWS_Ji8"

# JSON file to store the last checked video ID for each channel
last_video_file = "last_videos.json"
# Text file containing YouTube channel IDs, one ID per line
channel_file = "channel_ids.txt"


def load_channel_ids():
    try:
        with open(channel_file, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []


def load_last_videos():
    try:
        with open(last_video_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_last_videos(last_video_ids):
    with open(last_video_file, "w") as file:
        json.dump(last_video_ids, file)


def get_latest_video(channel_id):
    # YouTube API endpoint to fetch the latest video from a channel
    api_endpoint = f"https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId={channel_id}&maxResults=1&key=AIzaSyDFx7Xiqqz-G8XkxMvNjJ6iTUtUUaH-Uqk"

    response = requests.get(api_endpoint)
    data = response.json()

    # Extract the video ID from the API response
    video_id = data["items"][0]["id"]["videoId"]
    return video_id


def send_discord_webhook(webhook_url, video_url):
    payload = {"content": video_url}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 204:
        print("Webhook sent successfully")
    else:
        print(f"Failed to send webhook. Status code: {response.status_code}")


# Load the channel IDs from the file
channel_ids = load_channel_ids()

# Load the last video IDs from the file
last_video_ids = load_last_videos()

def search_and_add():
    for channel_id in channel_ids:
        try:
            # Get the latest video ID for the channel
            latest_video_id = get_latest_video(channel_id)

            # Check if there's a new video
            if (
                channel_id not in last_video_ids
                or latest_video_id != last_video_ids[channel_id]
            ):
                last_video_ids[channel_id] = latest_video_id
                # Construct the YouTube video URL
                video_url = f"https://www.youtube.com/watch?v={latest_video_id}"
                # Send the Discord webhook with the video URL
                send_discord_webhook(webhook_url, video_url)
        except Exception as e:
            print(f"An error occurred while checking the channel: {channel_id}")
            send_discord_webhook(webhook_url, "eerror")
            print(str(e))

search_and_add()

# Save the updated last video IDs to the file
save_last_videos(last_video_ids)

os.system('git config --global user.name "Kinshuk Goel"')
os.system('git config --global user.email "103813028+RpM-Kinshuk@users.noreply.github.com"')
os.system('git add last_videos.json')
os.system('git commit -m "Update last_videos.json"')
os.system('git push')