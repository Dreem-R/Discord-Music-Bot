import base64

import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import yt_dlp
import asyncio
from collections import deque
from discord import FFmpegPCMAudio
import google.generativeai as genai
from KeepAlive import keep_alive


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

Gemini_key = os.getenv('Gemini_Key')
genai.configure(api_key=Gemini_key)

SONG_QUEUE = {}
current_mujik = {}
now_playing_messages = {}

ffmpeg_path = "./Bin/ffmpeg-7.0.2-amd64-static/ffmpeg"


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


class Playview(discord.ui.View):

    @discord.ui.button(label="Pause",style=discord.ButtonStyle.secondary)
    async def pause_button(self,interaction: discord.Interaction,button:discord.ui.button):
        await main_pause(interaction=interaction)

    @discord.ui.button(label="Resume",style=discord.ButtonStyle.blurple)
    async def resume_button(self,interaction: discord.Interaction,button:discord.ui.button):
        await main_resume(interaction=interaction)

    @discord.ui.button(label="Skip",style=discord.ButtonStyle.primary)
    async def skip_button(self,interaction: discord.Interaction,button:discord.ui.button):
        await main_skip(interaction)

    @discord.ui.button(label="Stop",style = discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction,buttons:discord.ui.button):
        await main_stop(interaction)
    

async def main_pause(interaction: discord.Interaction):
    if interaction.guild.voice_client and (interaction.guild.voice_client.is_playing()):
        interaction.guild.voice_client.pause()
        await interaction.response.send_message("you paused the music, why bro?", ephemeral=True)

    elif interaction.guild.voice_client:
        await interaction.response.send_message("Mujik is already paused", ephemeral=True)

    else:
        await interaction.response.send_message("No Mujik playing", ephemeral=True)

async def main_skip(interaction: discord.Interaction):
    if interaction.guild.voice_client and (
            interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
        interaction.guild.voice_client.stop()
        await interaction.response.send_message("you skipped the music, why bro?", ephemeral=True)
    else:
        await interaction.response.send_message(f"No Mujik playing", ephemeral=True)

async def main_stop(interaction: discord.Interaction):
    if interaction.guild.voice_client :
        interaction.guild.voice_client.stop()
        await interaction.response.send_message(f"Disconnecting from vc , sorry guys but {interaction.user.mention} ne chup bol diya")
    else:
        await interaction.response.send_message("No Mujik Playing")

async def main_resume(interaction: discord.Interaction):
    if interaction.guild.voice_client and (interaction.guild.voice_client.is_paused()):
        interaction.guild.voice_client.resume()
        await interaction.response.send_message("music is back on baby!!", ephemeral=True)
    elif interaction.guild.voice_client:
        await interaction.response.send_message("Mujik is already playing", ephemeral=True)

    else:
        await interaction.response.send_message("No Mujik in queue", ephemeral=True)

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
    await main_skip(interaction)

@bot.tree.command(name='pause', description='Pause Current Mujik')
async def pause(interaction: discord.Interaction):
    await main_pause(interaction)


@bot.tree.command(name='resume', description='Resume Current Mujik')
async def resume(interaction: discord.Interaction):
    await main_resume(interaction)



@bot.tree.command(name='stop', description='Stop Current Mujik')
async def stop(interaction: discord.Interaction):
    await main_stop(interaction)

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

    YDL_OPTIONS = {
        'format': 'bestaudio/best',  # Prioritize audio streams
        'noplaylist': True,          # Avoid playlists unless specified
        'quiet': False,               # Reduce log verbosity
        'no_warnings': False,       # Suppress warnings
        'default_search': 'ytsearch', # Enable YouTube search
    }

    query = "ytsearch1:" + song_query

    result = await search_ytdlp_async(query, YDL_OPTIONS)
    tracks = result.get("entries", [])

    if not tracks:
        await interaction.followup.send("No songs found.")
        return

    first_track = tracks[0]
    audio_url = first_track.get("url")
    title = first_track.get("title", "Untitled")

    if not audio_url:
        await interaction.followup.send("No audio stream found.")
        return

    guild_id = str(interaction.guild.id)
    if SONG_QUEUE.get(guild_id) is None:
        SONG_QUEUE[guild_id] = deque()

    SONG_QUEUE[guild_id].append((audio_url, title))

    if voice_client.is_playing() or voice_client.is_paused():
        await interaction.followup.send(f"Added To Queue {title}")
    else:
        pview = Playview()

        message = await interaction.followup.send(f"Playing the Mujik --> {title}", view = pview)
        now_playing_messages[guild_id] = message
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

        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10',
            'options': '-vn -bufsize 64k'  # Increase buffer size for stability
        }

        source = FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)  # Remove executable argument

        def after_play(error):
            if error:
                print(f"Error Playing {title}: error: {error}")
            asyncio.run_coroutine_threadsafe(play_next_song(voice_client, guild_id, channel), bot.loop)

        current_mujik[guild_id] = title
        voice_client.play(source, after=after_play)
        message = now_playing_messages.get(guild_id)
        if message:
            await message.edit(content=f"🎶 Playing the Mujik --> **{title}**")
        else:
            # If no previous message found, just send a new one
            message = await channel.send(f"🎶 Playing the Mujik --> **{title}**")
            now_playing_messages[guild_id] = message

    else:
        await voice_client.disconnect()
        SONG_QUEUE[guild_id] = deque()
        now_playing_messages[guild_id] = deque()

@bot.tree.command(name='search', description='Pucho jo Puchna hai')
@app_commands.describe(query='Chatbot')
async def search(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(f"{query}")
    print(response.text)
    if len(response.text) > 2000:
        import io
        file = discord.File(io.StringIO(response.text), filename="response.txt")
        await interaction.followup.send("Response was too long. Here's the file:", file=file)
    else:
        await interaction.followup.send(response.text)

bot.run(TOKEN)
