FROM debian:stretch

RUN apt-get update && \
	apt-get -y install sudo python

RUN useradd -m build && echo "build:build" | chpasswd && adduser build sudo && \
	echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
	mkdir /build && chown build.build /build

USER build
WORKDIR /build

CMD /bin/bash
