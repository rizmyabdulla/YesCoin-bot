import requests
import time
from colorama import Fore, Style, init
import json
import sys

init(autoreset=True)


def print_welcome_message():
    print(Fore.GREEN + Style.BRIGHT + """
##  ##   ### ###   ## ##    ## ##    ## ##     ####   ###  ##           ### ##    ## ##   #### ##  
##  ##    ##  ##  ##   ##  ##   ##  ##   ##     ##      ## ##            ##  ##  ##   ##  # ## ##  
##  ##    ##      ####     ##       ##   ##     ##     # ## #            ##  ##  ##   ##    ##     
 ## ##    ## ##    #####   ##       ##   ##     ##     ## ##             ## ##   ##   ##    ##     
  ##      ##          ###  ##       ##   ##     ##     ##  ##            ##  ##  ##   ##    ##     
  ##      ##  ##  ##   ##  ##   ##  ##   ##     ##     ##  ##            ##  ##  ##   ##    ##     
  ##     ### ###   ## ##    ## ##    ## ##     ####   ###  ##           ### ##    ## ##    ####    
          """)
    print(Fore.GREEN + Style.BRIGHT + "YesCoin BOT (ULTIMATE EDITION)")
    print(Fore.GREEN + Style.BRIGHT + "Created by: TG @NotMrStrange")
# Load tokens from file
def load_tokens(file_path):
    with open(file_path, 'r') as file:
        tokens = file.read().splitlines()
    return tokens
available_colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
# Define headers
def get_headers(token):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.yescoin.gold',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.yescoin.gold/',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
# def get_daily_checkins(token):
#     url = 'https://api-backend.yescoin.gold/signIn/list'
#     headers = get_headers(token)

#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         if data['code'] == 0:
#             for checkin in data['data']:
#                 if checkin['status'] == 1:
#                     return checkin
#             return None
                    
#         else:
#             return None
#     except requests.exceptions.HTTPError as http_err:
#         print(f"HTTP error occurred: {http_err}")  # HTTP-specific error logging

# def daily_checkin(token):
#     url = 'https://api-backend.yescoin.gold/signIn/claim'
#     headers = get_headers(token)

#     checkin = get_daily_checkins(token)
#     current_timestamp = int(time.time())

#     headers.update({'tm': current_timestamp, 'sign': '403c6db2d041a4faba753f8544e4a990'})
#     payload = {
#         "id": checkin['id'],
#         "createAt": current_timestamp,
#         "signInType": checkin['signInType'],
#         "destination": ""
#     }

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()
#         data = response.json()

#         print(data)
#         if data['code'] == 0:
#             print(data)
#             print(f"{Fore.GREEN + Style.BRIGHT}\r[ Daily Check-in ] : Checked in successfully {data['message']}", flush=True)
#             return data
#         else:
#             return None
#     except requests.exceptions.HTTPError as http_err:
#         print(f"HTTP error occurred: {http_err}")  # HTTP-specific error logging
#         return None
#     except Exception as e:
#         print(f"Error checking in: {e}")
#         return None
    

def collect_coin(token, amount):
    url = 'https://api.yescoin.gold/game/collectCoin'
    headers = get_headers(token)
    data = json.dumps(amount)  # Ensure data is sent as JSON-encoded string
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        # print(result)
        if result['code'] == 0:
            return result
        else:
            # print(f"Error in response: {result}")  # Detailed error logging
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP-specific error logging
        # print(f"Response status code: {response.status_code}")
        # print(f"Response text: {response.text}")
        return None
    except Exception as e:
        print(f"Error collecting coins: {e}")
        return None

def claim_invite_bonus(token):
    url='https://api-backend.yescoin.gold/invite/claimGiftBox?packId=PDOKzA'
    headers = get_headers(token)
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            print(f"{Fore.YELLOW + Style.BRIGHT}-\{Fore.WHITE + Style.BRIGHT} {data['data']['claimAmount']} coins Claimed by Invitation! {Fore.YELLOW + Style.BRIGHT}/-", flush=True)
            return 
        else:
            return None
    except Exception as e:
        print(f"Error fetching invite bonus: {e}")
        return None


def get_invitation(token):
    url = 'https://api-backend.yescoin.gold/invite/getInviteGiftBoxInfoWithCode?inviteCode=PDOKzA'
    headers = get_headers(token)
    try:
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            print(f"{Fore.BLUE + Style.BRIGHT} \n -\{Fore.WHITE + Style.BRIGHT} Invited by {data['data']['userNick']} {Fore.BLUE + Style.BRIGHT}/-", flush=True)
            claim_invite_bonus(token)
        else:
            return None
    except Exception as e:
        print(f"Error fetching invite bonus: {e}")
        return None

