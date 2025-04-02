# fr_arbitrage_bot
A funding rate arbitrage bot for crypto exchanges.

Please do your own research before running this bot in production environment.

**USE AT YOUR OWN RISK.**

## DB migration

first time
```
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

follow up
```
flask db migrate -m "Comment here"
flask db upgrade
```
