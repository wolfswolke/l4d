import requests


class WebhookHandler:
    def __init__(self):
        self.discord_urls = ""
        self.use_discord = ""

    def setup(self, discord_urls, use_discord):
        self.discord_urls = discord_urls
        self.use_discord = use_discord

    def discord(self, title="MISSING_TITLE", description="MISSING_DESCRIPTION", color=7932020):
        if self.use_discord:
            data = {
                         "content": "",
                         "embeds": [
                             {
                                 "title": f"{title}",
                                 "description": f"{description}",
                                 "color": f"{color}",
                             }
                         ],
                         "attachments": []
                     }
            for url in self.discord_urls:
                requests.post(url, json=data)
        else:
            pass

webhook_handler = WebhookHandler()