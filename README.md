# Discord Bot

A Discord bot to download YouTube videos and audio using the `pytube` and `moviepy` to get the desired part of the video.

## Features

- Download YouTube videos.
- Download YouTube audio.
- Download with Croping.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/discord-bot.git
   cd discord-bot
   ```
2.  required packages:
    ```
    pip install discord.py pytube moviepy python-dotenv
    ```
3. Create a .env file in the project directory and add your Discord bot token:
    ```js
    TOKEN=your-discord-bot-token
    ```
## Commands

```sql 
/ytvideo [YouTube link] [optional: start time] [optional: end time]
```

```sql
/ytmusic [YouTube link]
```

