# Class definitions and functions for Data Objects
import aiohttp
import aiosqlite
from datetime import datetime, timezone

# Definition of Reward Class
class Reward:
    def __init__(self,reward_type,reward_item,reward_count):
        self.reward_type = reward_type
        self.reward_item = reward_item
        self.reward_count = reward_count

# Definition of Alert Class
class Alert:
    def __init__(self, alert_id, activation_time, expiration_time, mission_node, mission_type, mission_faction):
        self.alert_id = alert_id
        self.activation_time = activation_time
        self.expiration_time = expiration_time
        self.mission_node = mission_node
        self.mission_type = mission_type
        self.mission_faction = mission_faction
        self.rewards = []

    # Function for adding rewards to the Alert Data Object
    def AddReward(self, reward):
        self.rewards.append(reward)


#################################################
# FUNCTIONS FOR INTERACTING WITH THE DATA OBJECTS

# Function for collecting alert data from Warframe Api
async def CollectNewAlertData():
    url = "https://api.warframestat.us/pc/alerts"
    alerts = []
    newAlerts =[]
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    alerts_data = await response.json()
                    
                    for alert_data in alerts_data:
                        alert_id = alert_data["id"]
                        activation_time = alert_data["activation"]
                        expiration_time = alert_data["expiry"]
                        mission_node = alert_data["mission"]["node"]
                        mission_type = alert_data["mission"]["type"]
                        mission_faction = alert_data["mission"]["faction"]
                        
                        alert = Alert(alert_id, activation_time, expiration_time, mission_node, mission_type, mission_faction)
                        
                        for reward_data in alert_data["reward"]:
                            reward_type = reward_data["type"]
                            reward_item = reward_data["item"]
                            if "count" in reward_data:
                                reward_count = reward_data["count"]
                            elif "amount" in reward_data:
                                reward_count = reward_data["amount"]
                            else:
                                reward_count = 1 # There will always be a reward count of 1 even if not specified
                                
                            reward = Reward(reward_type, reward_item, reward_count)
                            alert.AddReward(reward)
                        
                        alerts.append(alert)  # Append the alert inside the loop
                    savedAlerts = CollectSavedAlertData()
                    for alert in alerts:
                        if alert.alert_id not in savedAlerts:
                            newAlerts.append(alert)
                    
                    return newAlerts
                
                else:
                    raise Exception("Failed to fetch alerts. Status code: {response.status}")
    
    except aiohttp.ClientError as e:
        raise e

# This function collects the current active alert information store in the database based on
# which alerts the current time is between the activation tima nd expiration time    
async def CollectSavedAlertData():
    savedAlerts = []
    current_time = datetime.now(timezone.utc).isoformat()
    try:
        statement = "SELECT alert_id FROM Alerts WHERE ? BETWEEN activation_time AND expiration_time"

        async with aiosqlite.connect("alerts_db.db") as con:
            async with con.execute(statement, (current_time,)) as cursor:
                async for row in cursor:
                    savedAlerts.append(row[0])

        return savedAlerts
    except Exception as e:
        raise e
    finally: 
        cursor.close()


# This function saves new alert data to the database
async def SaveNewAlertData(alerts):
    alert_statement = "INSERT INTO Alerts (alert_id, activation_time, expiration_time, mission_node, mission_type, mission_faction) VALUES (?, ?, ?, ?, ?, ?)"
    reward_statement = "INSERT INTO Rewards (alert_id, reward_type, reward_item, reward_count) VALUES (?, ?, ?, ?)"
    
    try:
        async with aiosqlite.connect("alerts_db.db") as con:
            cur = await con.cursor()
            for alert in alerts:
                cur.execute(alert_statement,(alert.alert_id, alert.activation_time, alert.expiration_time, alert.mission_node, alert.mission_type, alert.mission_faction))
                alert_id = cur.lastrowid
                
                for reward in alert.rewards:
                    cur.execute(reward_statement,(alert_id, reward.reward_type, reward.reward_item, reward.reward_count))
            await con.commit()
    except Exception as e:
        raise e
    finally:
        await cur.close()
    return 