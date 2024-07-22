import discord
import os
import time
import random
from replit import db
from keep_alive import keep_alive 
from discord.ui import Select
import csv
#from discord_components import DiscordComponents



#all the assignments
#client2 = commands.Bot(command_prefix = "%")
client2 = discord.Client(intents= discord.Intents.all())
TOKEN = os.environ['TOKEN_ZWZ']
db["prefix_zwz"] = "%"  



#Login Status & On Ready
@client2.event
async def on_ready():
  await client2.change_presence(activity = discord.Game("%help"))
  print("We Have Logged In As {0.user}".format(client2))
  #DiscordComponents(client2)

snipe_message_author = {}
snipe_message_content = {}



#Triggers On Delete
@client2.event
async def on_message_delete(message):
  snipe_message_author[message.channel.id] = message.author
  snipe_message_content[message.channel.id] = message.content

  

#updates on every message
@client2.event
async def on_message(message):
  if message.author == client2.user:
    return

  msg = message.content

  prefix = db["prefix_zwz"]


  
  #color roles
  if msg == (prefix + 'color'):
    print("h")
    h = 1
    roles = message.author.roles
    for x in roles:
      if x.id == 728559929014878329 or h == 1:
        print("h2")
        await message.channel.send(content = "Click On The Dropdown Menu To Select Color Roles", components =
          [
            Select(placeholder = "Select Something",options = [
              discord.SelectOption(label = "Red", value = "red"),
              discord.SelectOption(label = "Blue", value = "blue"),
              discord.SelectOption(label = "Green", value = "green"),
              discord.SelectOption(label = "❌Cancel", value = "cancel")
          ],
          custom_id = "colormenu"
          )])

        print("hmm")
        #interaction = await client2.user.wait_for("select_option", check=None)
        interaction = await client2.wait_for('select_option', check = lambda inter: inter.custom_id == "colormenu")
        print("hmm2")

        print(interaction.label)
        print("hmm3")

        res = interaction.values[0]
        print("hmm4")

        if res == "cancel":
          print("h3")
          await interaction.send("Cancelled Successfully")
        
        elif res == "red":
          for x in roles:
            if x.id == 844854038314221588:
              await interaction.send("You Already Have That Role **Dum Dum**")
            else:
              await message.author.add_role(844854038314221588)
              await interaction.send("Role Successfully Added")

        elif res == "blue":
          for x in roles:
            if x.id == 844855037398220830:
              await interaction.send("You Already Have That Role **Dum Dum**")
            else:
              await message.author.add_role(844855037398220830)
              await interaction.send("Role Successfully Added")

        elif res == "green":
          for x in roles:
            if x.id == 844854522421313576:
              await interaction.send("You Already Have That Role **Dum Dum**")
            else:
              await message.author.add_role(844854522421313576)
              await interaction.send("Role Successfully Added")





  # F-words counter
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
      
  args = message.content.split(" ")
  for arg in args:
    arg = arg.lower()
    if arg.startswith("fuck"):
      writeToCsv(filename, readFromCsv(filename) + 1)
    elif arg == "f":
      writeToCsv(filename, readFromCsv(filename) + 1)
    elif "fuck" in arg or "fuck" in arg:
      writeToCsv(filename, readFromCsv(filename) + 1)
    elif arg == "fuc" or arg == "stfu" or arg == "fu" or arg == "fk" or arg == "tf" or arg == "wtf":
      writeToCsv(filename, readFromCsv(filename) + 1)

  if msg == (prefix + 'fwords'):
    embed = discord.Embed(title = "Total number of F-words used since (12th March 2024)", description = f"F-words: {readFromCsv(filename)}", colour = discord.Colour.blue())
    embed.set_footer(text = "Remember to maintain a respectful and friendly environment.")
    
    await message.channel.send(embed = embed)
      





  #snipe command
  try:
     if msg.lower() == (prefix + 'snipe'):
       channel = message.channel
    
       snipeEmbed = discord.Embed(title = "Gotcha!", description = snipe_message_content[channel.id], colour = discord.Colour.blue())
       snipeEmbed.set_footer(text = f"Deleted By {snipe_message_author[channel.id]}")
       snipeEmbed.set_thumbnail(url = snipe_message_author[message.channel.id].avatar)
       await message.channel.send(embed = snipeEmbed)
       del snipe_message_author[channel.id]
       del snipe_message_content[channel.id]
  except:
      await message.channel.send("No Messages To Snipe or Someone Sniped Before You. Get Better")    




  


  #responses
  if msg == (prefix + 'yt') or msg == (prefix + 'youtube'):
    await message.channel.send("https://www.youtube.com/c/zWORMzGaming")





              
  #Member Commands
  if msg.lower() == (prefix + 'plazo'):
    embedMembers = discord.Embed(title = "Plazo", description = "Joe Begriff Lil Scamenzo Plazo", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "24th Dec", inline = False)
    await message.channel.send(embed = embedMembers)


    #Draft For Embed
    #embedMembers = discord.Embed(title = "", description = "", color = 0x9b59b6)
    #embedMembers.add_field(name = "Bday", value = "", inline = False)
    #await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'grass'):
    embedMembers = discord.Embed(title = "bad DrO_NiK", description = "He's been requesting me for a year for this :)", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "I'll add it next year", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'mandar'):
    embedMembers = discord.Embed(title = "Mandar", description = "Luckiest person here fr", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "E", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'gabrrys'):
    embedMembers = discord.Embed(title = "Gabrrys", description = "GT knows him (yeah ik him)", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "11th Oct (i knew)", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'stefan'):
    embedMembers = discord.Embed(title = "StefanTheBestblahblah", description = "Instagram addict", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "I forgot sorry 😔", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'mxar'):
    embedMembers = discord.Embed(title = "Mxarkuz", description = "Nothing here YET", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "He didn't tell me on time", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'floof'):
    embedMembers = discord.Embed(title = "Floofenshmirtz", description = "Our beloved lomda", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "8th May", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'bloxy'):
    embedMembers = discord.Embed(title = "Bloxy", description = "Tate simp", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "Whenever tate's bday is", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'farts'):
    embedMembers = discord.Embed(title = "RainbowisticFarts", description = "The OG admin man", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "12th Jan", inline = False)
    await message.channel.send(embed = embedMembers)

  
  if msg == (prefix + 'jenny'):
    embedMembers = discord.Embed(title = "Jenny", description = "Silliest programmer girl (farts didn't ask for it)", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "5th Nov", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'kryzzp'):
    await message.channel.send("Our Favourite Youtuber")


  if msg == (prefix + 'loxie'):
    embedMembers = discord.Embed(title = "Loxie", description = "Was a mod", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "21st Sep", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'arch3r'):
    embedMembers = discord.Embed(title = "Arch3r", description = "Amogus", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "16th Apr", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'iron'):
    embedMembers = discord.Embed(title = "IronBlaster36", description = "Transport Fever 2 Pro", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "Unknown", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'ryuko'):
    await message.channel.send("Plazo's Tomboy Waifu")
  

  if msg == (prefix + 'anon'):
    embedMembers = discord.Embed(title = "Anonymous", description = "Active 24/7", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "13th Feb", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'tech nerd'):
    embedMembers = discord.Embed(title = "The Tech Nerd", description ="zwz local doctor", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "19th Oct", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'gt'):
    embedMembers = discord.Embed(title = "Gaming Tech", description = "Cheeeeeeeeeeeeeeeems", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "6th Nov", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'ralph'):
    embedMembers = discord.Embed(title = "Ralph", description = "Retired grandpa -h", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "29th May", inline = False)
    await message.channel.send(embed = embedMembers)
  

  if msg == (prefix + 'ayan'):
    embedMembers = discord.Embed(title = "Ayan", description = "Ayannn......", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "15th Nov", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'lone'):
    await message.channel.send("Habibi")


  if msg == (prefix + 'quietmoment'):
    embedMembers = discord.Embed(title = "QuietMoment7", description = "Totally Normal Sleep Schedule", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "14th Julyeee", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'gorcee'):
    embedMembers = discord.Embed(title = "Gorcee", description = "Intel HD Gamer", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "31st Oct", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'saad'):
    embedMembers = discord.Embed(title = "Saad", description = "Extremly Happy Boi", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "19th Oct", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'enerit'):
    embedMembers = discord.Embed(title = "Enerit", description = "Kryzzp's Expensive Chair", color = 0x9b59b6)
    embedMembers.add_field(name = "Bday", value = "19th Feb", inline = False)
    await message.channel.send(embed = embedMembers)


  if msg == (prefix + 'kutmin'):
    await message.channel.send("Cheems Founder And FreeGame Buster")


  if msg == (prefix + 'wolfer'):
    await message.channel.send("Good Boi Good Mod")


  if msg == (prefix + 'prefix'):
    await message.channel.send(f"My Prefix Is {prefix}")



  


  
  #Staff Commands
  if msg.lower() == (prefix + 'staff'):

    staffEmbed = discord.Embed(title = "Staff Members", description = "1.*<@!289056971007459329>* (Admin Man)\n2.*<@448895434249732106>* (Admin Man)\n3.*<@337762379398119424>* (Manager)\n4.*<@424615858854297621>* (Head Mod)\n5.*<@382313958004097027>* (Mod)\n6.*<@501159286223929374>* (Mod)\n7.*<@710445528579702864>* (Mod)\n8.*<@628300268634898433>* (Mod)", colour = discord.Colour.blue())

    await message.channel.send(embed = staffEmbed)
    






  

  #Currency Convertion
  if msg.lower() == (prefix + "convert"):

    await message.channel.send('What Currency You Wanna Convert\nEg-"inr to usd" or "usd to inr"')

    def check2(m):
        return m.channel == message.channel and m.author.id == message.author.id
    async def waitForMessage2():
        return await client2.wait_for("message", check=check2)

    while True:
      currency_input = await waitForMessage2()

      if str(currency_input.content) == "stop" or str(currency_input.content) == "Stop":
        await message. channel.send("Alright")
        break

      elif currency_input.content == ("inr to usd") or currency_input.content == ("Inr to usd"):
        await message.channel.send("Enter Amount In INR\n(only numbers without symbols)")

        currency_amount = await waitForMessage2()

        if str(currency_amount.content) == "stop" or str(currency_amount.content) == "Stop":
          break
        
        converted_currency = int(currency_amount.content) * 0.013

        await message.channel.send(f"₹ {currency_amount.content} INR = $ {round(converted_currency, 2)} USD")
        break
      
      elif currency_input.content == ("usd to inr") or currency_input.content == ("Usd to inr"):
        await message.channel.send("Enter Amount In USD\n(only numbers without symbols)")

        currency_amount = await waitForMessage2()

        if currency_amount.content == "stop" or currency_amount.content == "Stop":
          break
        
        converted_currency = int(currency_amount.content) * 74.81

        await message.channel.send(f"$ {currency_amount.content} USD = ₹ {round(converted_currency, 2)} INR")
        break

      elif currency_input.content == ("eur to inr") or currency_input.content == ("Eur to inr"):
        await message.channel.send("Enter Amount In EUR\n(only numbers without symbols)")

        currency_amount = await waitForMessage2()

        if currency_amount.content == "stop" or currency_amount.content == "Stop":
          break
        
        converted_currency = int(currency_amount.content) * 84.54

        await message.channel.send(f"€ {currency_amount.content} EUR = ₹ {round(converted_currency, 2)} INR")
        break

      elif currency_input.content == ("inr to eur") or currency_input.content == ("Inr to eur"):
        await message.channel.send("Enter Amount In INR\n(only numbers without symbols)")

        currency_amount = await waitForMessage2()

        if currency_amount.content == "stop" or currency_amount.content == "Stop":
          break
        
        converted_currency = int(currency_amount.content) * 0.012

        await message.channel.send(f"₹ {currency_amount.content} INR = € {round(converted_currency, 2)} EUR")
        break

      elif currency_input.content == ("usd to eur") or currency_input.content == ("Usd to eur"):
        await message.channel.send("Enter Amount In USD\n(only numbers without symbols)")

        currency_amount = await waitForMessage2()

        if currency_amount.content == "stop" or currency_amount.content == "Stop":
          break
        
        converted_currency = int(currency_amount.content) * 0.89738

        await message.channel.send(f"$ {currency_amount.content} USD = € {round(converted_currency, 2)} EUR")
        break

      elif currency_input.content == ("eur to usd") or currency_input.content == ("Eur to usd"):
        await message.channel.send("Enter Amount In EUR\n(only numbers without symbols)")

        currency_amount = await waitForMessage2()

        if currency_amount.content == "stop" or currency_amount.content == "Stop":
          break
        
        converted_currency = int(currency_amount.content) * 1.1294969

        await message.channel.send(f"€ {currency_amount.content} EUR = $ {round(converted_currency, 2)} USD")
        break
        




  

  #to reply to certain words
  #reply commnads 
  args = message.content.split(" ")
  for arg in args:
    if arg.lower() == "yo1":
      await message.channel.send("Yo")
    if arg.lower() == "h1" or arg.lower() == "h?":
      await message.channel.send("h")

    if msg.lower() == ('cheems'):
      await message.channel.send("Cheems Indeed")
    
    if msg.lower() == ('.'):
      await message.channel.send("...")

    


  #Help commands
  if msg.lower() == (prefix + 'help'):

    embed = discord.Embed(title = "zWormz Bot", description = "Best Bot ;)", color = discord.Color.red())

    embed.add_field(name = "%snipe", value = "To See Last Deleted Message In A Channel", inline = False)
    embed.add_field(name = "%convert", value = "To Convert Currencies\n'%help currency' For More Info", inline = False)
    embed.add_field(name = "%prefix", value = "Just In Case You're Still Wondering", inline = False)
    embed.add_field(name = "%staff", value = "A List Of All Staff Members", inline = False)
    embed.add_field(name = "%yt", value = "Link To Kryzzp's Youtube", inline = False)
    embed.add_field(name = "%play guess",value = "To Play A Number Guessing Game\nOnly Works In <#710259442318442518>", inline = False)
    embed.add_field(name = "Other Features-", value = "-Custom Member Based Commands Gotta Figure Them Out Yourself", inline = False)
    embed.set_footer(text = "Created By Gaming Tech#8837\nExclusively For zWormz Community")

    await message.channel.send(embed = embed)


  #Help currency
  if msg.lower() == (prefix + 'help currency'):
    embed = discord.Embed(title = "Currency Conversion Commands-", description = 'Use These After Using "%convert"\n-"%inr to usd"\n-"%inr to eur"\n-"%eur to inr"\n-"%eur to usd"\n-"%usd to inr"\n-"%usd to eur"', color = discord.Color.green())
    embed.set_footer(text = "For Other Currencies Use Currency Bot")
    await message.channel.send(embed = embed)



  #Guessing game
  if msg.lower() == (prefix + "play guess"):

    channel = message.channel.id
    
    if channel == 710259442318442518 or channel == 937951965416136754:
      await message.channel.send("I Have Chosen A Number Between 1-100 Try To Guess It")

      correct_guess = random.randint(1, 101)
      guess_count = 0
      guess_limit = 5

      def check(m):
          return m.channel == message.channel and m.author.id == message.author.id
      async def waitForMessage():
          return await client2.wait_for("message", check=check)

      while guess_count <= guess_limit:
        guess_count += 1
        remaining_guesses = guess_limit - guess_count
        #await message.reply("Waiting for response")
        user_guess = await waitForMessage()
        #await message.reply("Got response")
        try:
          if user_guess.content == str("Stop") or user_guess.content == str("stop"):
            await message.channel.send("Ok, I Guess")
            break
          elif user_guess.content == str(correct_guess):
            await message.channel.send("You Guessed It Right!")
            break
          elif remaining_guesses == 0:
            await message.channel.send("You Ran Out Of Guesses")
            await message.channel.send(f"The Number Was {correct_guess}")
            break
          elif int(user_guess.content) > correct_guess:
            await message.channel.send("My Number Is Smaller Than Yours")
            await message.channel.send(f"{remaining_guesses} Guesses Remain")
          elif int(user_guess.content) < correct_guess:
            await message.channel.send("My Number Is Larger Than Yours")
            await message.channel.send(f"{remaining_guesses} Guesses Remain")
          elif remaining_guesses == 0:
            await message.channel.send("You Ran Out Of Guesses")
            await message.channel.send(f"The Number Was {correct_guess}")
            break
        except:
          await message.channel.send("Please Enter A Valid Input")
    else:
      await message.channel.send("Use this in Bot Abuse only")



keep_alive()
client2.run(TOKEN)