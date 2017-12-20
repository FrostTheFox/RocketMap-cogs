import discord
import requests
import logging
from discord.ext import commands


class checkproxy:
    """Cog for proxy checking"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def checkproxy(self, ctx, proxy):
        """Checks the provided proxy."""

        p = proxy
        pr = {
                    'http': p,
                    'https': p
                }
        try:
            r = requests.get('https://pgorelease.nianticlabs.com/plfe/version',
                             proxies=pr,
                             timeout=5,
                             headers={'Host': 'pgorelease.nianticlabs.com',
                                      'Connection': 'close',
                                      'Accept': '*/*',
                                      'User-Agent': 'pokemongo/0 CFNetwork/893.14.2 Darwin/17.3.0',
                                      'Accept-Language': 'en-us',
                                      'Accept-Encoding': 'br, gzip, deflate',
                                      'X-Unity-Version': '2017.1.2f1'})
            if r.status_code == 200:
                nstatus = ':white_check_mark: 200 OK, proxy is not banned.'
            if r.status_code == 403:
                nstatus = ':x: 403 Forbidden, proxy is banned.'
        except requests.exceptions.Timeout:
            nstatus = ':x: Timed out after 5 seconds.'
        except requests.exceptions.RequestException as e:
            nstatus = 'Unable to connect to the proxy, or timed out. Make sure to add https://, and the port.'
            logging.error('requestsexception: ' + str(e))

        try:
            r = requests.get('https://sso.pokemon.com/sso/login?service=https%3A%2F%2Fsso.pokemon.com%2Fsso%2Foauth2.0%2FcallbackAuthorize&locale=en_US',
                             proxies=pr,
                             timeout=5,
                             headers={'Host': 'sso.pokemon.com',
                                      'Connection': 'close',
                                      'Accept': '*/*',
                                      'User-Agent': 'pokemongo/0 CFNetwork/893.14.2 Darwin/17.3.0',
                                      'Accept-Language': 'en-us',
                                      'Accept-Encoding': 'br, gzip, deflate',
                                      'X-Unity-Version': '2017.1.2f1'})
            if r.status_code == 200:
                pstatus = ':white_check_mark: 200 OK, proxy is not banned.'
            if r.status_code == 409:
                pstatus = ':x: 409 Conflict, proxy is banned.'
        except requests.exceptions.Timeout:
            pstatus = ':x: Timed out after 5 seconds.'
        except requests.exceptions.RequestException as e:
            pstatus = 'Unable to connect to the proxy, or timed out. Make sure to add https://, and the port.'
            logging.error('requestsexception: ' + str(e))

        await self.bot.say("""Niantic: """ + nstatus + """
PTC: """ + pstatus)

        if not ctx.message.channel.is_private:
            await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(checkproxy(bot))
