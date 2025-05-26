import discord
from discord.ext import commands
import random
from keep_alive import keep_alive
import csv
import asyncio
from bot_token import token
import datetime

# Bot setup with command prefix and intents
bot = commands.Bot(command_prefix="%%", intents=discord.Intents.all(), help_command=None)
TOKEN = token

# Snipe message storage
snipe_message_author = {}
snipe_message_content = {}

# F-words counter file
filename = "fwords.csv"


def readFromCsv(filename):
    number = int()
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        # Assuming the CSV file has only one row with one number
        for row in reader:
            number = int(row[0])
        return number


def writeToCsv(filename, number):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([number])


# Login Status & On Ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("%help"))
    print(f"We Have Logged In As {bot.user}")


# Triggers On Delete
@bot.event
async def on_message_delete(message):
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content


# F-words counter
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # F-words counter
    args = message.content.split(" ")
    for arg in args:
        arg = arg.lower()
        if arg.startswith("fuck"):
            writeToCsv(filename, readFromCsv(filename) + 1)
        elif arg == "f":
            writeToCsv(filename, readFromCsv(filename) + 1)
        elif "fuck" in arg:
            writeToCsv(filename, readFromCsv(filename) + 1)
        elif arg == "fuc" or arg == "stfu" or arg == "fu" or arg == "fk" or arg == "tf" or arg == "wtf":
            writeToCsv(filename, readFromCsv(filename) + 1)

    # To reply to certain words
    args = message.content.split(" ")
    for arg in args:
        if arg.lower() == "yo1":
            await message.channel.send("Yo")
        if arg.lower() == "h1" or arg.lower() == "h?":
            await message.channel.send("h")

    msg = message.content.lower()
    if msg == 'cheems':
        await message.channel.send("Cheems Indeed")

    if msg == '.':
        await message.channel.send("...")

    # Process commands after our message handling
    await bot.process_commands(message)


# Snipe command
@bot.command(name='snipe')
async def snipe(ctx):
    try:
        channel = ctx.channel
        snipeEmbed = discord.Embed(title="Gotcha!", description=snipe_message_content[channel.id],
                                   colour=discord.Colour.blue())
        snipeEmbed.set_footer(text=f"Deleted By {snipe_message_author[channel.id]}")
        snipeEmbed.set_thumbnail(url=snipe_message_author[channel.id].avatar)
        await ctx.send(embed=snipeEmbed)
        del snipe_message_author[channel.id]
        del snipe_message_content[channel.id]
    except:
        await ctx.send("No Messages To Snipe or Someone Sniped Before You. Get Better")


# F-words counter command
@bot.command(name='fwords')
async def fwords(ctx):
    embed = discord.Embed(
        title="Total number of F-words used since (12th March 2024)",
        description=f"F-words: {readFromCsv(filename)}",
        colour=discord.Colour.blue()
    )
    embed.set_footer(text="Remember to maintain a respectful and friendly environment.")
    await ctx.send(embed=embed)


# YouTube link command
@bot.command(name='yt', aliases=['youtube'])
async def youtube(ctx):
    await ctx.send("https://www.youtube.com/c/zWORMzGaming")


# Prefix command
@bot.command(name='prefix')
async def prefix(ctx):
    await ctx.send(f"My Prefix Is %")


# Staff command
@bot.command(name='staff')
async def staff(ctx):
    staffEmbed = discord.Embed(
        title="Staff Members",
        description="1.*<@!289056971007459329>* (Admin Man)\n2.*<@448895434249732106>* (Admin Man)\n3.*<@337762379398119424>* (Manager)\n4.*<@424615858854297621>* (Head Mod)\n5.*<@382313958004097027>* (Mod)\n6.*<@501159286223929374>* (Mod)\n7.*<@710445528579702864>* (Mod)\n8.*<@628300268634898433>* (Mod)",
        colour=discord.Colour.blue()
    )
    await ctx.send(embed=staffEmbed)


