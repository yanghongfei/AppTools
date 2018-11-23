FROM centos:7
# 设置编码
ENV LANG en_US.UTF-8
# 同步时间
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 1. 安装基本依赖
RUN yum update -y && yum install epel-release -y && yum update -y && yum install wget unzip epel-release nginx  xz gcc automake zlib-devel openssl-devel supervisor  groupinstall development  libxslt-devel libxml2-devel libcurl-devel git -y
#WORKDIR /var/www/

# 2. 准备python
RUN wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tar.xz
RUN xz -d Python-3.6.4.tar.xz && tar xvf Python-3.6.4.tar && cd Python-3.6.4 && ./configure && make && make install

# 3. 安装yum依赖

# 4. 复制代码
RUN mkdir -p /opt/AppTools/
ADD . /opt/AppTools/

# 5. 安装pip依赖
WORKDIR /opt/AppTools/
RUN pip3 install -U pip && \
RUN pip3 install --upgrade pip && \
RUN pip3 install -r requirements.txt

# 6. 日志
# VOLUME /var/log/

# 7. 准备文件
COPY supervisord.conf  /etc/supervisord.conf

EXPOSE 9001
CMD ["/usr/bin/supervisord"]
