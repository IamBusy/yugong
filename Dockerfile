FROM markadams/chromium-xvfb-py3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo Asia/Shanghai > /etc/timezone && \
    pip3 install --no-cache-dir -r requirements.txt

ENV app=fetch
COPY . /usr/lib/python3/dist-packages
COPY . .

CMD "python3" "cmd/${app}.py"