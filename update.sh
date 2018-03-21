contName=$1
docker stop ${contName};
docker rm ${contName};
docker build -t yugong-${contName} -e "app=${contName}" .
docker run --name ${contName} -d  yugong-${contName}