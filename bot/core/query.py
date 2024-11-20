import asyncio
import json
from itertools import cycle
import sys
from time import time
import aiohttp
import cloudscraper
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from bot.core.agents import generate_random_user_agent
from bot.config import settings

from bot.utils import logger
from bot.exceptions import InvalidSession
from .headers import headers
from random import uniform
import random
import hashlib
import urllib.parse

endpoint = "https://bi.yescoin.gold/"


class Tapper:
    def __init__(self, query: str, session_name: str, multi_thread: bool):
        self.query = query
        self.session_name = session_name
        self.auth_token = ""
        self.multi_thread = multi_thread
        self.balance = 0
        self.my_ref = "PDOKzA"

    @staticmethod
    def generate_hash(id: str, claim_type: int = 1):
        t = int(time())
        input_string = str(id) + str(t) + "6863b339db454f5bbd42ffb5b5ac9841" + str(claim_type)
        sign = hashlib.md5(input_string.encode()).hexdigest()
        return t, sign, claim_type

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy):
        try:
            response = await http_client.get(url='https://ipinfo.io/json', timeout=aiohttp.ClientTimeout(20))
            response.raise_for_status()

            response_json = await response.json()
            ip = response_json.get('ip', 'NO')
            country = response_json.get('country', 'NO')

            logger.info(f"{self.session_name} |🟩 Logging in with proxy IP {ip} and country {country}")
            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")
            return False

    async def get_token(self, http_client: cloudscraper.CloudScraper, retry=3):
        if retry == 0:
            return None
        
        try:
            query_string = self.query.strip()
                
            parsed_query = urllib.parse.unquote(query_string)
            payload = {"code": parsed_query}

            get_token = http_client.post(f"{endpoint}user/login", json=payload)
            if get_token.status_code == 200 and get_token.json().get("code") == 0:
                res = get_token.json()
                data = res['data']

                self.auth_token = data["token"]
                logger.success(f"{self.session_name} | <green>Successfully logged in!</green>")
            else:
                logger.warning(
                    f"{self.session_name} | <yellow>Failed to login: {get_token.status_code}. Query is invalid! retry in 3-5 seconds</yellow>")
                await asyncio.sleep(random.randint(3, 5))
                await self.get_token(http_client, retry - 1)
        except Exception as e:
            # traceback.print_exc()
            logger.error(f"{self.session_name} | Unknown error while trying to login: {e}")


    def process_invitation(self, httpClient: cloudscraper.CloudScraper):
        try:
            invitation = httpClient.get(f"{endpoint}invite/getInviteGiftBoxInfoWithCode?inviteCode={self.my_ref}")
            if invitation.status_code == 200 and invitation.json().get("code") == 0:
                res = invitation.json()
                if res['code'] == 0:
                    claim_invitation = httpClient.post(f"{endpoint}invite/claimGiftBox?packId={self.my_ref}")
                    if claim_invitation.status_code == 200 and claim_invitation.json().get("code") == 0:
                        logger.success(f"{self.session_name} | <green>Successfully claimed invite bonus</green>")
                    else:
                        return False
            else:
                return None
        except Exception as e:
            return None

    def fetch_account_info(self, http_client: cloudscraper.CloudScraper):
        try:
            account_info = http_client.get(f"{endpoint}account/getAccountInfo")
            if account_info.status_code == 200 and account_info.json().get("code") == 0:
                res = account_info.json()
                data = res['data']
                return data
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to fetch account info: {account_info.status_code}</yellow>")
                return None
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to fetch account info: {e}")
            return None
    
    def fetch_build_info(self, http_client: cloudscraper.CloudScraper):
        try:
            build_info = http_client.get(f"{endpoint}build/getAccountBuildInfo")
            res = build_info.json()
            if build_info.status_code == 200 and res.get("code") == 0:
                data = res.get("data")
                return data
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to fetch build info: {build_info.status_code}</yellow>")
                return None
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to fetch build info: {e}")
            return None

    def fetch_game_info(self, http_client: cloudscraper.CloudScraper):
        try:
            game_info = http_client.get(f"{endpoint}game/getGameInfo")
            if game_info.status_code == 200 and game_info.json().get("code") == 0:
                res = game_info.json()
                data = res['data']
                return data
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to fetch game info: {game_info.status_code}</yellow>")
                return None
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to fetch game info: {e}")
            return None
    
    def update_balance(self, http_client: cloudscraper.CloudScraper):
        account_info = self.fetch_account_info(http_client)
        if account_info is None:
            return False
        self.balance = account_info['currentAmount']
        return True
    
    def get_checkin(self, http_client: cloudscraper.CloudScraper):
        try:
            get_checkin = http_client.get(f"{endpoint}signIn/list")
            res = get_checkin.json()
            if get_checkin.status_code == 200 and res.get("code") == 0:
                for checkin in res['data']:
                    if checkin['status'] == 1:
                        return checkin
                return None
                        
            else:
                return None
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to get check-in: {e}")
            return None
    
    async def process_checkin(self, http_client: cloudscraper.CloudScraper):
        checkin = self.get_checkin(http_client)
        await asyncio.sleep(random.uniform(1, 3))

        if checkin is None:
            return False
        checkin_id = checkin['id']
        checkin_name = checkin['name']

        tm, sign, type = self.generate_hash(str(checkin_id))
        payload = json.dumps({"id": checkin_id,"createAt": tm, "signInType": type, "destination": ""})
        http_client.headers.update({'tm': str(tm), 'sign': str(sign)})
        try:
            
            checkin_res = http_client.post(f"{endpoint}signIn/claim", data=payload)
            res = checkin_res.json()
            if checkin_res.status_code == 200:
                if res.get("code") == 0:
                    logger.success(f"{self.session_name} | <green>Successfully claimed check-in {checkin_name}: Claimed <cyan>{res.get('data').get('reward')}</cyan> coins</green>")
                    self.update_balance(http_client)
                    return True
                else:
                    logger.warning(f"{self.session_name} | <yellow>Failed to claim check-in: {res.get('message')}</yellow>")
                    return False
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to claim check-in: {checkin_res.status_code}</yellow>")
                return False
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to process check-in: {e}")
            return False

    def offline_bonus(self, http_client: cloudscraper.CloudScraper):
        try:
            offline_bonus = http_client.get(f"{endpoint}game/getOfflineYesPacBonusInfo")
            res = offline_bonus.json()

            if offline_bonus.status_code == 200:
                if res.get("code") == 0:
                    data = res.get("data")
                    return data
                else:
                    return None
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to get offline bonus: {e}")
            return None
    
    def process_offline_bonus(self, http_client: cloudscraper.CloudScraper):
        offline_bonus = self.offline_bonus(http_client)
        if offline_bonus is None:
            return False
        offline_bonus_id = offline_bonus[1]['transactionId']
        tm, sign, type = self.generate_hash(str(offline_bonus_id))
        payload = json.dumps({"id": offline_bonus_id, "createAt": tm, "destination": "", "claimType": 2})
        http_client.headers.update({'tm': str(tm), 'sign': str(sign)})
        try:
            offline_bonus_res = http_client.post(f"{endpoint}game/claimOfflineBonus", data=payload)
            res = offline_bonus_res.json()
            if offline_bonus_res.status_code == 200:
                if res.get("code") == 0:
                    logger.success(f"{self.session_name} | <green>Successfully claimed offline bonus: {offline_bonus_id}: Claimed <cyan>{res.get('data').get('collectAmount')}</cyan> coins</green>")
                    self.update_balance(http_client)
                    return True
                else:
                    logger.warning(f"{self.session_name} | <yellow>Failed to claim offline bonus: {res.get('message')}</yellow>")
                    return False
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to claim offline bonus: {e}")
            return False
        
    def collect_coin(self, http_client: cloudscraper.CloudScraper, amount: int):
        try:
            payload = json.dumps(amount)
            collect_coin = http_client.post(f"{endpoint}game/collectCoin", json=payload)
            res = collect_coin.json()
            if collect_coin.status_code == 200:
                if res.get("code") == 0:
                    logger.success(f"{self.session_name} | <green>Successfully collected <cyan>{amount}</cyan> coins</green>")
                    self.update_balance(http_client)
                    return True
                else:
                    logger.warning(f"{self.session_name} | <yellow>Failed to collect <cyan>{amount}</cyan> coins: {res.get('message')}</yellow>")
                    return False
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to collect <cyan>{amount}</cyan> coins: {collect_coin.status_code}</yellow>")
                return False
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to collect coin: {e}")
            return False
        

    def collect_special_box(self, http_client: cloudscraper.CloudScraper, box_type: int, coin_amount: int):
        try:
            while coin_amount > 0:
                payload = {"boxType": box_type, "coinCount": coin_amount}
                collect_special_box = http_client.post(f"{endpoint}game/collectSpecialBoxCoin", json=payload)
                res = collect_special_box.json()
                if collect_special_box.status_code == 200:
                    if res.get("code") == 0:
                        logger.success(f"{self.session_name} | <green>Successfully collected <cyan>{res.get('data').get('collectAmount')} coins</cyan></green>")
                        self.update_balance(http_client)
                        # coin_amount -= res.get("data").get("collectAmount")
                        coin_amount -= 20
                        return True
                    else:
                        logger.warning(f"{self.session_name} | <yellow>Failed to collect special box: {res.get('message')}</yellow>")
                        return False
                else:
                    logger.warning(f"{self.session_name} | <yellow>Failed to collect <cyan>{coin_amount}</cyan> coins: {collect_special_box.status_code}</yellow>")
                    return False
            logger.success(f"{self.session_name} | <green>Successfully collected <cyan>{coin_amount}</cyan> coins</green>")
            return True
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to collect special box: {e}")
            return False
        
    def refresh_special_box(self, http_client: cloudscraper.CloudScraper):
        try:
            refresh_special_box = http_client.post(f"{endpoint}game/specialBoxReloadPage")
            if refresh_special_box.status_code == 200:
                if refresh_special_box.json().get("code") == 0:
                    return True
                else:
                    return False
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to refresh special box: {e}")
            return False
        
    def fetch_special_box(self, http_client: cloudscraper.CloudScraper):
        try:
            special_box = http_client.get(f"{endpoint}game/getSpecialBoxInfo")
            res = special_box.json()
            if special_box.status_code == 200:
                if res.get("code") == 0:
                    data = res.get("data")
                    return data
                else:
                    return None
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to fetch special box: {e}")
            return None
        
    def recover_special_box(self, http_client: cloudscraper.CloudScraper):
        try:
            recover_special_box = http_client.post(f"{endpoint}game/recoverSpecialBox")
            if recover_special_box.status_code == 200:
                if recover_special_box.json().get("code") == 0:
                    logger.success(f"{self.session_name} | <green>Successfully recovered special box</green>")
                    return True
                else:
                    logger.warning(f"{self.session_name} | <yellow>Failed to recover special box: {recover_special_box.json().get('message')}</yellow>")
                    return False
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to recover special box: {e}")
            return False
    
    def recover_coin_pool(self, http_client: cloudscraper.CloudScraper):
        try:
            recover_coin_pool = http_client.post(f"{endpoint}game/recoverCoinPool")
            if recover_coin_pool.status_code == 200:
                if recover_coin_pool.json().get("code") == 0:
                    logger.success(f"{self.session_name} | <green>Successfully recovered coin pool</green>")
                    return True
                else:
                    logger.warning(f"{self.session_name} | <yellow>Failed to recover coin pool: {recover_coin_pool.json().get('message')}</yellow>")
                    return False
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to recover coin pool: {e}")
            return False
        

    async def upgrade_level(self, http_client: cloudscraper.CloudScraper, maxUpgrade: int = 15):
        level_info = self.fetch_build_info(http_client)
        level_data = level_info

        upgrade_data = {
            1: {
                "name": "Multi value",
                "currentLevel": level_data['singleCoinValue'],
                "maxLevel": 15,
                "upgradeCost": level_data['singleCoinUpgradeCost']
            },
            2: {
                "name": "Fill rate",
                "currentLevel": level_data['coinPoolRecoverySpeed'],
                "maxLevel": 15,
                "upgradeCost": level_data['coinPoolRecoveryUpgradeCost']
            },
            3: {
                "name": "Coin limit",
                "currentLevel": level_data['singleCoinLevel'],
                "maxLevel": 15,
                "upgradeCost": level_data['coinPoolTotalUpgradeCost']
            },
            4: {
                "name": "Yes Pack",
                "currentLevel": level_data['swipeBotLevel'],
                "maxLevel": 5,
                "upgradeCost": level_data['swipeBotUpgradeCost']
            }
        }

        try:
            self.update_balance(http_client)

            yes_pack = upgrade_data[4]
            if yes_pack["currentLevel"] < yes_pack["maxLevel"] and yes_pack["currentLevel"] < maxUpgrade and self.balance >= yes_pack["upgradeCost"]:
                payload = json.dumps({"upgrade_type": 4})
                response = http_client.post(f"{endpoint}build/levelUp", json=payload)
                if response.ok:
                    logger.success(f"{self.session_name} | <green>Successfully upgraded Yes Pack to level {yes_pack['currentLevel'] + 1}</green>")
                    self.update_balance(http_client)
                    await asyncio.sleep(random.uniform(1, 3))

            other_upgrade_types = [1, 2, 3]
            random.shuffle(other_upgrade_types)
            for upgrade_type in other_upgrade_types:
                upgrade_info = upgrade_data[upgrade_type]
                if upgrade_info["currentLevel"] < upgrade_info["maxLevel"] and upgrade_info["currentLevel"] < maxUpgrade and self.balance >= upgrade_info["upgradeCost"]:
                    payload = json.dumps({"upgrade_type": upgrade_type})
                    response = http_client.post(f"{endpoint}build/levelUp", json=payload)
                    if response.ok:
                        logger.info(f"{self.session_name} | <green>Successfully upgraded {upgrade_info['name']} to level {upgrade_info['currentLevel'] + 1}</green>")
                        self.update_balance(http_client)
                        await asyncio.sleep(random.uniform(1, 3))
                    else:
                        logger.warning(f"{self.session_name} | <yellow>Failed to upgrade {upgrade_info['name']}.</yellow>")

            logger.warning(f"{self.session_name} | <yellow>Completed all possible upgrades with current balance.</yellow>")
            return True

        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to upgrade level: {e}")
            return False
        
    def fetch_missions(self, http_client: cloudscraper.CloudScraper):
        try:
            missions = http_client.get(f"{endpoint}mission/getDailyMission")
            res = missions.json()
            if missions.status_code == 200 and res.get("code") == 0:
                data = res.get("data")
                return data
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to fetch daily missions: {missions.status_code}</yellow>")
                return None
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to fetch daily missions: {e}")
            return None

    async def check_mission(self, http_client: cloudscraper.CloudScraper, mission_id: str, attempt=3, maxattempt=3):
        if attempt == 0:
            return False
        try:
            payload = json.dumps(mission_id)
            logger.info(f"{self.session_name} | Attempt <red>{maxattempt - attempt + 1}</red> to check daily mission: <cyan>{mission_id}</cyan>")
            check_mission = http_client.post(f"{endpoint}mission/checkDailyMission", data=payload)
            res = check_mission.json()
            if check_mission.status_code == 200:    
                if res.get("code") == 0:
                    data = res.get("data")
                    logger.success(f"{self.session_name} | <green>Checking daily mission {mission_id}...</green>")
                    return True
                else:
                    logger.warning(f"{self.session_name} | <yellow>Failed to check daily mission {mission_id}: {res.get('message')}</yellow>")
                    await asyncio.sleep(random.uniform(3, 5))
                    return await self.check_mission(http_client, mission_id, attempt - 1, maxattempt)
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to check daily mission {mission_id}: {check_mission.status_code}</yellow>")
                await asyncio.sleep(random.uniform(3, 5))
                return await self.check_mission(http_client, mission_id, attempt - 1, maxattempt)
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to check daily mission {mission_id}: {e}")
            return False

    async def claim_mission(self, http_client: cloudscraper.CloudScraper, mission_id: str, attempt=3, maxattempt=3):
        if attempt == 0:
            return False
        
        try:
            payload = json.dumps(mission_id)
            logger.info(f"{self.session_name} | Attempt <red>{maxattempt - attempt + 1}</red> to check daily mission: <cyan>{mission_id}</cyan>")
            claim_mission = http_client.post(f"{endpoint}mission/claimReward", data=payload)
            res = claim_mission.json()
            if claim_mission.status_code == 200:
                if res.get("code") == 0:
                    logger.success(f"{self.session_name} | <green>Successfully claimed daily mission {mission_id}: Claimed <cyan>{res['data']['reward']}</cyan> coins. <cyan>{res['data']['score']}</cyan> points added to your level.</green>")
                    self.update_balance(http_client)
                    return True
                else:
                    logger.warning(f"{self.session_name} | <yellow>Failed to claim daily mission {mission_id}: {res.get('message')}</yellow>")
                    await asyncio.sleep(random.uniform(3, 5))
                    return await self.claim_mission(http_client, mission_id, attempt - 1, maxattempt)
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to claim daily mission {mission_id}: {claim_mission.status_code}</yellow>")
                await asyncio.sleep(random.uniform(3, 5))
                return await self.claim_mission(http_client, mission_id, attempt - 1, maxattempt)
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to claim daily mission {mission_id}: {e}")
            return False
        
    async def process_missions(self, http_client: cloudscraper.CloudScraper, attempt=3, maxattempt=3):
        if attempt == 0:
            return False

        missions = self.fetch_missions(http_client)
        if missions is None:
            return False

        for mission in missions:
            if mission['missionStatus'] == 0:
                check = await self.check_mission(http_client, mission['missionId'], attempt, maxattempt)
                if check:
                    await asyncio.sleep(random.uniform(3, 5))
                    await self.claim_mission(http_client, mission['missionId'], attempt, maxattempt)
                else:
                    logger.warning(f"{self.session_name} | <yellow>Skipping mission {mission['missionId']} after failed attempts.</yellow>")

                await asyncio.sleep(random.uniform(1, 3))

        logger.success(f"{self.session_name} | <green>Successfully processed all daily missions</green>")
        return True
    
    async def fetch_tasks(self, http_client: cloudscraper.CloudScraper):
        try:
            tasks = http_client.get(f"{endpoint}task/getTaskList")
            res = tasks.json()
            if tasks.status_code == 200 and res.get("code") == 0:
                data = res.get("data")
                return data
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to fetch tasks: {res['message']}</yellow>")
                return None
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to fetch tasks: {e}")
            return None
        
    async def check_task(self, http_client: cloudscraper.CloudScraper, task_id: str, attempt=3, maxattempt=3):
        if attempt == 0:
            return False

        try:
            payload = json.dumps(task_id)
            check_task = http_client.post(f"{endpoint}task/checkTask", data=payload)
            res = check_task.json()
            if check_task.status_code == 200:
                if res.get("code") == 0:
                    logger.success(f"{self.session_name} | <green>Checking task {task_id}...</green>")
                    return True
                else:
                    logger.warning(f"{self.session_name} | <yellow>Failed to check task {task_id}: {res.get('message')}</yellow>")
                    await asyncio.sleep(random.uniform(3, 5))
                    return await self.check_task(http_client, task_id, attempt - 1, maxattempt)
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to check task {task_id}: {check_task.status_code}</yellow>")
                await asyncio.sleep(random.uniform(3, 5))
                return await self.check_task(http_client, task_id, attempt - 1, maxattempt)
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to check task {task_id}: {e}")
            return False

    async def finish_task(self, http_client: cloudscraper.CloudScraper, task_id: str, attempt=3, maxattempt=3):
        if attempt == 0:
            return False    
        try:
            payload = json.dumps(task_id)
            finish_task = http_client.post(f"{endpoint}task/claimTaskReward", data=payload)
            res = finish_task.json()
            if finish_task.status_code == 200:
                if res.get("code") == 0:
                    logger.success(f"{self.session_name} | <green>Successfully finished task {task_id}. Claimed <cyan>{res.get('data').get('bonusAmount')}</cyan> coins.</green>")
                    self.update_balance(http_client)
                    return True
                else:
                    logger.warning(f"{self.session_name} | <yellow>Failed to finish task {task_id}: {res.get('message')}</yellow>")
                    await asyncio.sleep(random.uniform(3, 5))
                    return await self.finish_task(http_client, task_id, attempt - 1, maxattempt)
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to finish task {task_id}: {finish_task.status_code}</yellow>")
                await asyncio.sleep(random.uniform(3, 5))
                return await self.finish_task(http_client, task_id, attempt - 1, maxattempt)
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to finish task {task_id}: {e}")
            return False
        
    async def process_tasks(self, http_client: cloudscraper.CloudScraper):
        tasks = await self.fetch_tasks(http_client)
        
        if not tasks:
            logger.warning(f"{self.session_name} | No tasks found to process.")
            return False

        all_tasks = [task for task_list in tasks.values() if isinstance(task_list, list) for task in task_list]
        unfinished_tasks = [task for task in all_tasks if task["taskStatus"] == 0]

        if not unfinished_tasks:
            logger.info(f"{self.session_name} | <green>All tasks are already completed. </green>")
            return True

        for task in unfinished_tasks:
            check = await self.check_task(http_client, task["taskId"])
            if not check:
                logger.warning(f"{self.session_name} | <yellow>Skipping task: {task['taskDescription']}</yellow>")
                continue
            await asyncio.sleep(random.uniform(1, 3))
            await self.finish_task(http_client, task["taskId"], 3, 3)
            logger.info(f"{self.session_name} | <green>Completed task: {task['taskDescription']}</green>")

        skipped_tasks = len(all_tasks) - len(unfinished_tasks)
        if skipped_tasks:
            logger.info(f"{self.session_name} | Skipped {skipped_tasks} already completed tasks.")

        logger.success(f"{self.session_name} | <green>Successfully processed all tasks.</green>")
        return True
    
    async def finish_upgrade_task(self, http_client: cloudscraper.CloudScraper, task_id: str):
        try:
            payload = json.dumps(task_id)
            finish_task = http_client.post(f"{endpoint}task/finishUserUpgradeTask", data=payload)
            res = finish_task.json()
            if finish_task.status_code == 200 and res.get("code") == 0:
                logger.success(f"{self.session_name} | <green>Successfully finished upgrade task {task_id}. Claimed <cyan>{res.get('data').get('bonusAmount')}</cyan> coins.</green>")
                return True
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to finish upgrade task {task_id}: {res.get('message')}</yellow>")
                return False
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to finish upgrade task {task_id}: {e}")
            return False
        
    async def process_upgrade_tasks(self, http_client: cloudscraper.CloudScraper):
        try:
            upgrade_tasks = http_client.get(f"{endpoint}task/getUserUpgradeTaskList")
            res = upgrade_tasks.json()
            if upgrade_tasks.status_code == 200 and res.get("code") == 0:
                data = res.get("data")
                tasks = data.get("taskBonusBaseResponseList")

                if not tasks:
                    logger.warning(f"{self.session_name} | No upgrade tasks found to process.")
                    return False
                
                eligible_tasks = [task for task in tasks if task['taskUserLevel'] <= data['userLevel']]
                if not eligible_tasks:
                    logger.warning(f"{self.session_name} | No eligible upgrade tasks found to process.")
                    return False
                
                for task in eligible_tasks:
                    if task['taskStatus'] == 0:
                        finish_upgrade_task = await self.finish_upgrade_task(http_client, task['taskId'])
                        if finish_upgrade_task:
                            logger.info(f"{self.session_name} | <green>Completed upgrade task: {task['taskDescription']}</green>")
                        else:
                            logger.warning(f"{self.session_name} | <yellow>Failed to finish upgrade task: {task['taskDescription']}</yellow>")

                logger.success(f"{self.session_name} | <green>Successfully processed all upgrade tasks.</green>")
                return True

            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to fetch upgrade tasks: {res['message']}</yellow>")
                return None
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to fetch upgrade tasks: {e}")
            return None
        
    
    async def claim_bonus(self, http_client: cloudscraper.CloudScraper, bonus_id: int):
        try:
            payload = json.dumps(bonus_id)
            claim_bonus = http_client.post(f"{endpoint}task/claimBonus", data=payload)
            res = claim_bonus.json()
            if claim_bonus.status_code == 200 and res.get("code") == 0:
                data = res.get("data")
                logger.success(f"{self.session_name} | <green>Finished {bonus_id == 1 and 'Daily Mission' or 'Tasks'} bonus. Successfully claimed <cyan>{data['bonusAmount']}</cyan> coins.</green>")
                return True
            else:
                logger.warning(f"{self.session_name} | <yellow>Failed to claim bonus {bonus_id}: {res['message']}</yellow>")
                return None
        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while trying to claim bonus: {e}")
            return None
        

    # Get YES SUMMER SKINS
    # async def claim_skins_mystery_reward(self, http_client: cloudscraper.CloudScraper):
    #     try:
    #         claim_skins = http_client.post(f"{endpoint}skin/claimReward")
    #         res = claim_skins.json()
    #         if claim_skins.status_code == 200 and res.get("code") == 0:
    #             logger.success(f"{self.session_name} | <green>Successfully claimed <cyan>YES SUMMER SKINS MYSTERY REWARD!</cyan>. Claimed <cyan>{res.get('data').get('bonusAmount')}</cyan> coins.</green>")
    #             return True
    #         else:
    #             logger.warning(f"{self.session_name} | <yellow>Failed to claim <cyan>YES SUMMER SKINS MYSTERY REWARD</cyan>: {res['message']}</yellow>")
    #             return None
    #     except Exception as e:
    #         logger.error(f"{self.session_name} | Unknown error while trying to claim <cyan>YES SUMMER SKINS MYSTERY REWARD!</cyan>: {e}")
    #         return None



    async def run(self, proxy: str | None) -> None:
        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        headers["User-Agent"] = generate_random_user_agent(device_type='android', browser_type='chrome')
        http_client = CloudflareScraper(headers=headers, connector=proxy_conn)
        session = cloudscraper.create_scraper()
        if proxy:
            proxy_check = await self.check_proxy(http_client=http_client, proxy=proxy)
            if proxy_check:
                proxy_type = proxy.split(':')[0]
                proxies = {
                    proxy_type: proxy
                }
                session.proxies.update(proxies)
                logger.info(f"{self.session_name} | bind with proxy ip: {proxy}")
            else:
                http_client._connector = None

        while True:
            try:
                await self.get_token(session)
                
                if self.auth_token:
                    http_client.headers['token'] = f"{self.auth_token}"
                    session.headers = http_client.headers.copy()

                    await asyncio.sleep(random.uniform(1, 3))

                    self.process_invitation(session)

                    self.update_balance(session)
                    await asyncio.sleep(random.uniform(1, 2))

                    self.refresh_special_box(session)
                    await asyncio.sleep(random.uniform(1, 2))

                    game_data = self.fetch_account_info(session)

                    if game_data:
                        rank = game_data.get('levelInfo', {}).get('rankName', '')
                        level = game_data.get('levelInfo', {}).get('level', 0)

                        logger.info(f"{self.session_name} | <green>Rank: <cyan>{rank}</cyan> - Level: <cyan>{level}</cyan></green>")

                    game_info = self.fetch_build_info(session)
                    if game_info:
                        chests_left = game_info.get('specialBoxLeftRecoveryCount', 0)
                        recovery_count = game_info.get('coinPoolLeftRecoveryCount', 0)
                        multi_value_level = game_info.get('singleCoinValue', 0)
                        coin_limit_level = game_info.get('singleCoinLevel', 0)
                        fill_rate_level = game_info.get('coinPoolRecoverySpeed', 0)
                        yes_pack_level = game_info.get('swipeBotLevel', 0)
                        
                        logger.info(f"{self.session_name} | <green>Chests left: <cyan>{chests_left}</cyan> - Recovery count: <cyan>{recovery_count}</cyan> - Coins left: <cyan>{self.balance}</cyan></green>")
                        logger.info(f"{self.session_name} | <green>Multi value: <cyan>{multi_value_level} Lvl</cyan> - Coin limit: <cyan>{coin_limit_level} Lvl</cyan> - Fill rate: <cyan>{fill_rate_level} Lvl</cyan> - Yes pack: <cyan>{yes_pack_level} Lvl</cyan></green>")

                    await self.process_checkin(session)
                    await asyncio.sleep(random.uniform(1, 3))

                    collect_info = self.fetch_game_info(session)
                    if collect_info:
                        single_coin_value = collect_info.get('singleCoinValue', 0)
                        coin_pool_left_count = collect_info.get('coinPoolLeftCount', 0)
                        logger.info(f"{self.session_name} | <green>Collecting coins...</green>")
                        if coin_pool_left_count > 0:
                            amount = coin_pool_left_count // single_coin_value
                            self.collect_coin(session, amount)
                            await asyncio.sleep(random.uniform(1, 3))

                    if game_info and game_info.get('specialBoxLeftRecoveryCount', 0) > 0:
                        for _ in range(game_info.get('specialBoxLeftRecoveryCount', 0)):
                            if self.recover_special_box(session):
                                box_info = self.fetch_special_box(session)
                                box_info = box_info['recoveryBox']
                                if box_info is not None and box_info['boxStatus'] is True:
                                    logger.info(f"{self.session_name} | <green>Collecting special box...</green>")
                                    self.collect_special_box(session, box_info['boxType'], box_info['specialBoxTotalCount'])
                                    self.refresh_special_box(session)
                                    await asyncio.sleep(0.5)
                        await asyncio.sleep(random.uniform(1, 3))

                    game_info = self.fetch_build_info(session)
                    if game_info and game_info.get('coinPoolLeftRecoveryCount', 0) > 0:
                        for _ in range(game_info.get('coinPoolLeftRecoveryCount', 0)):
                            if self.recover_coin_pool(session):
                                collect_info = self.fetch_game_info(session)
                                coin_pool_left_count = collect_info.get('coinPoolLeftCount', 0)
                                if coin_pool_left_count > 0:
                                    amount = coin_pool_left_count // game_info.get('singleCoinValue', 1)
                                    self.collect_coin(session, amount)
                                    await asyncio.sleep(0.5)
                        await asyncio.sleep(random.uniform(1, 3))

                    self.process_offline_bonus(session)
                    await asyncio.sleep(random.uniform(1, 3))

                    await self.process_missions(session)
                    await asyncio.sleep(random.uniform(1, 3))

                    if settings.AUTO_TASK:
                        await self.process_tasks(session)
                        await asyncio.sleep(random.uniform(1, 3))

                        await self.process_upgrade_tasks(session)
                        await asyncio.sleep(random.uniform(1, 3))

                        await self.claim_bonus(session, 1)
                        await asyncio.sleep(random.uniform(1, 2))
                        await self.claim_bonus(session, 2)
                        await asyncio.sleep(random.uniform(1, 2))

                    if settings.AUTO_UPGRADE_LEVEL:
                        await self.upgrade_level(session)
                        await asyncio.sleep(random.uniform(1, 3))

                    box_info = self.fetch_special_box(session)
                    box_info = box_info['autoBox']
                    if box_info is not None and box_info['boxStatus'] is True:
                        self.collect_special_box(session, box_info['boxType'], box_info['specialBoxTotalCount'])
                        self.refresh_special_box(session)
                        await asyncio.sleep(random.uniform(1, 3))

                    logger.info(f"----<cyan>Completed {self.session_name}</cyan>----")
                    await http_client.close()
                    session.close()
                    return

            except InvalidSession as error:
                raise error

            except Exception as error:
                # traceback.print_exc()
                logger.error(f"{self.session_name} | Unknown error: {error}")
                await asyncio.sleep(delay=uniform(60, 120))


async def run_query_tapper(query: str, name: str, proxy: str | None):
    try:
        sleep_ = uniform(15, 60)
        logger.info(f" start after {sleep_}s")
        await asyncio.sleep(sleep_)
        await Tapper(query=query, session_name=name, multi_thread=False).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"Invalid Query: {query}")

async def run_query_tapper1(querys: list[str], proxies):
    proxies_cycle = cycle(proxies) if proxies else None
    name = "Account"

    while True:
        i = 0
        for query in querys:
            try:
                await Tapper(query=query, session_name=f"{name} {i}", multi_thread=True).run(next(proxies_cycle) if proxies_cycle else None)
            except InvalidSession:
                logger.error(f"Invalid Query: {query}")
            i += 1

            sleep_ = uniform(settings.DELAY_EACH_ACCOUNT[0], settings.DELAY_EACH_ACCOUNT[1])
            logger.info(f"Sleep {sleep_}s...")
            await asyncio.sleep(sleep_)

        sleep_ = uniform(600, 700)
        logger.info(f"<red>Sleep {sleep_}s...</red>")
        await asyncio.sleep(sleep_)