# Help command
@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(title="zWormz Bot", description="Best Bot ;)", color=discord.Color.red())
    embed.add_field(name="%snipe", value="To See The Last Deleted Message In A Channel", inline=False)
    embed.add_field(name="%fwords", value="Get The Number Of F-words Used Inn The Server", inline=False)
    embed.add_field(name="%convert", value="To Convert Currencies\n'%help currency' For More Info", inline=False)
    embed.add_field(name="%prefix", value="Just In Case You're Still Wondering", inline=False)
    embed.add_field(name="%staff", value="A List Of All The Staff Members", inline=False)
    embed.add_field(name="%yt", value="Link To Kryzzp's Youtube", inline=False)
    embed.add_field(name="%play guess", value="To Play A Number Guessing Game\nOnly Works In <#710259442318442518>", inline=False)
    embed.add_field(name="Other Features-", value="-Custom Member Based Commands Gotta Figure Them Out Yourself", inline=False)
    embed.add_field(name="For Mods:", value="", inline=False)
    embed.add_field(name="%kick", value="To Kick A User", inline=False)
    embed.add_field(name="%ban", value="To Ban A User", inline=False)
    embed.add_field(name="%unban", value="To Unban A User", inline=False)
    embed.add_field(name="%mute", value="To Mute A User", inline=False)
    embed.add_field(name="%unmute", value="To Unmute A User", inline=False)
    embed.set_footer(text="Created By Gaming Tech#8837\nExclusively For zWormz Community")
    await ctx.send(embed=embed)


# Help currency command
@bot.command(name='help_currency')
async def help_currency(ctx):
    embed = discord.Embed(
        title="Currency Conversion Commands-",
        description='Use These After Using "%convert"\n-"%inr to usd"\n-"%inr to eur"\n-"%eur to inr"\n-"%eur to usd"\n-"%usd to inr"\n-"%usd to eur"',
        color=discord.Color.green()
    )
    embed.set_footer(text="For Other Currencies Use Currency Bot")
    await ctx.send(embed=embed)


# Currency conversion command
@bot.command(name='convert')
async def convert(ctx):
    await ctx.send('What Currency You Wanna Convert\nEg-"inr to usd" or "usd to inr"')

    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author

    try:
        currency_input = await bot.wait_for("message", check=check, timeout=30.0)

        if str(currency_input.content).lower() == "stop":
            await ctx.send("Alright")
            return

        elif currency_input.content.lower() == "inr to usd":
            await ctx.send("Enter Amount In INR\n(only numbers without symbols)")

            currency_amount = await bot.wait_for("message", check=check, timeout=30.0)

            if str(currency_amount.content).lower() == "stop":
                await ctx.send("Alright")
                return

            converted_currency = int(currency_amount.content) * 0.013
            await ctx.send(f"₹ {currency_amount.content} INR = $ {round(converted_currency, 2)} USD")

        elif currency_input.content.lower() == "usd to inr":
            await ctx.send("Enter Amount In USD\n(only numbers without symbols)")

            currency_amount = await bot.wait_for("message", check=check, timeout=30.0)

            if str(currency_amount.content).lower() == "stop":
                await ctx.send("Alright")
                return

            converted_currency = int(currency_amount.content) * 74.81
            await ctx.send(f"$ {currency_amount.content} USD = ₹ {round(converted_currency, 2)} INR")

        elif currency_input.content.lower() == "eur to inr":
            await ctx.send("Enter Amount In EUR\n(only numbers without symbols)")

            currency_amount = await bot.wait_for("message", check=check, timeout=30.0)

            if str(currency_amount.content).lower() == "stop":
                await ctx.send("Alright")
                return

            converted_currency = int(currency_amount.content) * 84.54
            await ctx.send(f"€ {currency_amount.content} EUR = ₹ {round(converted_currency, 2)} INR")

        elif currency_input.content.lower() == "inr to eur":
            await ctx.send("Enter Amount In INR\n(only numbers without symbols)")

            currency_amount = await bot.wait_for("message", check=check, timeout=30.0)

            if str(currency_amount.content).lower() == "stop":
                await ctx.send("Alright")
                return

            converted_currency = int(currency_amount.content) * 0.012
            await ctx.send(f"₹ {currency_amount.content} INR = € {round(converted_currency, 2)} EUR")

        elif currency_input.content.lower() == "usd to eur":
            await ctx.send("Enter Amount In USD\n(only numbers without symbols)")

            currency_amount = await bot.wait_for("message", check=check, timeout=30.0)

            if str(currency_amount.content).lower() == "stop":
                await ctx.send("Alright")
                return

            converted_currency = int(currency_amount.content) * 0.89738
            await ctx.send(f"$ {currency_amount.content} USD = € {round(converted_currency, 2)} EUR")

        elif currency_input.content.lower() == "eur to usd":
            await ctx.send("Enter Amount In EUR\n(only numbers without symbols)")

            currency_amount = await bot.wait_for("message", check=check, timeout=30.0)

            if str(currency_amount.content).lower() == "stop":
                await ctx.send("Alright")
                return

            converted_currency = int(currency_amount.content) * 1.1294969
            await ctx.send(f"€ {currency_amount.content} EUR = $ {round(converted_currency, 2)} USD")

        else:
            await ctx.send("Invalid currency pair. Use '%help_currency' for available options.")

    except asyncio.TimeoutError:
        await ctx.send("Timed out. Please try again.")