def fetch_account_info(token):
    try:
        url = 'https://api.yescoin.gold/account/getAccountInfo'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching account info: {e}")

def fetch_game_info(token):
    try:
        url = 'https://api.yescoin.gold/game/getGameInfo'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching game info: {e}")

def use_special_box(token):
    url = 'https://api.yescoin.gold/game/recoverSpecialBox'
    headers = get_headers(token)
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            print(f"{Fore.GREEN + Style.BRIGHT}\r[ Chest ] : Activating...", end="", flush=True)
            return True
        else:
            print(f"{Fore.RED + Style.BRIGHT}\r[ Chest ] : Failed to activate", end="", flush=True)
            return False
    except Exception as e:
        print(f"{Fore.RED}\r[ Chest ] : Error", flush=True)
        return False
    
def fetch_special_box_info(token):
    try:
        url = 'https://api.yescoin.gold/game/getSpecialBoxInfo'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching special box info: {e}")


def get_my_user_nick(token):
    try:
        url = 'https://api.yescoin.gold/account/getRankingList?index=1&pageSize=1&rankType=1&userLevel=1'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if 'myUserNick' in data['data'] and data['data']['myUserNick']:
            return data['data']['myUserNick']
        else:
            return "no nickname"
    except Exception as e:
        print(f"Error fetching my user nick: {e}")


def collect_from_special_box(token, box_type, coin_count):
    url = 'https://api.yescoin.gold/game/collectSpecialBoxCoin'
    headers = get_headers(token)
    data = json.dumps({"boxType": box_type, "coinCount": coin_count})
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            if result['data']['collectStatus']:
                print(f"{random.choice(available_colors) + Style.BRIGHT}\r[ Chest ] : Collected {result['data']['collectAmount']} Coins                                                     ", flush=True)
          
                return True, result['data']['collectAmount']
            else:
                print(f"{Fore.RED + Style.BRIGHT}\r[ Chest ] : No chest Available          ", flush=True)
                return True, 0
        else:
            print(f"{Fore.RED + Style.BRIGHT}\r[ Chest ] : Failed to collect coins: {result['message']}", end="", flush=True)
            return False, 0
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}\r[ Chest ] : Error: {e}", flush=True)
        return False, 0

def attempt_collect_special_box(token, box_type, initial_coin_count):
    coin_count = initial_coin_count
    while coin_count > 0:
        success, collected_amount = collect_from_special_box(token, box_type, coin_count)
        if success:
            return collected_amount
        coin_count -= 20 
    print(f"{Fore.RED + Style.BRIGHT}\r[ Chest ] : Unable to collect any coins after adjustments", flush=True)
    return 0



def fetch_account_build_info(token):
    try:
        url = 'https://api.yescoin.gold/build/getAccountBuildInfo'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data['code'] == 0:
            # print(data)
            return data

        else:
            return None
        #     print(f"Failed to fetch account build info: {data['message']}")
    except Exception as e:
        print(f"Error fetching account build info: {e}")


def fetch_squad_info(token):
    url = 'https://api.yescoin.gold/squad/mySquad'
    headers = get_headers(token)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching squad info: {e}")
        return None
    
def recover_coin_pool(token):
    url = 'https://api.yescoin.gold/game/recoverCoinPool'
    headers = get_headers(token)
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Recovery ] : Successfully recovered {result['data']['recoverAmount']} coins.                ", flush=True)
            return True
        else:
            print(f"{Fore.RED + Style.BRIGHT}\r[ Recovery ] : Failed to recover coins!", flush=True)
            return False
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}\r[ Recovery ] : Error: {e}", flush=True)
        return False

def fetch_daily_missions(token):
    url = 'https://api-backend.yescoin.gold/mission/getDailyMission'
    headers = get_headers(token)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        missions = response.json()
        if missions['code'] == 0:
            return missions['data']
        else:
            print(f"{Fore.RED + Style.BRIGHT}\r[ Daily Mission ] : Failed to get Daily Mission list: {missions['message']}", flush=True)
            return None
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}Error: {e}")
        return None
    
def check_mission(token, mission_id):
    url = 'https://api-backend.yescoin.gold/mission/checkDailyMission'
    headers = get_headers(token)
    data = json.dumps(mission_id)
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
   
        if result['code'] == 0:
            print(f"{Fore.GREEN + Style.BRIGHT}\r[ Daily Mission ] : Checking Mission {mission_id}...", flush=True)
            return True
        elif result['message'] == 'secret code get lock failed':
            print(result)
            print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Daily Mission ] : Requesting again for {mission_id}...", flush=True)
            time.sleep(5)
        else:
            print(f"{Fore.RED + Style.BRIGHT}\r[ Daily Mission ] : Failed to check mission {mission_id}: {result['message']}", flush=True)
            return False
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}\r[ Daily Mission ] : Error: {e}", flush=True)
        return False
    
