FROM ubuntu:latest
#FROM python:3.12
LABEL authors="cha"

#ENTRYPOINT ["top", "-b"]


#RUN apt install webp
RUN apt-get update && apt-get install -y \
     python3.12\
      python3.12-venv\
#    python-qt4 \
#    python-pyside \
    #python-pip
    webp \
    graphicsmagick \
    inkscape\
    python3-pip
    #python3-pyqt5





COPY requirements.txt .
COPY slimebot.py .
COPY imagetest.py .
COPY slimeql.py .
COPY test.db .
COPY images ./images

RUN python3 -m venv /opt/venv
#RUN python3 -m venv ~/py_envs
#RUN source ~/py_envs/bin/activate
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

#RUN pip install --no-cache-dir -r requirements.txt


#RUN apt install graphicsmagick
#sudo apt install inkscape
#CMD ["python", "-m", "pytest", "-v"]
#CMD ["python3.12", "./slimebot.py"]
CMD . /opt/venv/bin/activate && exec python3.12 slimebot.py