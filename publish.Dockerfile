FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -i index-url=http://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /usr/local/lib/python3.6/site-packages
COPY . .

CMD [ "python", "cmd/publish.py" ]