def claim_mission(token, mission_id):
    url = 'https://api-backend.yescoin.gold/mission/claimReward'
    headers = get_headers(token)
    data = json.dumps(mission_id)
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
   
        if result['code'] == 0:
            print(f"{Fore.GREEN + Style.BRIGHT}\r[ Daily Mission ] : Claiming Mission {mission_id}...", flush=True)
            print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Daily Mission ] : Claimed {result['data']['reward']} coins. {result['data']['score']} points added to your level.                ", flush=True)
            return True
        else:
            print(f"{Fore.RED + Style.BRIGHT}\r[ Daily Mission ] : Failed to claim mission {mission_id}: {result['message']}", flush=True)
            return False
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}\r[ Daily Mission ] : Error: {e}", flush=True)
        return False

def fetch_task_list(token):
    url = 'https://api.yescoin.gold/task/getCommonTaskList'
    headers = get_headers(token)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tasks = response.json()
        if tasks['code'] == 0:
            return tasks['data']
        else:
            print(f"{Fore.RED + Style.BRIGHT}\r[ Task ] : Failed to get task list: {tasks['message']}", flush=True)
            return None
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}Error: {e}")
        return None

def finish_task(token, task_id):
    url = 'https://api.yescoin.gold/task/finishTask'
    headers = get_headers(token)
    data = json.dumps(task_id)
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
   
        if result['code'] == 0:
            print(f"{Fore.GREEN + Style.BRIGHT}\r[ Task ] : Task {task_id} finished. Bonus: {result['data']['bonusAmount']}", flush=True)
            return True
        else:
            # print(result)
            print(f"{Fore.RED + Style.BRIGHT}\r[ Task ] : Failed to finish task {task_id}: {result['message']}", flush=True)
            return False
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}\r[ Task ] : Error: {e}", flush=True)
        return False

def process_tasks(token):
    tasks = fetch_task_list(token)
    if tasks:
        for task in tasks:
            if task['taskStatus'] == 0:
                finish_task(token, task['taskId'])
            else:
                print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Task ] : Task already finished          ", flush=True)

def process_daily_missions(token):
    missions = fetch_daily_missions(token)
    if missions:
        for mission in missions:
            if mission['missionStatus'] == 0 and check_mission(token, mission['missionId']):
                time.sleep(5)
                claim_mission(token, mission['missionId'])
            else:
                print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Daily Mission ] : Mission already finished          ", flush=True)


import random
def upgrade_level(token, current_level, target_level, upgrade_type):

    url = 'https://api.yescoin.gold/build/levelUp'
    headers = get_headers(token)
    data = json.dumps(upgrade_type)
    if upgrade_type == '1':
            upgrade_type_name = 'Multi Value'
    else:
        upgrade_type_name = 'Fill Rate'
    while current_level < target_level:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
       
        if result['code'] == 0:
            current_level += 1
            print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Upgrade ] : {upgrade_type_name} Upgrade to {current_level}            ", flush=True)
        else:
            print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Upgrade ] : Failed to upgrade: {result['message']}        ", flush=True)
            break

    if current_level == target_level:
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Upgrade ] : {upgrade_type_name} already at level {current_level}          ", flush=True)

def get_token_from_payload(payload):
    url = 'https://api-backend.yescoin.gold/user/login'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.yescoin.gold',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.yescoin.gold/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    data = json.dumps({"code": payload})
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    result = response.json()
    if result['code'] == 0:
        return result['data']['token']
    else:
        raise Exception("Failed to get token")
    

import urllib.parse


