FROM tleemcjr/metasploitable2:latest

WORKDIR /metasploitable2

COPY ./root.txt .

CMD [ "/bin/bash", "-c", "/bin/services.sh && tail -F /var/log/nginx/access.log"]
