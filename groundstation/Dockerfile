FROM ubuntu:24.04

# noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Password utenti
ENV HELPDESK_PASSWORD=H3lpd3skH3ro3s123!
ENV RESEARCH_PASSWORD=ScienceGeekSquad#2025!
ENV SECURITY_PASSWORD=david.thompson88
ENV HR_PASSWORD="Hum4nR3s2025!#"

# Installa roba
RUN apt-get update && apt-get install -y --no-install-recommends openssh-server vsftpd

# Crea utenti
RUN useradd -m helpdesk && echo "helpdesk:$HELPDESK_PASSWORD" | chpasswd
RUN useradd -m research && echo "research:$RESEARCH_PASSWORD" | chpasswd
RUN useradd -m security && echo "security:$SECURITY_PASSWORD" | chpasswd
RUN useradd -m hr && echo "hr:$HR_PASSWORD" | chpasswd

# Crea directory data
RUN mkdir -p /data/security /data/helpdesk /data/hr /data/research /data/public

# Configura SSH
RUN mkdir /var/run/sshd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login (utile?)
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd

# FTP
RUN mkdir -p /var/run/vsftpd/empty /data/public && \
    chown nobody:nogroup /data/public && \
    chmod 755 /data/public

RUN echo "listen=YES" > /etc/vsftpd.conf && \
    echo "dirmessage_enable=YES" >> /etc/vsftpd.conf && \
    echo "use_localtime=YES" >> /etc/vsftpd.conf && \
    echo "xferlog_enable=YES" >> /etc/vsftpd.conf && \
    echo "connect_from_port_20=YES" >> /etc/vsftpd.conf && \
    echo "local_enable=YES" >> /etc/vsftpd.conf && \
    echo "write_enable=NO" >> /etc/vsftpd.conf && \
    echo "chroot_local_user=YES" >> /etc/vsftpd.conf && \
    echo "secure_chroot_dir=/var/run/vsftpd/empty" >> /etc/vsftpd.conf && \
    echo "pam_service_name=vsftpd" >> /etc/vsftpd.conf && \
#    echo "userlist_enable=YES" >> /etc/vsftpd.conf && \
#    echo "userlist_file=/etc/vsftpd.userlist" >> /etc/vsftpd.conf && \
#    echo "userlist_deny=NO" >> /etc/vsftpd.conf && \
	echo "pasv_enable=YES" >> /etc/vsftpd.conf && \
    echo "pasv_min_port=40000" >> /etc/vsftpd.conf && \
    echo "pasv_max_port=40009" >> /etc/vsftpd.conf && \
    echo "pasv_address=127.0.0.1" >> /etc/vsftpd.conf && \
    echo "user_sub_token=\$USER" >> /etc/vsftpd.conf && \
    echo "local_root=/data/\$USER" >> /etc/vsftpd.conf && \
	echo "allow_writeable_chroot=YES" >> /etc/vsftpd.conf && \
    echo "anonymous_enable=YES" >> /etc/vsftpd.conf && \
    echo "anon_root=/data/public" >> /etc/vsftpd.conf && \
    echo "anon_upload_enable=NO" >> /etc/vsftpd.conf && \
    echo "anon_mkdir_write_enable=NO" >> /etc/vsftpd.conf && \
    echo "no_anon_password=YES" >> /etc/vsftpd.conf
	
# Starta servizi
COPY start.sh /opt/start.sh
RUN chmod 700 /opt/start.sh
COPY ./data /data
CMD ["/opt/start.sh"]
