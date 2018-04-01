FROM markadams/chromium-xvfb-py3
ENV LANG C.UTF-8

COPY requirements.txt ./

RUN mkdir /root/.pip && \
    curl -o /root/.pip/pip.conf http://ojiqea97q.bkt.clouddn.com/mirrors/pip.conf && \
    ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo Asia/Shanghai > /etc/timezone && \
    pip3 install --no-cache-dir -r requirements.txt

ENV app=fetch
COPY . /usr/local/lib/python3.5/dist-packages
COPY . .

CMD "python3" "cmd/${app}.py"