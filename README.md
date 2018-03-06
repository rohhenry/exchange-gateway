# exchange-gateway
proof of concept exchange gateway using gemini's test api

Interactions with gemeni's trading api is done through gemini.py

Interactions with database is in db.py

The core logic of the exchange is in logic.py

crawler.py just crawls over the db and prunes pending transactions

listen.py is the flask app

Everything else is just barebones html
