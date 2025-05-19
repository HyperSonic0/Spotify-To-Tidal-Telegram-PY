import base64
import requests
import re
import uuid

from googlesearch import search
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, InlineQueryHandler

client_id = "wpierdol_tu_client_id"
client_secret = "wpierdol_tu_client_secret"
telegram_token = "wpierdol_tu_telegram_token"

def get_access_token():
    auth = f"{client_id}:{client_secret}"
    auth_bytes = auth.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = { "Authorization": f"Basic {auth_base64}" }
    data = { "grant_type": "client_credentials" }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    access_token = response.json()['access_token']
    return access_token

def get_track_name(access_token, track_id):
    headers = { "Authorization": f"Bearer {access_token}" }
    url = f"https://api.spotify.com/v1/tracks/{track_id}" 

    response = requests.get(url, headers=headers)
    data = response.json()

    return data["name"], data["artists"][0]["name"]

def get_track_id(url):
    match = re.search(r"open\.spotify\.com/track/([a-zA-Z0-9]+)", url)
    if match:
        return match.group(1)
    return None

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    track_id = get_track_id(query)
    access_token = get_access_token()
    artist,name = get_track_name(access_token, track_id)
    track_info = f"{name} - {artist}"
    url = next(search(f"site:tidal.com {track_info}"), None)

    if track_id and access_token and track_info:
        result = InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Get Tidal Link",
            input_message_content=InputTextMessageContent(
                f"🎵 Track name: {track_info}\n🔗 Tidal Link: {url}"
            )
        )

    await update.inline_query.answer([result], cache_time=1)

if __name__ == "__main__":
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(InlineQueryHandler(inline_query_handler))
    app.run_polling()
