#-dをつけるとバックグラウンドで実行できる
docker rm mysql
docker-compose down --rmi all
docker-compose build --no-cache
docker-compose up -d