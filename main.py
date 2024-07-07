import discord
from discord.ext import commands
from pytube import YouTube
from pytube.helpers import safe_filename
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import AudioFileClip
import os 

from dotenv import load_dotenv
load_dotenv()




client = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@client.event
async def on_ready():
    print("bot ready")
    await client.change_presence(status=discord.Status.idle)
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    



def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"Removed file: {path}")
    else:
        print(f"File does not exist: {path}")


def get_video_title(link):
    video = YouTube(link)
    return video.title



def audio_download(link):
    video = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    video_stream = video.streams.filter(only_audio=True).first()
    file_name = f"{safe_filename(video.title)}.mp4"  
    
    file_path = os.path.join('.\\downloads', file_name)
    video_stream.download(output_path='.\\downloads', filename=file_name)

    audio_path = file_path.replace('.mp4', '.mp3')
    audio_clip = AudioFileClip(file_path)
    audio_clip.write_audiofile(audio_path)
    audio_clip.close()
    file_path = audio_path
    file_size = round((os.path.getsize(file_path) / (1024 * 1024)), 2)
    
    return file_path, file_size





def video_download(link):
    video = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    video_stream = video.streams.get_lowest_resolution()

    safe_title = safe_filename(video_stream.title)
    file_path = os.path.join('.\\downloads', f"{safe_title}.mp4")

    video_stream.download(output_path='.\\downloads', filename=f"{safe_title}.mp4")

    file_size = round((os.path.getsize(file_path)/ (1024 * 1024)),2)
    return file_path,file_size





@client.tree.command(name="ytmusic",description = "Youtube music download")
async def music(interaction: discord.Integration,link:str):
    try:
        await interaction.response.send_message(f"Downloading... ")
        file_path,file_size = audio_download(link)
        try:
            await interaction.followup.send(file=discord.File(file_path))
        except:
            await interaction.followup.send(f"Can't send that audio, **`{file_size} MB`**")
        
    except Exception as e:
        await interaction.response.send_message("Couldn't find that link.")


  
@client.tree.command(name="ytvideo",description = "Youtube video download")
async def video(interaction: discord.Integration,link:str,initial:str = None, final:str = None):
    if initial == None and final == None:
        await interaction.response.send_message(f"Downloading... \n**{get_video_title(link)}**")
        file_path,file_size = video_download(link)
        try:
            await interaction.followup.send(file=discord.File(file_path))
        except:
            await interaction.followup.send(f"Cant send that video, **`{file_size} MB`**")
    else:
        title = get_video_title(link)
        await interaction.response.send_message(f"Downloading...\n**{title}**\n***Croping*** **`{initial}`**-**`{final}`**")
        
        file_path,file_size = video_download(link)

        start_time_str = initial
        end_time_str = final
        start_time_min, start_time_sec = map(int, start_time_str.split(":"))
        end_time_min, end_time_sec = map(int, end_time_str.split(":"))
        start_time = start_time_min * 60 + start_time_sec
        end_time = end_time_min * 60 + end_time_sec

        video = VideoFileClip(file_path)
        cropped_video = video.subclip(start_time, end_time)
        cropped_video_file_path = f"{title}-cropped.mp4"
        cropped_video.write_videofile(cropped_video_file_path)
        video.close()
        cropped_video.close()

        size = round((os.path.getsize(cropped_video_file_path) / (1024 * 1024)), 2)

        try:
            await interaction.followup.send(file=discord.File(cropped_video_file_path))
        except:
            await interaction.followup.send(f"Can't send that video, **`{size} MB`**")
            
  



@client.command()
async def ping(ctx):
    await ctx.send('`latency: {0}`'.format(round(client.latency, 1)))




@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user:
        return
    
    




client.run(os.getenv('TOKEN'))



