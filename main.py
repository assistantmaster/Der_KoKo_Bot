import discord
from discord.ext import commands
from discord.ui import Button, View
import os
import random

token = "YOUR TOKEN"
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # Add this line to enable voice state intents
intents.members = True  # Add this line to enable member intents


class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot(command_prefix="\\", intents=intents)
botlog = bot.get_channel(1204440357476241438)
if os.path.exists("./count.txt"):
    with open("./count.txt", "r") as count:
        current_count = int(count.read())
else:
    current_count = 0

if os.path.exists("./countuser.txt"):
    with open("./countuser.txt", "r") as countuser:
        countuser = int(countuser.read())
else:
    countuser = 0


@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.tree.command(name="ping", description="Replies with pong")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="80s Musik")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f'Logged in as {bot.user}')
    create_ticket_channel = bot.get_channel(1204307581351366666)
    async for message in create_ticket_channel.history(limit=1):
        await message.delete()
    embed = discord.Embed(title="Ticket erstellen", description="Klicke auf den Button unten, um ein Ticket zu erstellen.", color=0x00ff00)
    view = TicketView()
    await create_ticket_channel.send(embed=embed, view=view)
    
@bot.event
async def on_message(msg):
    botlog = bot.get_channel(1204440357476241438)
    if not msg.author == bot.user:
        #print(f"[{msg.author}] {msg.content}")
        if ("idiot" in msg.content or
        "dummkopf" in msg.content or
        "trottel" in msg.content or
        "arschloch" in msg.content or
        "mistkerl" in msg.content or
        "blödmann" in msg.content or
        "spast" in msg.content or
        "hornochse" in msg.content or
        "vollidiot" in msg.content or
        "pissnelke" in msg.content or
        "schwachkopf" in msg.content or
        "depp" in msg.content or
        "penner" in msg.content or
        "verlierer" in msg.content or
        "honk" in msg.content or
        "fuck" in msg.content or
        "fick" in msg.content or
        "shit" in msg.content or
        "asshole" in msg.content or
        "bastard" in msg.content or
        "moron" in msg.content or
        "idiot" in msg.content or
        "loser" in msg.content or
        "dumbass" in msg.content or
        "jackass" in msg.content or
        "jerk" in msg.content or
        "prick" in msg.content or
        "twat" in msg.content or
        "wanker" in msg.content or
        "dipshit" in msg.content or
        "douchebag" in msg.content):
            await msg.delete()
            embed = discord.Embed(title="Nachricht gelöscht",
                description=f'{msg.author.mention} hat "{msg.content}" in {msg.channel.mention} gesendet!',
                color=0xff0000)
            #await botlog.send(f'**Nachricht Gelöscht:** {msg.author.mention} hat "{msg.content}" in {msg.channel.mention} gesendet!')
            await botlog.send(embed=embed)

        if msg.channel.id == 1203656361901035520:
            global current_count, countuser
            try:
                if msg.content is int:
                    number = int(msg.content)
                if os.path.exists("./countuser.txt"):
                    with open("./countuser.txt", "r") as countuser:
                        countuser = int(countuser.read())

                if number == current_count + 1:
                    if msg.author.id != countuser:
                        current_count += 1
                        countuser = msg.author.id
                        with open("./count.txt", "w") as count:
                            count.write(str(current_count))
                        with open("./countuser.txt", "w") as count:
                            count.write(str(countuser))
                        await msg.add_reaction("✅")
                    else:
                        await msg.delete()
                        await msg.channel.send(f"Bitte lass auch die anderen Leute zählen.")
                else:
                    await msg.delete()
                    await msg.channel.send(f"Das war nicht die korrekte Zahl. Die nächste Zahl sollte {current_count + 1} sein.")
            except ValueError:
                await msg.delete()
                await msg.channel.send("Bitte sende eine gültige Zahl.")
        
    await bot.process_commands(msg)

@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    if after.channel and after.channel.id == 1303123299307491330:
        new_channel = await guild.create_voice_channel(name=f"{member.name}'s Channel", category=after.channel.category)
        await member.move_to(new_channel)

        def check(m, b, a):
            return m == member and a.channel != new_channel

        await bot.wait_for('voice_state_update', check=check)
        await new_channel.delete()

@bot.event
async def on_member_join(member):
    player_role = member.guild.get_role(1203439759679168532)
    announcement_role = member.guild.get_role(1206020311905214466)
    welcome_channel = bot.get_channel(1204439767517761677)  # Replace with your welcome channel ID
    await member.add_roles(player_role)
    await member.add_roles(announcement_role)
    embed = discord.Embed(title=f"Willkommen {member}!",
        description=f"Willkommen {member.mention} und viel Spaß auf unserem Discord-Server! Am besten liest du dir kurz noch die Regeln durch. <:Welcome:1291012438640168960>",
        colour=0x00ff00)
    embed.set_thumbnail(url=f"{member.avatar.url}")
    await welcome_channel.send(embed=embed)
    #await welcome_channel.send(f"Willkommen {member.mention} und viel Spaß auf unserem Discord-Server! Am besten liest du dir kurz noch die Regeln durch. 😉!")

