import base64

import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import yt_dlp
import asyncio
from collections import deque

from KeepAlive import keep_alive


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

SONG_QUEUE = {}
current_mujik = {}

encoded = os.getenv("COOKIES_BASE64")
if encoded:
    decoded = base64.b64decode(encoded).decode()
    with open("cookies.txt", "w", encoding="utf-8") as f:
        f.write(decoded)

ffmpeg_path = './Bin/ffmpeg/ffmpeg'


keep_alive()

# {current_mujik.get(interaction.guild.id,"No Track Info")}

async def search_ytdlp_async(query, ydl_options):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_options))


def _extract(query, ydl_options):
    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        return ydl.extract_info(query, download=False)


intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='!', intents=intent)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is ready")


@bot.event
async def on_message(msg):
    if msg.author.id != bot.user.id:
        await msg.channel.send(f"Sahi baat kar rahe ho! , {msg.author.mention}")


@bot.tree.command(name="greet", description="Send greeting to another user")
async def greet(interaction: discord.Interaction):
    await interaction.response.defer()
    username = interaction.user.mention
    await interaction.followup.send(f"Hello there, {username}")


@bot.tree.command(name='skip', description='Skip Current Mujik')
async def skip(interaction: discord.Interaction):
    if interaction.guild.voice_client and (
            interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
        interaction.guild.voice_client.stop()
        await interaction.response.send_message(f"Skipping Mujik")
    else:
        await interaction.response.send_message(f"No Mujik playing")


@bot.tree.command(name='pause', description='Pause Current Mujik')
async def pause(interaction: discord.Interaction):
    if interaction.guild.voice_client and (interaction.guild.voice_client.is_playing()):
        interaction.guild.voice_client.pause()
        await interaction.response.send_message(f"Pausing Mujik")

    elif interaction.guild.voice_client:
        await interaction.response.send_message("Mujik is already paused")

    else:
        await interaction.response.send_message("No Mujik playing")


@bot.tree.command(name='resume', description='Resume Current Mujik')
async def resume(interaction: discord.Interaction):
    if interaction.guild.voice_client and (interaction.guild.voice_client.is_paused()):
        interaction.guild.voice_client.resume()
        await interaction.response.send_message(f"Playing Mujik")

    elif interaction.guild.voice_client:
        await interaction.response.send_message("Mujik is already playing")

    else:
        await interaction.response.send_message("No Mujik in queue")


@bot.tree.command(name='stop', description='Stop Current Mujik')
async def stop(interaction: discord.Interaction):
    if interaction.guild.voice_client :
        interaction.guild.voice_client.stop()
        await interaction.response.send_message(f"Disconnecting from vc , sorry guys but {interaction.user.mention} ne chup bol diya")
    else:
        await interaction.response.send_message("No Mujik Playing")

@bot.tree.command(name="mujik", description="Music Bajane ke liye")
@app_commands.describe(song_query="Search query")
async def mujik(interaction: discord.Interaction, song_query: str):
    await interaction.response.defer()

    if interaction.user.voice is None or interaction.user.voice.channel is None:
        await interaction.followup.send("You need to be in a voice channel to use this command.")
        return

    voice_channel = interaction.user.voice.channel

    voice_client = interaction.guild.voice_client
    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_client != voice_channel:
        await voice_client.move_to(voice_channel)

    ydl_options = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'cookiefile': 'cookies.txt',
        'youtube_include_dash_manifest': False,
    }

    query = "ytsearch1:" + song_query

    result = await search_ytdlp_async(query, ydl_options)
    tracks = result.get("entries", [])

    if tracks is None:
        await interaction.followup.send("No songs found")
        return

    first_track = tracks[0]
    formats = first_track.get("formats", [])
    audio_url = None

    # Find the best audio-only URL manually
    for f in formats:
        if f.get("acodec") != "none" and f.get("vcodec") == "none":
            if "audio_url" not in locals():
                audio_url = f["url"]

    if not audio_url:
        await interaction.followup.send("No audio stream found.")
        return

    title = first_track.get("title", "Untitled")

    guild_id = str(interaction.guild.id)
    if SONG_QUEUE.get(guild_id) is None:
        SONG_QUEUE[guild_id] = deque()

    SONG_QUEUE[guild_id].append((audio_url, title))

    if voice_client.is_playing() or voice_client.is_paused():
        await interaction.followup.send(f"Added To Queue {title}")
    else:
        await interaction.followup.send(f"Playing the Mujik --> {title}")
        await play_next_song(voice_client, guild_id, interaction.channel)

    #this is the music playing part
    # ffmpeg_options = {
    #     "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    #     "options": "-vn -c:a libopus -b:a 96k",
    # }
    #
    # source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_options)
    # voice_client.play(source)


async def play_next_song(voice_client, guild_id, channel):
    if SONG_QUEUE[guild_id]:
        audio_url, title = SONG_QUEUE[guild_id].popleft()

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn"
        }

        # Instead of FFmpegPCMAudio
        source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_options, executable=ffmpeg_path)

        def after_play(error):
            if error:
                print(f"Error Playing {title}: error: {error}")
            asyncio.run_coroutine_threadsafe(play_next_song(voice_client, guild_id, channel), bot.loop)

        current_mujik[guild_id] = title
        voice_client.play(source, after=after_play)
        await asyncio.create_task(channel.send(f"{title} is playing"))

    else:
        await voice_client.disconnect()
        SONG_QUEUE[guild_id] = deque()


bot.run(TOKEN)
