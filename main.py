import discord 
import os
from discord.ext import commands, tasks
from music import *
from quotes import *
import random
import asyncio
import time

client = commands.Bot(command_prefix='.')

@client.event 
async def on_ready():
    print("logged in as {0.user}".format (client))

@client.command(pass_context=True)
async def hello(ctx, *args):
    await ctx.send("Hello! Are you ready to start studying?")

@client.command(pass_context=True)
async def music(ctx, *args):
    await ctx.send("**Music:** \nGrab some headphones and listen! \n" + random.choice(random_music))

@client.command(pass_context=True)
async def inspire(ctx, *args):
    await ctx.send(random.choice(random_quotes))


@client.command(pass_context=True)
async def pomodoro(ctx, *args):

    smallBreaks = 1
    workTime = 25 * 60
    smallBreakTime = 5 * 60 
    longBreakTime = 30 * 60

    if len(args) != 3:
        await ctx.send("Invalid arguments. Usage: .pomodoro [work time] [small break time] [long break time]")
        return

    if (not isinstance(int(args[0]), int)) or (not isinstance(int(args[1]), int)) or (not isinstance(int(args[2]), int)):
        await ctx.send("Invalid arguments. Usage: .pomodoro [work time] [small break time] [long break time]")
        return

    workTime = int(args[0]) 
    smallBreakTime = int(args[1]) 
    longBreakTime = int(args[2]) 

    for i in range(1, 5):
        t = time.time()
        await ctx.send(f"**Pomodoro:** \n{i}/4 work cycles in progress, keep going <@{ctx.author.id}>. \nNext break at {time.strftime('%I:%M:%S %p', time.localtime(t + workTime))}.")
        time.sleep(workTime)
        if i != 4:
            await ctx.send(f"**Pomodoro:** \nGood job <@{ctx.author.id}>! \nTake a small break, start working at {time.strftime('%I:%M:%S %p', time.localtime(t + workTime + smallBreakTime))}.")
        time.sleep(smallBreakTime)

    await ctx.send(f"**Pomodoro:** \n4/4 work cycles completed. \nCongrats! \nTake a break, <@{ctx.author.id}>, you earned it!.")


@client.command()
async def remind(ctx, message=None, *args):
    remindTime = int(args[0])
    t = time.time()
    await ctx.send(f"**Reminder:** \n<@{ctx.author.id}>, you will be reminded at {time.strftime('%I:%M:%S %p', time.localtime(t + remindTime))}. \nFor: {message}.")
    time.sleep(remindTime)
    await ctx.send(f"**Reminder:** \n<@{ctx.author.id}>, you need to do {message} starting now! \nGood luck! :)")

goals_lst = []

@client.command()
async def setgoal(ctx, message):
    goals_lst.append(message)
    await ctx.send(f"**Set Goal:** \n<@{ctx.author.id}>, your goal, **{message}**, has been logged. \nUse '.goals' to view all your goals. \nUse '.complete <goal number>' to complete/delete a goal.")
    if len(goals_lst) != 0:
        time.sleep(20)
        await ctx.send(f"**Goal Reminder:** \n<@{ctx.author.id}>, have you completed any goals? \nUse '.complete <goal number>' to clear it from your list.")

@client.command()
async def goals(ctx, *args): 
    message = f"**<@{ctx.author.id}>'s Goals:** \n"
    for i in range(len(goals_lst)):
        message += '**' + str(i + 1) + ". **" + goals_lst[i] + "\n"

    await ctx.send(message)
    

@client.command()
async def complete(ctx, num):
    del goals_lst[int(num) - 1]
    if len(goals_lst) != 0:
        await ctx.send("Great job! \nKeep at it and complete the rest of your goals! :)")
        message = f"**<@{ctx.author.id}>'s Remaining Goals:** \n"
        for i in range(len(goals_lst)):
            message += f"**{str(i + 1)}. **{str(goals_lst[i])}\n"
        await ctx.send(message)
        
    else:
        await ctx.send(f"Congrats <@{ctx.author.id}>! \nYou completed all your goals for today! :)")

start_time = None
@client.command()
async def study(ctx, message):
    global start_time 
    if start_time != None:
        return
    await ctx.send(f"**Studying:** \nYour timer for **{message}** has started. \nUse '.stop' to stop the timer. \nOnce you reach 2 hours of studying you'll gain the 'starter' role!")
    start_time = time.time()

@client.command()
async def stop(ctx, *args):
    global start_time
    end_time = time.time()
    time_elapsed = end_time - start_time
    start_time = None
    print(time_elapsed)
    await ctx.send(f"**Studying:** \nGood job! \nYou studied for {time.strftime('%M:%S', time.localtime(time_elapsed))}")
    if time_elapsed >= 2:
        member = ctx.author
        role = discord.utils.get(member.guild.roles, name="starter")
        await member.add_roles(role)
        await ctx.send(f"**Level Up:** \n<@{ctx.author.id}>, you have gained the 'starter' role. \nContinue studying to earn more! :)")

@client.command(pass_context=True)
async def bye(ctx, *args):
    await ctx.send("Logging off... \nGreat job today! :D")

client.run('ODE0OTYwMzU0MDU1NDIxOTgy.YDlc-Q.4xUdKHkZoOYs85E2qsOqKGvsE0M')