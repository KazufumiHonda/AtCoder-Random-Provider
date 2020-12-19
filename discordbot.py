import discord
import json
from collections import OrderedDict
import random
import sys
import requests
import pprint
import os

#TOKEN_PATH = './token.txt'

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
DEBUG_FLAG = False
contest_max_abc = 0
contest_max_arc = 0
contest_max_agc = 0

client = discord.Client()

data = ''
help = "AtCoderの問題(ABC,ARC,AGC)を無作為に1問返します\n〇使い方\nメンションする\n@AtCoder Random Problem Provider\n〇引数で難易度(difficulty)指定も可能です\n・数値指定\n@AtCoder Random Problem Provider  (difficultyの下限)  (difficultyの上限)\n・色指定\n@AtCoder Random Problem Provider  色\n各色のdiffに対する引数は以下の通りです\n灰diff：灰 または GRY\n茶diff：茶 または BRN\n緑diff：緑 または GRN\n水diff：水 または AQU\n青diff：青 または BLU\n黃diff：黃 または YEL\n赤diff：赤 または RED\n銀diff：銀 または SIL\n金diff：金 または GLD\n"


def get_atcoder_problems_api():
  global data
  resp = requests.get('https://kenkoooo.com/atcoder/resources/problem-models.json')
#  print(resp.status_code)
  json_load = resp.json()
  data = resp.json()

def get_atcoder_problems_api_locally():
  global data
  path = './problem-models.json'
  f = open(path, 'r')
  data = json.load(f)

def get_token():
  global TOKEN
  token_file = open(TOKEN_PATH, 'r')
  TOKEN = token_file.read()
  token_file.close()

def set_contest_num_max():
  global contest_max_abc,contest_max_arc,contest_max_agc
  global data
  for d in data.keys():
    s_contest = d[0:3]
    if s_contest == 'abc':
      s_num = d[3:6]
      contest_max_abc = max(contest_max_abc,int(s_num))
    elif s_contest == 'arc':
      s_num = d[3:6]
      contest_max_arc = max(contest_max_arc,int(s_num))
    elif s_contest == 'agc':
      s_num = d[3:6]
      contest_max_agc = max(contest_max_agc,int(s_num))
  """
  print('abc',contest_max_abc)
  print('arc',contest_max_arc)
  print('agc',contest_max_agc)
  """

def get_contest_kind():
  n = random.randint(1,10000)
  div = 6
  brg = n%div
  log(brg)

  contest_kind = 'a'
  if brg == 0:
    contest_kind += 'g'
  elif brg == 1 or brg == 2 :
    contest_kind += 'r'
  else:
    contest_kind += 'b'
  contest_kind += 'c'
  return contest_kind

def get_contest_number(kind):
  contest_num = 0
  if kind == 'abc':
    contest_num = random.randint(1,contest_max_abc)
  elif kind == 'arc':
    contest_num = random.randint(1,contest_max_arc)
  else:
    contest_num = random.randint(1,contest_max_agc)
  contest_num_string = str(contest_num)
  contest_num_string = contest_num_string.zfill(3)
  return contest_num_string

def get_problem_number():
  n = random.randint(0,5)
  problem_number = chr(ord('a')+n)
  return problem_number


def get_url(c_str,p_str):
  url = 'https://atcoder.jp/contests/' + c_str + '/tasks/' + p_str
  return url

def log(str):
  if DEBUG_FLAG == True:
    print(str)

def error(str):
  print(str)
  #sys.exit()

def generate(message):
#  global data
  """
  path = './problem-models.json'

  f = open(path, 'r')

  json_load = json.load(f)
  """

  json_load = data

  print(message.content)
#  args = sys.argv
  args = message.content.split()
  """
  log('args')
  for arg in args:
    log(arg)
  log('')
  """


  lower = -10000
  upper = 10000

  if len(args) >= 2:
    if args[1] == 'help' or args[1] == 'ヘルプ':
      return help

    if args[1] != 'def':
      if args[1] == 'GRY' or args[1] == '灰':
        upper = 399
      elif args[1] == 'BRN' or args[1] == '茶':
        lower = 400
        upper = 799
      elif args[1] == 'GRN' or args[1] == '緑':
        lower = 800
        upper = 1199
      elif args[1] == 'AQU' or args[1] == '水':
        lower = 1200
        upper = 1599
      elif args[1] == 'BLU' or args[1] == '青':
        lower = 1600
        upper = 1999
      elif args[1] == 'YEL' or args[1] == '黃':
        lower = 2000
        upper = 2399
      elif args[1] == 'ORN' or args[1] == '橙':
        lower = 2400
        upper = 2799
      elif args[1] == 'RED' or args[1] == '赤':
        lower = 2800
        upper = 3199
      elif args[1] == 'SIL' or args[1] == '銀':
        lower = 3200
        upper = 3599
      elif args[1] == 'GLD' or args[1] == '金':
        lower = 3600
      else:
        if args[1].isdecimal():
          lower = int(args[1])
    if len(args) >= 3:
      if args[2] != 'def':
        if args[2].isdecimal():
          upper = int(args[2])

  if lower > upper:
    error('difficulty setting error')
    return

  log('lower limit:'+str(lower))
  log('upper limit:'+str(upper))

  s = ''
  sc = ''
  search_count = 0
  search_limit = 1000
  search_flag = False
  while search_count < search_limit:
    sc = get_contest_kind()
    sc += get_contest_number(sc)
    sn = get_problem_number()
    s = sc + '_' + sn
    if s in json_load:
      difficulty = json_load[s].get('difficulty','not found')
      if difficulty == 'not found':
        log('difficulty not found')
        continue
      if lower <= difficulty and difficulty <= upper:
        print(json_load[s]['difficulty'])
        break
    else:
      log('problem not found')
    search_count += 1
    if search_count == search_limit:
      search_flag = True

  log('')

  #f.close()

  if search_flag:
    return ''

  url = get_url(sc,s)
  print(url)

  return url


# 起動時に動作する処理
@client.event
async def on_ready():
    print('started correctly')

async def reply(message):
#    reply = f'{message.author.mention} called?'
    url = generate(message)
    #reply = f'{message.author.mention} '
    #reply += url
    reply = url
    if reply != '':
      await message.channel.send(reply)

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
#    if message.author.bot:
#        return

    if client.user in message.mentions:
        await reply(message)

#    if message.content == '/neko':
#        await message.channel.send('にゃーん')

def main():
  #get_atcoder_problems_api()
  get_atcoder_problems_api_locally()
  #get_token()
  set_contest_num_max()
  # Botの起動とDiscordサーバーへの接続
  client.run(TOKEN)

if __name__ == '__main__':
  main()