@bot.group()
async def play(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Use `%play guess` to play.')


# Guessing game command
@play.command(name='guess')
async def play_guess(ctx):
    channel = ctx.channel.id

    if channel == 710259442318442518 or channel == 937951965416136754:
        await ctx.send("I Have Chosen A Number Between 1-100 Try To Guess It")

        correct_guess = random.randint(1, 100)
        guess_count = 0
        guess_limit = 5

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        while guess_count < guess_limit:
            guess_count += 1
            remaining_guesses = guess_limit - guess_count

            try:
                user_guess = await bot.wait_for("message", check=check, timeout=30.0)

                if user_guess.content.lower() == "stop":
                    await ctx.send("Ok, I Guess")
                    break

                elif user_guess.content == str(correct_guess):
                    await ctx.send("You Guessed It Right!")
                    break

                elif int(user_guess.content) > correct_guess:
                    await ctx.send("My Number Is Smaller Than Yours")
                    await ctx.send(f"{remaining_guesses} Guesses Remain")

                elif int(user_guess.content) < correct_guess:
                    await ctx.send("My Number Is Larger Than Yours")
                    await ctx.send(f"{remaining_guesses} Guesses Remain")

                if remaining_guesses == 0:
                    await ctx.send("You Ran Out Of Guesses")
                    await ctx.send(f"The Number Was {correct_guess}")
                    break

            except ValueError:
                await ctx.send("Please Enter A Valid Input")

            except asyncio.TimeoutError:
                await ctx.send("Timed out. Game ended.")
                break
    else:
        await ctx.send("Use this in Bot Abuse only")


# Member commands
@bot.command(name='plazo')
async def plazo(ctx):
    embed = discord.Embed(title="Plazo", description="Joe Begriff Lil Scamenzo Plazo", color=0x9b59b6)
    embed.add_field(name="Bday", value="24th Dec", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='grass')
async def grass(ctx):
    embed = discord.Embed(title="bad DrO_NiK", description="He's been requesting me for a year for this :)",
                          color=0x9b59b6)
    embed.add_field(name="Bday", value="I'll add it next year", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='mandar')
async def mandar(ctx):
    embed = discord.Embed(title="Mandar", description="Luckiest person here fr", color=0x9b59b6)
    embed.add_field(name="Bday", value="E", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='gabrrys')
async def gabrrys(ctx):
    embed = discord.Embed(title="Gabrrys", description="GT knows him (yeah ik him)", color=0x9b59b6)
    embed.add_field(name="Bday", value="11th Oct (i knew)", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='stefan')
async def stefan(ctx):
    embed = discord.Embed(title="StefanTheBestblahblah", description="Instagram addict", color=0x9b59b6)
    embed.add_field(name="Bday", value="I forgot sorry 😔", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='mxar')
async def mxar(ctx):
    embed = discord.Embed(title="Mxarkuz", description="Nothing here YET", color=0x9b59b6)
    embed.add_field(name="Bday", value="He didn't tell me on time", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='floof')
async def floof(ctx):
    embed = discord.Embed(title="Floofenshmirtz", description="Our beloved lomda", color=0x9b59b6)
    embed.add_field(name="Bday", value="8th May", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='bloxy')
async def bloxy(ctx):
    embed = discord.Embed(title="Bloxy", description="Tate simp", color=0x9b59b6)
    embed.add_field(name="Bday", value="Whenever tate's bday is", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='farts')
async def farts(ctx):
    embed = discord.Embed(title="RainbowisticFarts", description="The OG admin man", color=0x9b59b6)
    embed.add_field(name="Bday", value="12th Jan", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='jenny')
async def jenny(ctx):
    embed = discord.Embed(title="Jenny", description="Silliest programmer girl (farts didn't ask for it)",
                          color=0x9b59b6)
    embed.add_field(name="Bday", value="5th Nov", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='kryzzp')
async def kryzzp(ctx):
    await ctx.send("Our Favourite Youtuber")


@bot.command(name='loxie')
async def loxie(ctx):
    embed = discord.Embed(title="Loxie", description="Was a mod", color=0x9b59b6)
    embed.add_field(name="Bday", value="21st Sep", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='arch3r')
async def arch3r(ctx):
    embed = discord.Embed(title="Arch3r", description="Amogus", color=0x9b59b6)
    embed.add_field(name="Bday", value="16th Apr", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='iron')
async def iron(ctx):
    embed = discord.Embed(title="IronBlaster36", description="Transport Fever 2 Pro", color=0x9b59b6)
    embed.add_field(name="Bday", value="Unknown", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='ryuko')
async def ryuko(ctx):
    await ctx.send("Plazo's Tomboy Waifu")


@bot.command(name='anon')
async def anon(ctx):
    embed = discord.Embed(title="Anonymous", description="Active 24/7", color=0x9b59b6)
    embed.add_field(name="Bday", value="13th Feb", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='tech_nerd')
async def tech_nerd(ctx):
    embed = discord.Embed(title="The Tech Nerd", description="zwz local doctor", color=0x9b59b6)
    embed.add_field(name="Bday", value="19th Oct", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='gt')
async def gt(ctx):
    embed = discord.Embed(title="Gaming Tech", description="Cheeeeeeeeeeeeeeeems", color=0x9b59b6)
    embed.add_field(name="Bday", value="6th Nov", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='ralph')
async def ralph(ctx):
    embed = discord.Embed(title="Ralph", description="Retired grandpa -h", color=0x9b59b6)
    embed.add_field(name="Bday", value="29th May", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='ayan')
async def ayan(ctx):
    embed = discord.Embed(title="Ayan", description="Ayannn......", color=0x9b59b6)
    embed.add_field(name="Bday", value="15th Nov", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='lone')
async def lone(ctx):
    await ctx.send("Habibi")


@bot.command(name='quietmoment')
async def quietmoment(ctx):
    embed = discord.Embed(title="QuietMoment7", description="Totally Normal Sleep Schedule", color=0x9b59b6)
    embed.add_field(name="Bday", value="14th Julyeee", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='gorcee')
async def gorcee(ctx):
    embed = discord.Embed(title="Gorcee", description="Intel HD Gamer", color=0x9b59b6)
    embed.add_field(name="Bday", value="31st Oct", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='saad')
async def saad(ctx):
    embed = discord.Embed(title="Saad", description="Extremly Happy Boi", color=0x9b59b6)
    embed.add_field(name="Bday", value="19th Oct", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='enerit')
async def enerit(ctx):
    embed = discord.Embed(title="Enerit", description="Kryzzp's Expensive Chair", color=0x9b59b6)
    embed.add_field(name="Bday", value="19th Feb", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='kutmin')
async def kutmin(ctx):
    await ctx.send("Cheems Founder And FreeGame Buster")


@bot.command(name='wolfer')
async def wolfer(ctx):
    await ctx.send("Good Boi Good Mod")


# Admin Commands
@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member.id == ctx.author.id:
        await ctx.send(f"What kinda kink is that?")
        return

    if member.id == 358634118965231626 or member.id == 745881713661575209 or member.id == 638091868948922409:
        await ctx.send(f"You don't have the balls to kick {member.name}")
        return
    elif member.guild_permissions.kick_members or member.guild_permissions.ban_members:
        await ctx.send(f"Nice try, {ctx.author.mention}, but sadly {member.display_name} is a mod. Sit down.")
        return


    if ctx.author.id == 745881713661575209:
        # List of random kick messages
        kick_messages = [
            f"Mandar complained to Quietmoment about {member.name}",
            f"Mandar flexed his Genshin characters on {member.name} too hard.",
            f"{member.name} was crushed between Eula's thighs",
            f"Mandar punched {member.name} off the Endermen farm",
        ]
    else:
        # List of random kick messages
        kick_messages = [
            f"{member.name} was yeeted from the server!",
            f"Goodbye {member.name}! You'll be missed... maybe.",
            f"{ctx.author.name} didn't like {member.name}",
            f"The ban hammer has spoken! {member.name} is out!",
            f"{member.name} was kicked faster than you can say 'oops'!",
            f"Another one bites the dust! Farewell, {member.name}!",
            f"{member.name} will have to play elsewhere now.",
            f"Server population decreased by one: {member.name} is gone!",
            f"{member.name} has been kicked! Maybe they can talk to Plazo about it. iykyk ;)",
            f"{member.name} got kicked in the nuts by {ctx.author.name}. Ouch!",
            f"Kryzzp told {ctx.author.name} to kick {member.name}",
            f"{member.name} sacked the roooock!!!!!!",
        ]

    random_message = random.choice(kick_messages)

    try:
        # Try to DM the user
        await member.send(
            f"You've been kicked from {ctx.guild.name}. Reason: {reason if reason else 'No reason provided.'}\nGet better dude. Sucks to be you.")
    except:
        pass

    try:
        await member.kick(reason=reason)
        await ctx.send(random_message)

        if reason:
            await ctx.send(f"Reason: {reason}")
    except:
        await ctx.send(f"I don't have permission to kick {member.mention}.")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Lmaoo, {ctx.author.name} thinks he has mod perms.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I can't kick air, can I?.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("There's none by that name bruh.")
    else:
        await ctx.send(f"An error occurred: {error}")


@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member.id == ctx.author.id:
        await ctx.send(f"You know you can just leave?")
        return

    if member.id == 358634118965231626 or member.id == 745881713661575209 or member.id == 638091868948922409:
        await ctx.send(f"{ctx.author.name}'s balls punctured while trying to ban {member.name}")
        return
    elif member.guild_permissions.kick_members or member.guild_permissions.ban_members:
        await ctx.send(f"Nice try, {ctx.author.mention}, but unfortunately {member.display_name} is a mod. Better luck next time.")
        return

    if ctx.author.id == 745881713661575209:
        ban_messages = [
            f"Mandar finally had enough of {member.name}'s nonsense",
            f"{member.name} questioned Mandar's gacha luck and paid the price",
            f"Mandar complained to Quietmoment about {member.name}",
            f"Mandar flexed his Genshin characters on {member.name} too hard.",
            f"{member.name} was crushed between Eula's thighs",
            f"Mandar punched {member.name} off the Enderman farm",
        ]
    else:
        # List of random ban messages
        ban_messages = [
            f"{member.name} was banished to the backrooms!",
            f"The banhammer has spoken! {member.name} is out forever! or maybe Plazo can help..",
            f"{ctx.author.name} decided {member.name} needed to touch some grass",
            f"{member.name} was banned faster than Kutmin can post free games in #💶free-games💶",
            f"{member.name} will have to find another server to shit in now.",
            f"Member count permanently decreased by one: {member.name} is gone!",
            f"{member.name} has been banned! Maybe they can beg Kryzzp for forgiveness.",
            f"{member.name} got hit with the ban hammer by {ctx.author.name}. Critical hit!",
            f"Kryzzp ordered {ctx.author.name} to permanently remove {member.name}",
            f"{member.name} messed with the wrong server!",
            f"{member.name} found out what happens when you mess with Plazo!",
            f"The almighty {ctx.author.name} has cast {member.name} into oblivion!",
            f"{member.name} is now banned! Press F to pay respects (or not)."
        ]

    random_message = random.choice(ban_messages)

    try:
        # Try to DM the user
        await member.send(
            f"You've been banned from {ctx.guild.name}. Reason: {reason if reason else 'No reason provided.'}\nLmaoo, imagine getting banned. lolololol")
    except:
        pass

    try:
        await member.ban(reason=reason)
        await ctx.send(random_message)

        if reason:
            await ctx.send(f"Reason: {reason}")
    except:
        await ctx.send(f"I don't have permission to ban {member.mention}.")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Lmfaoo, {ctx.author.name} thinks his tiny hands are powerful enough to wield the ban hammer.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Air has been banned successfully, now die.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("If you're gonna ban them at least mention their name correctly. Who tf is that?")
    else:
        await ctx.send(f"An error occurred: {error}")


@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    try:
        # Check if input is a user ID
        if member.isdigit():
            user_id = int(member)
            user = None

            async for ban_entry in ctx.guild.bans():
                if ban_entry.user.id == user_id:
                    user = ban_entry.user
                    await ctx.guild.unban(user)
                    break

            if user is not None:
                # List of random unban messages
                unban_messages = [
                    f"{ban_entry.user.name} has been given a second chance! As usual.",
                    f"{ctx.author.name} simps for {ban_entry.user.name}",
                    f"The ban has been lifted for {ban_entry.user.name}. Probably begged Plazo",
                    f"{ban_entry.user.name} managed to convince {ctx.author.name} to unban!",
                    f"Looks like {ban_entry.user.name} finally apologized enough to get unbanned!",
                    f"The council has decided: {ban_entry.user.name} deserves redemption!"
                ]

                # Special message if Mandar is doing the unbanning
                if ctx.author.id == 745881713661575209:
                    unban_messages = [
                        f"Mandar simps for {ban_entry.user.name}!",
                        f"{ban_entry.user.name} agreed to find a GF for Mandar.",
                        f"{ban_entry.user.name} bought Mandar a Eula bodypillow ;)",
                        f"Mandar has decided {ban_entry.user.name} deserves another chance. Probably bought welkin for him."
                    ]

                random_message = random.choice(unban_messages)
                await ctx.send(random_message)
                return
            else:
                await ctx.send(f"Could not find a banned user with the name or ID: {member}")

    except ValueError:
        await ctx.send("Invalid format. Use either a User ID or Username#Discriminator format.")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name} got a big heart but no mod perms, lol.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Air has been unbanned, now you can breath.")
    else:
        await ctx.send(f"An error occurred: {error}")


