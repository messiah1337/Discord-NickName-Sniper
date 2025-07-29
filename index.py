import aiohttp
import asyncio

async def get_tokens_and_passwords():
    tokens = []
    passwords = []
    index = 1
    while True:
        token = input(f"Enter Discord token #{index}: ").strip()
        password = input(f"Enter password for token #{index}: ").strip()
        if token and password:
            tokens.append(token)
            passwords.append(password)
        more = input("Do you want to add another token? (y/n): ").strip().lower()
        if more != 'y':
            break
        index += 1
    return tokens, passwords

async def get_usernames():
    usernames = []
    while True:
        username = input("Enter a username to snipe: ").strip()
        if username:
            usernames.append(username)
        more = input("Do you want to add another username? (y/n): ").strip().lower()
        if more != 'y':
            break
    return usernames

async def send_webhook(webhook_url, embed_title, embed_desc, color=0x00ff00):
    data = {
        "content": "@here",
        "embeds": [
            {
                "title": embed_title,
                "description": embed_desc + "\n\n@Made by Messiah",
                "color": color
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(webhook_url, json=data) as res:
                if res.status != 204:
                    print(f"[!] Webhook failed: {res.status} {await res.text()}")
        except Exception as e:
            print(f"[!] Webhook error: {e}")

async def is_token_valid(session, token):
    async with session.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}) as res:
        return res.status == 200

async def is_username_available(session, username):
    url = f"https://discord.com/api/v9/users/{username}"
    async with session.get(url) as res:
        return res.status == 404

async def try_claim_username(session, token, password, new_username, webhook_url):
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "username": new_username,
        "password": password
    }
    async with session.patch(url, headers=headers, json=payload) as res:
        if res.status == 200:
            return True
        elif res.status == 403:
            text = await res.text()
            if "captcha" in text.lower():
                await send_webhook(
                    webhook_url,
                    embed_title="⚠️ CAPTCHA required!",
                    embed_desc=f"Token triggered CAPTCHA while claiming `{new_username}`.\nManual verification needed.",
                    color=0xffa500
                )
            return False
        else:
            return False

async def main():
    tokens, passwords = await get_tokens_and_passwords()
    usernames = await get_usernames()
    webhook = input("Enter your Discord webhook URL: ").strip()

    print(f"\n[+] Starting sniper with {len(tokens)} token(s) and {len(usernames)} username(s)...\n")

    async with aiohttp.ClientSession() as session:
        while True:
            for username in usernames:
                if await is_username_available(session, username):
                    print(f"[!] Username '{username}' is AVAILABLE!")
                    await send_webhook(
                        webhook,
                        embed_title="🎯 Username Sniped!",
                        embed_desc=f"**Nickname 😶‍🌫️:** `{username}`\n**Situation:** `True ✅`",
                        color=0x00ff00
                    )
                    for i in range(len(tokens) -1, -1, -1):
                        token = tokens[i]
                        password = passwords[i]
                        if await is_token_valid(session, token):
                            success = await try_claim_username(session, token, password, username, webhook)
                            if success:
                                print(f"[+] Claimed username '{username}' with token #{i+1}")
                                await send_webhook(
                                    webhook,
                                    embed_title="✅ Claimed!",
                                    embed_desc=f"Successfully claimed `{username}` with Token #{i+1}!",
                                    color=0x00ff00
                                )
                                return
                            else:
                                print(f"[!] Failed to claim username '{username}' with token #{i+1}")
                        else:
                            print("[x] Token is dec.")
                            await send_webhook(
                                webhook,
                                embed_title="✖️ Token is Dec.",
                                embed_desc=f"Token #{i+1} has been deactivated.",
                                color=0xff0000
                            )
                            del tokens[i]
                            del passwords[i]
            await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(main())