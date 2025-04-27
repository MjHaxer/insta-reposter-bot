# auto_reposter.py

from instagrapi import Client
import schedule
import time

USERNAME = "your_username"       # Apna Instagram username
PASSWORD = "your_password"       # Apna Instagram password
TARGET_USERNAME = "target_account_username"   # Jis account se repost karna hai

cl = Client()

def login():
    cl.login(USERNAME, PASSWORD)
    print("Login successful!")

def repost_latest_post():
    try:
        user_id = cl.user_id_from_username(TARGET_USERNAME)
        media = cl.user_medias(user_id, 1)[0]
        
        media_id = media.pk
        media_type = media.media_type
        
        if media_type == 1:
            # Photo
            photo_url = media.thumbnail_url
            photo_bytes = cl.photo_download_by_url(photo_url)
            cl.photo_upload(photo_bytes, caption=media.caption_text)
            print("Photo reposted!")
        elif media_type == 2:
            # Video/Reel
            video_url = media.video_url
            video_bytes = cl.video_download_by_url(video_url)
            cl.video_upload(video_bytes, caption=media.caption_text)
            print("Video/Reel reposted!")
        else:
            print("Unknown media type, skipping.")
    except Exception as e:
        print(f"Error: {e}")

def job():
    login()
    repost_latest_post()

# Har 30 minutes mein check karega (chaaho to 5 min bhi kar sakte ho)
schedule.every(30).minutes.do(job)

print("Bot is running...")

while True:
    schedule.run_pending()
    time.sleep(5)