@bot.command(name='mute')
@commands.has_permissions(manage_roles=True)
async def mute(ctx, *, member: discord.Member):
    if member.id == ctx.author.id:
        await ctx.send(f"You know you can just stfu?")
        return

    if member.id == 358634118965231626 or member.id == 745881713661575209 or member.id == 638091868948922409:
        await ctx.send(f"{ctx.author.name} is too short to tape {member.name}'s mouth")
        return
    elif member.guild_permissions.kick_members or member.guild_permissions.ban_members:
        await ctx.send(
            f"Nice try, {ctx.author.mention}, but you cannot mute a mod (I'd suggest removing their mod first, ehe)")
        return

    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        await ctx.send("Muted role doesn't exist. Create one called `Muted` and try again.")
        return

    if muted_role in member.roles:
        await ctx.send(f"{member.name} is already muted. What's your problem man?")
        return

    await member.add_roles(muted_role)

    mute_messages = [
        f"{member.name} has been muted. Too loud, maybe?",
        f"{member.name} got bonked with the mute hammer by {ctx.author.name}.",
        f"{ctx.author.name} said: 'Shut up, {member.name}' (in a nice way ofc).",
        f"{member.name} told {ctx.author.name} to shut up. Ohh look how the tables have turned.",
        f"{member.name} is now mute. Chat is peaceful again.",
    ]

    if ctx.author.id == 745881713661575209:
        mute_messages = [
            f"Mandar muted {member.name} with love ❤️",
            f"{member.name} said bad things about Eula, Mandar took it personally.",
            f"Mandar’s silence spell worked. {member.name} is now quiet.",
            f"{member.name} got muted for asking Mandar to touch grass."
        ]

    await ctx.send(random.choice(mute_messages))

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"How about you stfu instead?.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("*Cuts off your ear so you cannot hear the wind*")
    else:
        await ctx.send(f"An unknown error occurred: {error}")


