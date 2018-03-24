FROM mark-adams/docker-chromium-xvfb

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo Asia/Shanghai > /etc/timezone && \
    pip install --no-cache-dir -r requirements.txt

ENV app=fetch
COPY . /usr/local/lib/python3.6/site-packages
COPY . .

CMD "python" "cmd/${app}.py"