import discord
from discord.ext import commands
import random
from keep_alive import keep_alive
import csv
import asyncio
from bot_token import token

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
    embed.add_field(name="%snipe", value="To See Last Deleted Message In A Channel", inline=False)
    embed.add_field(name="%convert", value="To Convert Currencies\n'%help currency' For More Info", inline=False)
    embed.add_field(name="%prefix", value="Just In Case You're Still Wondering", inline=False)
    embed.add_field(name="%staff", value="A List Of All Staff Members", inline=False)
    embed.add_field(name="%yt", value="Link To Kryzzp's Youtube", inline=False)
    embed.add_field(name="%play guess", value="To Play A Number Guessing Game\nOnly Works In <#710259442318442518>",
                    inline=False)
    embed.add_field(name="Other Features-", value="-Custom Member Based Commands Gotta Figure Them Out Yourself",
                    inline=False)
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


keep_alive()
bot.run(TOKEN)