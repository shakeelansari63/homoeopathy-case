FROM    amd64/ubuntu:20.04
USER    root
RUN     apt-get update -y
RUN     apt-get install python3 python3-pip -y
RUN     pip3 install pyinstaller
RUN     pip3 install qtmodern
RUN     pip3 install PyQt5
CMD     ["python3", "/project/compile.py"]