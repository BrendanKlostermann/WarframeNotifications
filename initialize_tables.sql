create table if not exists Alerts(
    alert_id TEXT PRIMARY KEY,
    activation_time DATETIME NOT NULL,
    expiration_time DATETIME NOT NULL,
    mission_node TEXT,
    mission_type TEXT,
    mission_faction TEXT
);


create table if not exists RewardLineItem(
    reward_id INTEGER PRIMARY KEY,
    alert_id TEXT NOT NULL,
    reward_type TEXT,
    reward_item TEXT,
    reward_count INTEGER,
    FOREIGN KEY (alert_id) REFERENCES Alerts(alert_id)
);


create table if not exists Arbitration(
    id TEXT PRIMARY KEY,
    activation_time DATETIME NOT NULL,
    expiration_time DATETIME NOT NULL,
    mission_type TEXT,
    enemy_type TEXT,
    node TEXT
)