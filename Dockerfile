FROM alpine:latest

RUN apk add --no-cache bash python3 py3-pip git curl openssl

WORKDIR /root/ish-dev

COPY . .

RUN pip3 install requests supabase

RUN chmod +x core/*.sh core/*.py

CMD ["/root/ish-dev/core/menu.sh"]
