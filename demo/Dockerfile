FROM python:3.10.14-alpine
RUN pip install flask
RUN apk add --update npm
RUN apk add --update openssh
RUN ssh-keygen -A
RUN mkdir -p /app/public
WORKDIR /app
COPY node/package.json /app
COPY node/package-lock.json /app
RUN npm i
RUN rm /app/package.json
RUN rm /app/package-lock.json
COPY node/public /app/public
COPY node/app.js /app
COPY node/documents.js /app
COPY start.sh /
COPY node/index.pug /app
COPY node/document.pug /app
COPY node/layout.pug /app
RUN addgroup -S dave && adduser -S dave -G dave --shell /bin/sh
RUN echo "dave:1e8aa90e-ac0a-4cab-a9aa-543878f6a16a" | chpasswd
RUN chown -R dave:dave /app
RUN chmod +x /start.sh
RUN mkdir /home/dave/.ssh && \
    chown dave:dave /home/dave/.ssh
RUN addgroup -S admin && adduser -S admin -G admin --shell /bin/sh
RUN echo "admin:acac77f6-00c1-4d16-8b0a-d007c037dc44" | chpasswd
RUN rm -rf /etc/ssh/ssh_host_rsa_key /etc/ssh/ssh_host_dsa_key
RUN ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
RUN ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa
RUN mkdir -p /var/run/sshd
USER dave
RUN ssh-keygen -t rsa -b 4096 -f /home/dave/.ssh/id_rsa -q -N "" && \
    cp /home/dave/.ssh/id_rsa.pub /home/dave/.ssh/authorized_keys && \
    chmod 600 /home/dave/.ssh/id_rsa
USER root
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/AllowTcpForwarding no/AllowTcpForwarding yes/' /etc/ssh/sshd_config
COPY python/__init__.py /usr/local/lib/python3.10/site-packages/werkzeug/debug/
RUN chmod 644 /usr/local/lib/python3.10/site-packages/werkzeug/debug/__init__.py && \
	chown root:root /usr/local/lib/python3.10/site-packages/werkzeug/debug/__init__.py

COPY python/tbtools.py /usr/local/lib/python3.10/site-packages/werkzeug/debug/
RUN chmod 644 /usr/local/lib/python3.10/site-packages/werkzeug/debug/tbtools.py && \
	chown root:root /usr/local/lib/python3.10/site-packages/werkzeug/debug/tbtools.py

COPY python/style.css /usr/local/lib/python3.10/site-packages/werkzeug/debug/shared/
RUN chmod 644 /usr/local/lib/python3.10/site-packages/werkzeug/debug/shared/style.css && \
	chown root:root /usr/local/lib/python3.10/site-packages/werkzeug/debug/shared/style.css

COPY python/debugger.js /usr/local/lib/python3.10/site-packages/werkzeug/debug/shared/
RUN chmod 644 /usr/local/lib/python3.10/site-packages/werkzeug/debug/shared/debugger.js && \
	chown root:root /usr/local/lib/python3.10/site-packages/werkzeug/debug/shared/debugger.js

COPY python/govgpt.png /usr/local/lib/python3.10/site-packages/werkzeug/debug/shared
RUN chmod 644 /usr/local/lib/python3.10/site-packages/werkzeug/debug/shared/govgpt.png && \
	chown root:root /usr/local/lib/python3.10/site-packages/werkzeug/debug/shared/govgpt.png
COPY python/app.py /home/admin/
COPY python/requests /home/admin/requests
RUN chown -R admin:admin /home/admin/
# RUN echo "* soft    nproc   3000" >> /etc/security/limits.conf
# RUN echo "* hard    nproc   3100" >> /etc/security/limits.conf
CMD ["/start.sh"]