@bot.event
async def on_raw_reaction_add(payload):
    ChID = 1203627969617334272
    if payload.channel_id != ChID:
        return
    if str(payload.emoji) == "❌":
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        announcement_role = discord.utils.get(guild.roles, id=1206020311905214466)
        await member.remove_roles(announcement_role)

@bot.event
async def on_raw_reaction_remove(payload):
    ChID = 1203627969617334272
    if payload.channel_id != ChID:
        return
    if str(payload.emoji) == "❌":
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        announcement_role = discord.utils.get(guild.roles, id=1206020311905214466)
        await member.add_roles(announcement_role)

# TODO: TICKET 
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🎫 Ticket erstellen", style=discord.ButtonStyle.green)
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        botlog = bot.get_channel(1204440357476241438)
        guild = interaction.guild
        category = interaction.channel.category

        ticket_channel = await category.create_text_channel(f"ticket-{interaction.user.name}")
        supporter_role = guild.get_role(1203345032543866910)  # Replace with your Supporter role ID

        await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await ticket_channel.set_permissions(supporter_role, read_messages=True, send_messages=True)
        await ticket_channel.set_permissions(guild.default_role, read_messages=False)

        embed = discord.Embed(title="Ticket erstellt",
            description=f"Vielen Dank {interaction.user.mention}, dass du ein Ticket erstellt hast. Bitte beschreibe dein Problem so genau wie Möglich. Ein {supporter_role.mention} wird sich bald um dich kümmern. Sollte dein Problem behoben sein, drücke auf den Button unten, um das Ticket zu schließen.",
            color=0x00ff00)
        #await ticket_channel.send(f"Willkommen {interaction.user.mention}, ein Teammitglied wird sich bald um dein Anliegen kümmern. Bitte erkläre dein Anliegen so genau wie möglich, so dass wir dir schnellstmöglichst helfen können!")

        close_button_view = CloseTicketView(ticket_channel)
        #await ticket_channel.send("Klicke auf den Button unten, um das Ticket zu schließen.", view=close_button_view)
        await ticket_channel.send(embed=embed, view=close_button_view)
        await interaction.response.send_message(f"Dein Ticket wurde erstellt: {ticket_channel.mention}", ephemeral=True)
        embed = discord.Embed(title="Ticket erstellt",
            description=f"{interaction.user.mention} hat ein Ticket in {ticket_channel.mention} erstellt!",
            color=0x00ff00)
        await botlog.send(embed=embed)

class CloseTicketView(View):
    def __init__(self, ticket_channel):
        super().__init__(timeout=None)
        self.ticket_channel = ticket_channel

    @discord.ui.button(label="🎫 Ticket schließen", style=discord.ButtonStyle.red)
    async def close_ticket(self,  interaction: discord.Interaction, button: Button):
        botlog = bot.get_channel(1204440357476241438)
        await self.ticket_channel.delete()
        embed = discord.Embed(title="Ticket gelöscht",
            description=f"{interaction.user.mention} hat sein Ticket gelöscht!",
            color=0x000000)
        await botlog.send(embed=embed)
        
@bot.tree.command(name="ticket", description='Erstellt ein "Ticket erstellen"-Embed')
async def ticket(interaction: discord.Interaction):
    embed = discord.Embed(title="Ticket erstellen", description="Klicke auf den Button unten, um ein Ticket zu erstellen.", color=0x00ff00)
    view = TicketView()
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="yt_announcement", description='Erstellt eine Nachricht zum entfernen der "yt-announcement"-Rolle')
async def yt_announcement(interaction: discord.Interaction):
    channel = bot.get_channel(1203627969617334272)
    await channel.send('Wer keine Benachrichtigung bei einem Upload erhalten möchte, kann auf diese Nachricht mit "❌" reagieren!')

# TODO: TICTACTOE
class TicTacToeButton(Button):
    def __init__(self, x, y, game_view):
        super().__init__(label="\u200b", style=discord.ButtonStyle.secondary, row=y)
        self.x = x
        self.y = y
        self.game_view = game_view

    async def callback(self, interaction):
        view = self.game_view

        if interaction.user != view.current_player:
            await interaction.response.send_message("Du bist nicht dran!", ephemeral=True)
            return

        if view.board[self.y][self.x] != "":
            await interaction.response.send_message("Dieses Feld ist bereits belegt.", ephemeral=True)
            return

        mark = "❌" if view.current_player == view.player1 else "⭕"
        self.label = mark
        self.style = discord.ButtonStyle.danger if mark == "❌" else discord.ButtonStyle.success
        self.disabled = True
        view.board[self.y][self.x] = mark

        winner = view.check_winner()
        if winner:
            for child in view.children:
                child.disabled = True
            winner_mention = view.player1.mention if winner == "❌" else view.player2.mention
            await interaction.response.edit_message(content=f"{winner_mention} gewinnt!", view=view)
            view.stop()
        elif view.is_draw():
            for child in view.children:
                child.disabled = True
            await interaction.response.edit_message(content="Unentschieden!", view=view)
            view.stop()
        else:
            view.current_player = view.player2 if view.current_player == view.player1 else view.player1
            await interaction.response.edit_message(
                content=f"{view.current_player.mention} ist dran ({'❌' if view.current_player == view.player1 else '⭕'})",
                view=view
            )


