FROM mysql:8.0-debian
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd
RUN useradd -m -s /bin/bash factory && echo 'factory:6551903a-8044-4212-addd-70cd6afe00bc' | chpasswd
RUN mkdir /home/factory/.ssh
RUN ssh-keygen -t rsa -b 4096 -f /home/factory/.ssh/id_rsa -q -N "" && \
    cp /home/factory/.ssh/id_rsa.pub /home/factory/.ssh/authorized_keys && \
    chmod 644 /home/factory/.ssh/id_rsa
RUN chown -R factory:factory /home/factory/.ssh && chmod 600 /home/factory/.ssh/authorized_keys
COPY ./factory_reset.sh /home/factory/factory_reset.sh
RUN chown factory:factory /home/factory/factory_reset.sh
RUN chmod +x /home/factory/factory_reset.sh
COPY ./custom.cnf /etc/mysql/conf.d/custom.cnf
RUN chmod 644 /etc/mysql/conf.d/custom.cnf
COPY ./init.sql /docker-entrypoint-initdb.d/init.sql
COPY ./start.sh /start.sh
RUN chmod +x /start.sh
USER root
RUN mkdir /var/lib/mysql-files
RUN chown mysql:mysql /var/lib/mysql-files
RUN chown mysql:mysql /etc/mysql/my.cnf
RUN chmod 644 /etc/mysql/my.cnf
CMD ["/start.sh"]
