import requests
import json
import time

# List of YouTube channel IDs
channel_ids = ["UCMOgdURr7d8pOVlc-alkfRg"]

# Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1118295987312672939/mdv4SNLEOK3_mYncLvfrN4I9Qo6uGrB3X3F1VWqRQ36tomaFDN-L3S4OnmaZiXWS_Ji8"

# Dictionary to store the last checked video ID for each channel
last_video_ids = {}

def get_latest_video(channel_id):
    # YouTube API endpoint to fetch the latest video from a channel
    api_endpoint = f"https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId={channel_id}&maxResults=1&key=AIzaSyDFx7Xiqqz-G8XkxMvNjJ6iTUtUUaH-Uqk"

    response = requests.get(api_endpoint)
    data = response.json()

    # Extract the video ID from the API response
    video_id = data["items"][0]["id"]["videoId"]
    return video_id

def send_discord_webhook(webhook_url, video_url):
    payload = {
        "content": video_url
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 204:
        print("Webhook sent successfully")
    else:
        print(f"Failed to send webhook. Status code: {response.status_code}")

while True:
    for channel_id in channel_ids:
        try:
            # Get the latest video ID for the channel
            latest_video_id = get_latest_video(channel_id)
            
            # Check if there's a new video
            if channel_id not in last_video_ids or latest_video_id != last_video_ids[channel_id]:
                last_video_ids[channel_id] = latest_video_id

                # Construct the YouTube video URL
                video_url = f"https://www.youtube.com/watch?v={latest_video_id}"

                # Send the Discord webhook with the video URL
                send_discord_webhook(webhook_url, video_url)

        except Exception as e:
            print(f"An error occurred while checking the channel: {channel_id}")
            print(str(e))

    # Sleep for 1 minute before checking again
    time.sleep(60)