@bot.command(name='unmute')
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, *, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        await ctx.send("Muted role doesn't exist. Try unmuting air instead.")
        return

    if muted_role not in member.roles:
        await ctx.send(f"{member.name} is not muted. You good, {ctx.author.name}?")
        return

    await member.remove_roles(muted_role)

    unmute_messages = [
        f"{member.name} is free to scream again. Thanks, {ctx.author.name}?",
        f"{ctx.author.name} gave {member.name} back their voice. Brave move.",
        f"{member.name} was unmuted. Peace was short-lived.",
        f"{ctx.author.name} unmuted {member.name}. Let chaos resume.",
        f"{member.name} can talk again. Time to regret that soon."
    ]

    if ctx.author.id == 745881713661575209:
        unmute_messages = [
            f"Mandar unmuted {member.name}. Must be love.",
            f"Mandar brought {member.name} back from Quietmoment's company.",
            f"{member.name} bribed Mandar with primogems to get unmuted.",
            f"Mandar granted {member.name} the power of speech again. Praise be."
        ]

    await ctx.send(random.choice(unmute_messages))

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Maybe request Plazo?")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Unmute who? The ghost of your dignity?")
    else:
        await ctx.send(f"Something broke: {error}")


@bot.command(name='warn')
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    embed = discord.Embed(title="⚠️ Warning Issued", color=discord.Color.orange())
    embed.add_field(name="Warned User", value=member.mention, inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.add_field(name="Warned By", value=ctx.author.mention, inline=False)
    embed.set_footer(text="Consider shutting the fuck up to avoid further action.")

    await ctx.send(embed=embed)

    try:
        await member.send(embed=embed)
    except:
        pass

    log_channel = bot.get_channel(1376678099856658584)
    log_embed = discord.Embed(title="⚠️ Warning Issued", color=discord.Color.orange())
    log_embed.add_field(name="Warned User", value=member.mention, inline=False)
    log_embed.add_field(name="Reason", value=reason, inline=False)
    log_embed.add_field(name="Warned By", value=ctx.author.mention, inline=False)
    log_embed.add_field(name="Date", value=f"{datetime.datetime.now().day} {datetime.datetime.now().strftime('%B')} {datetime.datetime.now().year}", inline=False)
    log_embed.set_footer(text="Does anyone even give a shit about warns?")
    if log_channel:
        await log_channel.send(embed=log_embed)

@warn.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Get Mod First")
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="⚠️ Warning Issued", color=discord.Color.orange())
        embed.add_field(name="Warned User", value=ctx.author.mention, inline=False)
        embed.add_field(name="Reason", value="Forgot to mention the user and wasted my time", inline=False)
        embed.add_field(name="Warned By", value=ctx.author.mention, inline=False)
        embed.set_footer(text="Consider double checking the command before sending.")

        await ctx.send(embed=embed)

        log_channel = bot.get_channel(1376678099856658584)
        if log_channel:
            embed.add_field(name="Date", value=f"{datetime.datetime.now().day} {datetime.datetime.now().strftime('%B')} {datetime.datetime.now().year}", inline=False)
            await log_channel.send(embed=embed)
    else:
        await ctx.send(f"Something broke: {error}")


keep_alive()
bot.run(TOKEN)