class TicTacToeView(View):
    def __init__(self, player1: discord.User, player2: discord.User):
        super().__init__(timeout=60)
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.board = [["" for _ in range(3)] for _ in range(3)]

        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y, self))

    def check_winner(self):
        lines = []

        # Reihen, Spalten, Diagonalen
        lines.extend(self.board)  # rows
        lines.extend([[self.board[y][x] for y in range(3)] for x in range(3)])  # columns
        lines.append([self.board[i][i] for i in range(3)])  # diag1
        lines.append([self.board[i][2 - i] for i in range(3)])  # diag2

        for line in lines:
            if line[0] != "" and all(cell == line[0] for cell in line):
                return line[0]
        return None

    def is_draw(self):
        return all(cell != "" for row in self.board for cell in row)


@bot.tree.command(name="tictactoe", description="Starte ein TicTacToe-Spiel gegen jemanden.")
async def tictactoe(interaction: discord.Interaction, user: discord.Member):
    if user.bot:
        await interaction.response.send_message("Du kannst nicht gegen einen Bot spielen.", ephemeral=True)
        return

    if user == interaction.user:
        await interaction.response.send_message("Du kannst nicht gegen dich selbst spielen.", ephemeral=True)
        return

    view = TicTacToeView(interaction.user, user)
    await interaction.response.send_message(
        f"TicTacToe: {interaction.user.mention} (❌) vs {user.mention} (⭕)\n{interaction.user.mention} beginnt!",
        view=view
    )

# TODO: ROCK PAPER SCISSORS

class RPSButton(Button):
    def __init__(self, label, choice, game_view):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.choice = choice
        self.game_view = game_view

    async def callback(self, interaction: discord.Interaction):
        # Spielerwahl und Überprüfen der Spielbedingungen
        player = interaction.user
        game_view = self.game_view
        game_view.player_choices[player] = self.choice  # Speichern der Wahl des Spielers

        # Wenn beide Spieler eine Wahl getroffen haben, ermitteln wir das Ergebnis
        if len(game_view.player_choices) == 2:
            player1, player2 = list(game_view.player_choices.keys())
            choice1 = game_view.player_choices[player1]
            choice2 = game_view.player_choices[player2]

            result = self.determine_winner(choice1, choice2, player1, player2)
            await interaction.response.edit_message(content=result, view=game_view)
            game_view.stop()
        else:
            await interaction.response.send_message(f"{player.mention} hat {self.choice} gewählt!", ephemeral=True)

    def determine_winner(self, choice1, choice2, player1, player2):
        """Bestimmt den Gewinner anhand der Schere, Stein, Papier-Regeln"""
        if choice1 == choice2:
            return f"Unentschieden! {player1.mention} und {player2.mention} haben das gleiche gewählt."
        elif (choice1 == "Schere" and choice2 == "Papier") or \
             (choice1 == "Papier" and choice2 == "Stein") or \
             (choice1 == "Stein" and choice2 == "Schere"):
            return f"{player1.mention} gewinnt! ({choice1} vs {choice2})"
        else:
            return f"{player2.mention} gewinnt! ({choice2} vs {choice1})"


class RPSView(View):
    def __init__(self, player1: discord.User, player2: discord.User):
        super().__init__(timeout=60)
        self.player1 = player1
        self.player2 = player2
        self.player_choices = {}  # Speichert die Wahl beider Spieler

        # Buttons für die Auswahl
        self.add_item(RPSButton("Schere", "Schere", self))
        self.add_item(RPSButton("Stein", "Stein", self))
        self.add_item(RPSButton("Papier", "Papier", self))


@bot.tree.command(name="rps", description="Starte ein Schere, Stein, Papier-Spiel gegen einen anderen Spieler.")
async def rps(interaction: discord.Interaction, user: discord.Member):
    if user.bot:
        await interaction.response.send_message("Du kannst nicht gegen einen Bot spielen.", ephemeral=True)
        return

    if user == interaction.user:
        await interaction.response.send_message("Du kannst nicht gegen dich selbst spielen.", ephemeral=True)
        return

    # Initialisieren des Spiels mit beiden Spielern
    view = RPSView(interaction.user, user)
    await interaction.response.send_message(
        f"{interaction.user.mention} fordert {user.mention} zu Schere, Stein, Papier heraus!",
        view=view
    )

bot.run(token)
