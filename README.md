# Lua Deobfuscator Discord Bot

A production-ready Discord bot for statically analyzing and deobfuscating Lua/Luau scripts safely.

## Deployment via Render

1. Create a GitHub repository and push this source code. (Ensure `DISCORD_TOKEN` is NOT in the code).
2. Create a new **Background Worker** on Render.
3. Connect your GitHub repository.
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `python bot.py`
6. Go to the Render Environment tab and add the `DISCORD_TOKEN` variable with your bot token.
7. Deploy. Ensure your bot has the Message Content Intent enabled in the Discord Developer Portal.
 
