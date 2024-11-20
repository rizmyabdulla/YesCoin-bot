
# YESCOIN BOT

[<img src="https://img.shields.io/badge/Telegram-%40Me-orange">](https://t.me/NotMrStrange)
[<img src="https://img.shields.io/badge/Telegram-Group-green">](https://t.me/Yk_daemon)
[<img src="https://img.shields.io/badge/Telegram-Announcement-green">](https://t.me/Ykdaemon)

> [!WARNING]
> ⚠️ I do my best to avoid detection of bots, but using bots is forbidden in all airdrops. i cannot guarantee that you will not be detected as a bot. Use at your own risk. I am not responsible for any consequences of using this software.

# 🔥🔥 MUST USE PYTHON 3.10 🔥🔥

## Features  
| Feature                                                     | Supported  |
|-------------------------------------------------------------|:----------:|
| Concurrent session handling with async                      |     ✅     |
| Proxy binding to session                                     |     ✅     |
| Auto check-in                                                |     ✅     |
| Auto complete daily missions                                               |     ✅     |
| Auto complete tasks                                          |     ✅     |
| Auto upgrade boosters                                |     ✅     |
| Auto Collect coins                                |     ✅     |
| Auto claim YESPACK                                |     ✅     |
| Auto use Daily Boosters                                |     ✅     |

## Settings
| Settings | Description |
|----------------------------|:-------------------------------------------------------------------------------------------------------------:|
| **API_ID / API_HASH**      | Platform data from which to run the Telegram session (default - android)                                      |       
| **REF_LINK**               | Put your ref link here (default: my ref link)                                                                 | 
| **AUTO_TASK**              | Whether to complete tasks automatically (True / False)                                                        |
| **AUTO_UPGRADE_LEVEL**     | Whether to upgrade boosters automatically (True / False)                                                      |
| **MAX_UPGRADE_LEVEL**      | Maximum level to upgrade boosters (default: 10)(Max level: 15)                                                |
| **DELAY_EACH_ACCOUNT**     | Delay between each account in seconds                                                                         |
| **USE_PROXY_FROM_FILE**    | Whether to use a proxy from the bot/config/proxies.txt file (True / False)                                    |



**Obtaining API Keys**
1. Go to [my.telegram.org](https://my.telegram.org) and log in with your phone number.
2. Select "API development tools" and register a new application.
3. Copy the **API_ID** and **API_HASH** to the `.env` file.


**Installation**

**Windows**

1. Download the script zip file and unzip it.

**Quick Start**
To install libraries and run the bot, open `run.bat` on Windows.

2. Open the folder in the terminal:
   ```shell
   cd YesCoin-bot
   ```
3. To install automatically, run:
   ```shell
   run.bat
   ```

**Manual Installation on Windows**

```shell
git clone https://github.com/rizmyabdulla/YesCoin-bot.git
cd YesCoin-bot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Add your API_ID and API_HASH in the .env file
python main.py
```

---

**Termux**

1. Download the script zip file and unzip it.
2. Open the folder in Termux:
   ```shell
   cd $HOME
   ```

**Manual Installation on Termux**

```shell
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/rizmyabdulla/YesCoin-bot.git
cd YesCoin-bot
pip install -r requirements.txt
cp .env-example .env
nano .env
# Add your API_ID and API_HASH in the .env file
python main.py
```

## Support
- Star the repo if you like the project ⭐
- Fork the repo if you want to contribute 🍴
- Open an issue if you have suggestions or found a bug 🐛
- PRs are welcome 🎉