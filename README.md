# simple-tg-bot
docker build . -t tg-bot  <br/>
docker run -e -d APP_URL='endpoint of data-proceccing-web-app' -e TG_BOT_TOKEN='token' tg-bot