def process_account(token):
    nickname = get_my_user_nick(token)
    print(f"{Fore.BLUE + Style.BRIGHT}\n========[{Fore.WHITE + Style.BRIGHT} Account | {nickname} {Fore.BLUE + Style.BRIGHT}]========")
    get_invitation(token)
    print(f"{random.choice(available_colors)+Style.BRIGHT}\n \r[ Squad ] : Getting...", end="", flush=True)
    squad_info = fetch_squad_info(token)
    if squad_info and squad_info['data']['isJoinSquad']:
        squad_title = squad_info['data']['squadInfo']['squadTitle']
        squad_members = squad_info['data']['squadInfo']['squadMembers']
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Squad ] : {squad_title} | {squad_members} Members")
    else:
        print(f"{Fore.YELLOW + Style.BRIGHT}\r[ Squad ] : Not in a squad", end="", flush=True)
        time.sleep(3)

    print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Profile Info ] : Getting...", end="", flush=True)
    profile_info = fetch_account_info(token)
    if profile_info is None:
        print(f"{Fore.RED}\r[ Profile Info ] : Failed to get profile info", flush=True)
        return
    else:
        profile_rank = profile_info.get('data', {}).get('levelInfo', {}).get('rankName', '')
        profile_level = profile_info.get('data', {}).get('levelInfo', {}).get('level', 0)
        balance = profile_info.get('data', {}).get('currentAmount', 0)
        print(f"{random.choice(available_colors) + Style.BRIGHT}\r[ Profile Info ] : Your Rank - {profile_rank} | level - {profile_level}          ", flush=True)
        print(f"{random.choice(available_colors) + Style.BRIGHT}\r[ Profile Info ] : Balance - {balance}           ", flush=True)
    
    # get_daily_checkin = get_daily_checkins(token)
    # if get_daily_checkin is None:
    #     print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Daily Check-in ] : Already checked in for today!", flush=True)
    # else:
    #     print(get_daily_checkin, flush=True)
    #     print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Daily Check-in ] : Checking in for {get_daily_checkin['name']}...", flush=True)
        # daily_checkin(token)

    #time.sleep(2)

    print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Game Info ] : Getting...", end="", flush=True)
    game_info = fetch_account_build_info(token)
    if game_info is None:
        print(f"{Fore.RED}\r[ Game Info ] : Failed to get data", flush=True)
        return
    else:
        special_box_left_recovery_count = game_info['data'].get('specialBoxLeftRecoveryCount', 0)
        coin_pool_left_recovery_count = game_info['data'].get('coinPoolLeftRecoveryCount', 0)
        single_coin_value = game_info['data'].get('singleCoinValue', 0)
        single_coin_level = game_info['data'].get('singleCoinLevel', 0)
        coin_pool_recovery_speed = game_info['data'].get('coinPoolRecoverySpeed', 0)
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Booster ] : Chest {special_box_left_recovery_count} | Recovery {coin_pool_left_recovery_count}", flush=True)
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Multivalue ] : Level {single_coin_value}", flush=True)
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Coin Limit ] : Level {single_coin_level}", flush=True)
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Fill Rate ] : Level {coin_pool_recovery_speed}", flush=True)

    if check_task_enable == 'y':
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Task ] : Trying to finish task..", end="", flush=True)
        process_tasks(token)
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Daily Mission ] : Trying to finish daily mission..", end="", flush=True)
        process_daily_missions(token)
    time.sleep(2)
    if upgrade_multi_enable == 'y':
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Upgrade ] : Upgrading Multi Value...", end="", flush=True)
        upgrade_level(token, single_coin_value, max_level, '1')
    time.sleep(2)
    if upgrade_fill_enable == 'y':
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Upgrade ] : Upgrading Fill Rate...", end="", flush=True)
        upgrade_level(token, coin_pool_recovery_speed, max_level, '2')
    
    print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Game Info ] : Getting...", end="", flush=True)
    collect_info = fetch_game_info(token)
    if collect_info is None:
        print(f"{Fore.RED}\r[ Game Info ] : Failed to get data", flush=True)
        return
    else:
        single_coin_value = collect_info['data'].get('singleCoinValue', 0)
        coin_pool_left_count = collect_info['data'].get('coinPoolLeftCount', 0)
        print(f"{random.choice(available_colors) + Style.BRIGHT}\r[ Coin Left ] : {coin_pool_left_count}                              ", flush=True)
        
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Collect ] : Collecting Coin...", end="", flush=True)
        if coin_pool_left_count > 0:
            amount =  coin_pool_left_count // single_coin_value
            collect_result = collect_coin(token, amount)
            if collect_result and collect_result.get('code') == 0:
                collected_amount = collect_result['data']['collectAmount']
                print(f"{random.choice(available_colors) + Style.BRIGHT}\r[ Collect ] : Collected {random.choice(available_colors)+Style.BRIGHT}{collected_amount}                                                  ", flush=True)
            else:
                print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Collect ] : Failed to collect coins", flush=True)
    
    print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Chest ] : Trying to activate...", end="", flush=True)
    if game_info and game_info['data'].get('specialBoxLeftRecoveryCount', 0) > 0:
        if use_special_box(token):
            print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Chest ] : Collecting...", end="", flush=True)
            collected_amount = attempt_collect_special_box(token, 2, 240) 
    else:
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Chest ] : No chest available          ", flush=True)
    time.sleep(2)
    print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Recovery ] : Trying to recover...", end="", flush=True)
    game_info = fetch_account_build_info(token)
    if game_info and game_info['data'].get('coinPoolLeftRecoveryCount', 0) > 0:
        if recover_coin_pool(token):
            collect_info = fetch_game_info(token)
            if collect_info:
                coin_pool_left_count = collect_info['data'].get('coinPoolLeftCount', 0)
                if coin_pool_left_count > 0:
                    amount = coin_pool_left_count // game_info['data'].get('singleCoinValue', 1)
                    collect_result = collect_coin(token, amount)
                    if collect_result and collect_result.get('code') == 0:
                        collected_amount = collect_result['data']['collectAmount']
                        print(f"{Fore.GREEN + Style.BRIGHT}\r[ Collect ] : Collected successfully {collected_amount} koin", flush=True)
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}\r[ Collect ] : Failed to collect coins", flush=True)
    else:
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Recovery ] : No recovery available", flush=True)
    time.sleep(2)
    print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Free Chest ] : Trying to collect..", end="", flush=True)
    collected_amount = attempt_collect_special_box(token, 1, 200) 
    time.sleep(2)

