contName=fetcher
docker stop ${contName};
docker rm ${contName};
docker build -t yugong-fetcher -f fetch.Dockerfile .
docker run --name ${contName} -d  yugong-fetcher