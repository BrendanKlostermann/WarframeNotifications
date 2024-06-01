@ECHO OFF
ECHO "Initializing or connecting to alerts_db database."
sqlite3 alerts_db.sqlite ""

ECHO "Creating or modifying database tables."
sqlite3 alerts_db.sqlite < initialize_tables.sql

ECHO "Checking tables to ensure accuracy."
sqlite3 alerts_db.sqlite ".tables"

ECHO "Database initialization completed."

PAUSE