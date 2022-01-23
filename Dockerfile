# Set docker image
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV NODE_VERSION=10.24.1
RUN apt-get update && \
    apt-get install wget curl ca-certificates rsync -y
RUN wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" &&  nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
RUN cp /root/.nvm/versions/node/v${NODE_VERSION}/bin/node /usr/bin/
RUN cp /root/.nvm/versions/node/v${NODE_VERSION}/bin/npm /usr/bin/
RUN apt-get update && \
    apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.6 python3-distutils python3-pip python3-apt python3-dev
RUN apt-get install -y build-essential libzbar-dev

RUN apt-get install -y bzip2 \
    libx11-6 \
    cmake \
    g++ \
    wget \
    cmake \
    unzip \
    pkg-config \
    python3-opencv \
    libopencv-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libgtk2.0-dev \
    python-numpy \
    python-pycurl \
    libatlas-base-dev \
    qt5-default \
    libvtk6-dev \
    zlib1g-dev \
    python3-venv 

RUN alias python='/usr/bin/python3'
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir imutils
RUN pip3 install --no-cache-dir torch==1.10.1+cpu torchvision==0.11.2+cpu torchaudio==0.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip3 install --no-cache-dir easyocr
RUN pip3 install --no-cache-dir pyzbar
RUN pip3 install --no-cache-dir simplejson 
RUN pip3 install --no-cache-dir numpy
RUN pip3 install --no-cache-dir zbar-py
RUN pip uninstall -y opencv-python-headless==4.5.5.62 
RUN pip install opencv-python-headless==4.1.2.30
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN apt-get install -y language-pack-en
ENV LANG="en_US.UTF-8"
ENV LC_ALL="en_US.UTF-8"
WORKDIR /app
COPY ./package.json /app
RUN npm install -g nodemon --unsafe-perm=true --allow-root
COPY . /app
CMD ["node" , "index.js"]