FROM ubuntu:18.04

#RUN apt-add-repository ppa:ubuntu-toolchain-r/test 
RUN apt update && apt install -y g++-9 && apt install -y wget
RUN wget https://boostorg.jfrog.io/artifactory/main/release/1.71.0/source/boost_1_71_0.tar.bz2
RUN tar xf boost_1_71_0.tar.bz2
RUN cd boost_1_71_0 && ./bootstrap.sh --prefix=/opt/boost/gcc && ./b2 install
ADD source_codes/ /source_codes/


