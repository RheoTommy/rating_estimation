FROM ubuntu:21.04

RUN mkdir /source_codes

ADD source_codes /source_codes

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-add-repository ppa:ubuntu-toolchain-r/test; apt update; apt install -y g++-9 wget build-essential python-dev autotools-dev libicu-dev libbz2-dev libboost-all-dev; \
    wget https://boostorg.jfrog.io/artifactory/main/release/1.71.0/source/boost_1_71_0.tar.bz2 \
    && tar xf boost_1_71_0.tar.bz2 \
    && cd boost_1_71_0 \
    && ./bootstrap.sh --prefix=/opt/boost/gcc \
    && ./b2 install \
    && git clone https://github.com/atcoder/ac-library.git /opt/ac-library