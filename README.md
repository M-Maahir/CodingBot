# Curiosity Discord Bot

> **Curiosity** is a playful, AI-powered documentation and programming assistant designed for Discord!
>
> Search documentation, ask coding questions, explore GitHub repositories — all without leaving your server.

---

## Features

* 🔎 `/search <language> <query>` — Search **official documentation** for programming languages and frameworks.
* 🧐 `/ask <question>` — Ask  **programming questions** , get  **LLM** -powered, step-by-step explanations with examples.
* 📚 `/gitsearch <keywords>` — Find **top GitHub repositories** based on keywords.
* 👤 `/gituser <username>` — View a **GitHub user's** profile: bio, repos, followers, and more.
* 🎉 Easter eggs and friendly, witty responses if you're off-topic.
* 🛠️ Built with  **Python** ,  **Discord.py** , **Ollama/Open-WebUI** models, and **Docker** support for easy deployment.

---

## Project Structure

![1745699466673](image/README/1745699466673.png)

| File                   | Purpose                                                                                                 |
| :--------------------- | :------------------------------------------------------------------------------------------------------ |
| `main.py`            | Main bot logic. Handles all commands and message responses.                                             |
| `_pipeline.py`       | Interface to interact with LLM servers (Ollama / Open-WebUI). Builds payloads and sends model requests. |
| `search_docs.py`     | Quick search tool to find official documentation links.                                                 |
| `github_search.py`   | GitHub API integration to search repositories and user profiles.                                        |
| `.env`               | Stores sensitive credentials (Discord Token, API Keys, Server URL).                                     |
| `docker-compose.yml` | Defines Docker services for bot deployment.                                                             |
| `Dockerfile`         | Builds the Curiosity bot container.                                                                     |

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/curiosity-discord-bot.git
cd curiosity-discord-bot
```

---

### 2. Environment Variables

Create a `.env` file in the root directory with the following (already provided):

```env
DISCORD_TOKEN=your_discord_token
CHANNEL_ID=your_channel_id
SERVER_TYPE=open-webui_or_ollama
SERVER_URL=http://your_model_server_url
SERVER_API_KEY=your_model_server_api_key
GITHUB_TOKEN=your_github_token (optional but recommended)
```

* `DISCORD_TOKEN`: Your Discord bot token.
* `SERVER_TYPE`: Either `open-webui` or `ollama` depending on your LLM backend.
* `SERVER_URL`: Your model API endpoint.
* `SERVER_API_KEY`: API key for secured model requests.
* `GITHUB_TOKEN`: (Optional) Needed for higher GitHub API rate limits.

---

### 3. Running Locally

#### Without Docker

```bash
pip install -r requirements.txt
python main.py
```

Make sure you have:

* Python 3.10+
* `discord.py`, `requests`, `python-dotenv`

#### With Docker

If you prefer containerized deployment:

```bash
docker-compose up --build
```

 Automatically loads `.env`, builds the container, and connects to your LLM backend.

---

## Bot Commands

| Command                        | Description                                                                   |
| :----------------------------- | :---------------------------------------------------------------------------- |
| `/search <language> <query>` | Search official documentation (Python, JavaScript, etc.).                     |
| `/ask <question>`            | Ask any programming-related question. Bot uses an LLM to answer thoughtfully. |
| `/gitsearch <keywords>`      | Search for top GitHub repositories related to a topic.                        |
| `/gituser <username>`        | Fetch GitHub user information.                                                |
| `/about`                     | Learn about Curiosity's mission and creator.                                  |
| `/help`                      | View a list of all available commands.                                        |

---

## LLM Backend (Model Server)

Curiosity can interact with:

* [Ollama](https://ollama.ai/)
* [Open-WebUI](https://github.com/open-webui/open-webui)

The payloads adapt dynamically based on the `SERVER_TYPE` setting.

Supported Models:

* Any `Llama3`, `Mixtral`, `Mistral`, `Command-R`, or compatible LLMs available at your model server.

---

## Fun Behavior

* If a user types something unrelated to coding, Curiosity will **make a witty joke** and cleverly redirect them back to programming topics.
* Easter Egg: Typing `India` returns a personalized, patriotic message!

---

## Deployment Tips

* To change the LLM server address or model, just modify `.env`.
* Adjust the model payload (e.g., `temperature`, `context_length`) directly inside `main.py` if needed.
* Use `restart: unless-stopped` inside Docker for reliable uptime.
* Update your Discord bot's **intent settings** to enable `MESSAGE CONTENT INTENT` under Developer Portal > Bot Settings.

---

## Credits

* **Developed by** : Maahir (with a little magic from GPT)
* **Built at** : Generative Intelligence Lab, FAU
* **Technologies** : Python, Discord.py, Ollama / Open-WebUI, Docker, GitHub API.

---

## Screenshots

* `/search python zip`
* `/ask "What is polymorphism?"`
* `/gitsearch machine learning`

![1745701170788](image/README/1745701170788.png)![1745701201670](image/README/1745701201670.png)

![1745701216802](image/README/1745701216802.png)

![1745701231328](image/README/1745701231328.png)

![1745701242303](image/README/1745701242303.png)

![1745701253985](image/README/1745701253985.png)

![1745701271489](image/README/1745701271489.png)

# About:

Group name: Interstellar 

Bot name: Curiosity

Group members: Maahir Mitayeegiri, Rakesh Shatamoni and Manikanth Nampally