def main():
    print_welcome_message()
    while True:
        try:
            with open('query.txt', 'r') as file:
                queries = file.readlines()
                
                if not queries:
                    print("\nEDIT THE query.txt FILE AND TRY AGAIN!")
                    print("Exiting...")
                    print("\n")
                    exit(1)
            
            for query_string in queries:
                query_string = query_string.strip()
                if not query_string:
                    continue
                
                # Parse and decode the query string
                parsed_query = urllib.parse.unquote(query_string)
                payload = f"user={parsed_query}"

                try:
                    token = get_token_from_payload(payload)
                    process_account(token)
                except Exception as e:
                    print(f"Error processing account: {e}")

            print(f"\n{random.choice(available_colors)+Style.BRIGHT}========={Fore.WHITE+Style.BRIGHT}All accounts have been successfully processed{Fore.GREEN+Style.BRIGHT}=========", end="", flush=True)
            waiting_time = 15
            for detik in range(waiting_time, 0, -1):
                sys.stdout.write(f"\r{Fore.CYAN}Waiting for the next claim time in {Fore.CYAN}{Fore.WHITE}{detik // 60} Minutes {Fore.WHITE}{detik % 60} Seconds")
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write("\rThe next claim time has arrived!                                                          \n")
        except (Exception, requests.ConnectionError, requests.JSONDecodeError) as e:
            print(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
            pass
        except KeyboardInterrupt:
            print(f"{Fore.RED + Style.BRIGHT}[ See You 👋🏻 ]{Style.RESET_ALL}")
            sys.exit(0)  

            
import argparse    
def parse_arguments():
    parser = argparse.ArgumentParser(description='Blum BOT')
    parser.add_argument('--task', type=str, choices=['y', 'n'], help='Check and Claim Task (y/n)')
    parser.add_argument('--multi', type=str, choices=['y', 'n'], help='Upgrade Multi Value (y/n)')
    parser.add_argument('--fill', type=str, choices=['y', 'n'], help='Upgrade Fill Rate (y/n)')
    parser.add_argument('--max-level', type=int, help='Maximum level for upgrade (default: 5)')
    
    args = parser.parse_args()

    if args.task is None:
        task_input = input("Do you want to check and claim tasks? (y/n, default n): ").strip().lower()
        args.task = task_input if task_input in ['y', 'n'] else 'n'
    
    if args.multi is None:
        multi_input = input("Do you want a multi value upgrade? (y/n, default n): ").strip().lower()
        args.multi = multi_input if multi_input in ['y', 'n'] else 'n'
    
    if args.fill is None:
        fill_input = input("Do you want to upgrade the fill rate? (y/n, default n): ").strip().lower()
        args.fill = fill_input if fill_input in ['y', 'n'] else 'n'
    
    if (args.multi == 'y' or args.fill == 'y') and args.max_level is None:
        max_level_input = input("Enter the maximum level to upgrade (default: 5): ").strip()
        args.max_level = int(max_level_input) if max_level_input else 5
    elif args.max_level is None:
        args.max_level = 5  # Default value if max_level is not provided and neither multi nor fill is 'y'
    
    return args

args = parse_arguments()
check_task_enable = args.task
upgrade_multi_enable = args.multi
upgrade_fill_enable = args.fill
max_level = args.max_level


if __name__ == '__main__':
    main()
