import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import Embed
from _pipeline import create_payload, model_req
from search_docs import search_docs
from github_search import search_github_repos, get_github_user

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))  # Optional: greeting channel

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
#bot = commands.Bot(command_prefix='/', intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)


# Ready event
@bot.event
async def on_ready():
    print(f"Curiosity is online! Logged in as {bot.user} (ID: {bot.user.id})")
    if CHANNEL_ID:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(
                "👋 Hello! I'm **Curiosity**, your documentation assistant.\n\n"
                "Use \n`/search <lang> <query>` for docs, \n`/gitsearch <query>` for GitHub repos, " \
                "\n`/ask <question>`! for coding questions \n`/about`for about or \n`/help` for Help \nto get started"
            )

# /search command for official docs
@bot.command(name="search")
async def search_command(ctx, lang: str, *, query: str):
    await ctx.send(f"🔍 Searching **{lang}** docs for: `{query}`...")
    doc_url = search_docs(lang, query)

    if doc_url.startswith("http"):
        embed = Embed(
            title=f"{lang.capitalize()} Docs: {query}",
            description="📖 Click the link below to view the official documentation.",
            url=doc_url,
            color=0x3498db
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(doc_url)

# /gitsearch command for GitHub repos
@bot.command(name="gitsearch")
async def gitsearch_command(ctx, *, query: str):
    await ctx.send(f"🔍 Searching GitHub for: `{query}`...")
    results = search_github_repos(query)

    if not results:
        await ctx.send("❌ No repositories found or GitHub API error.")
        return

    response_lines = ["**Top GitHub Repositories:**\n"]
    for repo in results:
        line = f"🔗 [{repo['name']}]({repo['url']}) — ⭐ {repo['stars']}\n{repo['description']}"
        response_lines.append(line)

    full_response = "\n\n".join(response_lines)

    if len(full_response) > 2000:
        for i in range(0, len(full_response), 2000):
            await ctx.send(full_response[i:i+2000])
    else:
        await ctx.send(full_response)

# /gituser command for GitHub profiles
@bot.command(name="gituser")
async def gituser_command(ctx, username: str):
    await ctx.send(f"🔍 Fetching GitHub user `{username}`...")
    user = get_github_user(username)

    if not user:
        await ctx.send("❌ GitHub user not found.")
        return

    embed = Embed(
        title=f"{user['name']} (@{user['login']})",
        url=user["url"],
        description=user["bio"],
        color=0x24292e
    )
    embed.set_thumbnail(url=user["avatar"])
    embed.add_field(name="🗂️ Public Repos", value=str(user["repos"]))
    embed.add_field(name="👥 Followers", value=str(user["followers"]))
    embed.add_field(name="🧑 Following", value=str(user["following"]))
    await ctx.send(embed=embed)

# /ask command for structured LLM answers
@bot.command(name="ask")
async def ask_command(ctx, *, question: str):
    """LLM-powered Q&A for programming-related questions."""
    await ctx.send("🤖 Thinking...")

    prompt = f"""
You are a helpful programming assistant named **Curiosity**.
You answer user questions{question} about programming by thinking step-by-step like a teacher.
Use your knowledge of languages, frameworks, and coding tools to explain, reason, and provide an example.

If the user's question is off-topic or not programming-related, make a humorous remark and bring them back to coding with enthusiasm.

### Few-Shot Examples (Chain of Thought):

---

**User:** What does `map()` do in Python?

**Curiosity (Steps):**
1. Identify that the question is about Python's built-in `map()` function.
2. Recall that `map()` applies a function to each item in an iterable.
3. Show a working example.

**Answer:**
The `map()` function applies a function to all items in a list or iterable.
```python
nums = [1, 2, 3]
squared = list(map(lambda x: x**2, nums))
print(squared)  # [1, 4, 9] 
so answer the {question} like above"""

    payload = create_payload(
        target="ollama",
        model="llama3.2:latest",
        prompt=prompt,
        temperature=0.3,
        num_ctx=500,
        c=800
    )

    time_taken, response = model_req(payload=payload)

    if response:
        reply = f"**Curiosity says:**\n{response}"
        if time_taken != -1:
            reply += f"\n*Response time: {time_taken:.2f}s*"
    else:
        reply = "❌ I couldn’t get a response from the model."

    MAX_DISCORD_MSG_LEN = 2000
    if len(reply) > MAX_DISCORD_MSG_LEN:
        for i in range(0, len(reply), MAX_DISCORD_MSG_LEN):
            await ctx.send(reply[i:i+MAX_DISCORD_MSG_LEN])
    else:
        await ctx.send(reply)


@bot.command(name="help")
async def help_command(ctx):
    """Show all available commands and what they do."""
    embed = Embed(
        title="📚 Curiosity Bot Help",
        description="Here's what I can help you with:",
        color=0x00b0f4
    )
    embed.add_field(name="/search <lang> <query>", value="🔍 Search official documentation for any language/framework.", inline=False)
    embed.add_field(name="/gitsearch <keywords>", value="🧠 Find top GitHub repositories by topic or keyword.", inline=False)
    embed.add_field(name="/gituser <username>", value="👤 Show GitHub profile summary with bio, repos, and followers.", inline=False)
    embed.add_field(name="/ask <question>", value="💬 Ask me anything about code, tools, or concepts. I’ll fetch and explain it.", inline=False)
    embed.add_field(name="freeform (no slash)", value="📝 Just say something like `how do I use zip in Python?` — and I’ll respond.", inline=False)
    embed.add_field(name="/India 🎉", value="🎈 A little fun easter egg!", inline=False)
    embed.set_footer(text="I'm Curiosity — here to help you code smarter, faster, and better!")

    await ctx.send(embed=embed)


@bot.command(name="about")
async def about_command(ctx):
    """Show bot author and purpose."""
    embed = Embed(
        title="🤖 About Curiosity",
        description="I'm Curiosity — your AI documentation and coding assistant.",
        color=0x7289DA
    )
    embed.add_field(
        name="What I do",
        value=(
            "- Find official docs for languages & frameworks\n"
            "- Help with GitHub repo & user info\n"
            "- Answer technical questions using LLMs\n"
            "- Make coding smoother right from Discord"
        ),
        inline=False
    )
    embed.add_field(
        name="Created by",
        value="✨ **Maahir** with a little help from GPT 🚀",
        inline=False
    )
    embed.set_footer(text="Built using Python, Discord.py, and Generative AI magic.")
    await ctx.send(embed=embed)




# Fallback: general LLM-powered response
@bot.event
async def on_message(message):
    await bot.process_commands(message)  # Always allow slash commands first

    if message.author == bot.user:
        return  # Ignore own bot messages

    text = message.content.strip()



    # --- Quick checks to ignore ---
    if text.startswith("/") or len(text) < 5:
        return  # Ignore slash commands and very short messages
    
    if text.lower().startswith("india"):
        try:
            await message.channel.send(f"I love my country.\n India will stand strong.\n hand crafted with love by M\n")
        except StopIteration:
            await message.channel.send(" No results found for your query.")
        return

    # --- Heuristic: Only trigger LLM if question-like ---
    if not any(keyword in text.lower() for keyword in ["how", "what", "why", "explain", "example", "difference", "usage", "when", "where", "error", "bug", "debug", "issue"]):
        return  # Skip if message doesn't look like a coding question

    await message.channel.typing()

    # --- If it looks like a question, call LLM ---
    prompt = f"""
You are Curiosity — a friendly and knowledgeable AI programming assistant on Discord.

The user said: "{text}"

**Your job is to:**
- Clearly understand the user's intent.
- Assume they are asking a programming-related question unless it's clearly nonsense.
- Directly answer their question with a short explanation, and if possible a small code example.
- Be concise, focused, and helpful.

If the user's message is off-topic and clearly NOT about programming (e.g., "Do you like pizza?"), make a witty joke **but quickly bring them back to coding topics.**

Answer the user's question now:
"""

    payload = create_payload(
        target="ollama",
        model="llama3.2:latest",
        prompt=prompt,
        temperature=0.3,
        num_ctx=500,
        c=1000
    )

    time_taken, response = model_req(payload=payload)

    if response:
        reply = f"**Curiosity says:**\n{response}"
        if time_taken != -1:
            reply += f"\n*Response time: {time_taken:.2f}s*"
    else:
        reply = "❌ I couldn’t get a response from the model."

    MAX_DISCORD_MSG_LEN = 2000
    if len(reply) > MAX_DISCORD_MSG_LEN:
        for i in range(0, len(reply), MAX_DISCORD_MSG_LEN):
            await message.channel.send(reply[i:i+MAX_DISCORD_MSG_LEN])
    else:
        await message.channel.send(reply)

# Run the bot
bot.run(DISCORD_TOKEN)
