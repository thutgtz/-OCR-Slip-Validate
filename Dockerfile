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
RUN /root/.nvm/versions/node/v${NODE_VERSION}/bin/npm install  leasot@latest -g
RUN apt-get update && \
    apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.6 python3-distutils python3-pip python3-apt python3-dev
RUN apt-get install -y build-essential libzbar-dev

RUN apt-get install -y bzip2 
RUN apt-get install -y libx11-6
RUN apt-get install -y cmake
RUN apt-get install -y g++ 
RUN apt-get install -y wget
RUN apt-get install -y cmake
RUN apt-get install -y unzip 
RUN apt-get install -y pkg-config
RUN apt-get install -y python-opencv
RUN apt-get install -y libopencv-dev 
RUN apt-get install -y libjpeg-dev 
RUN apt-get install -y libpng-dev 
RUN apt-get install -y libtiff-dev  
RUN apt-get install -y libgtk2.0-dev 
RUN apt-get install -y python-numpy 
RUN apt-get install -y python-pycurl 
RUN apt-get install -y libatlas-base-dev
RUN apt-get install -y qt5-default
RUN apt-get install -y libvtk6-dev 
RUN apt-get install -y zlib1g-dev
RUN apt-get install -y python3-venv 

RUN alias python='/usr/bin/python3'
RUN pip3 install imutils
RUN pip3 install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install easyocr
RUN pip3 install pyzbar
RUN pip3 install simplejson 
RUN pip3 install numpy


RUN git clone https://github.com/opencv/opencv_contrib  && \
    cd opencv_contrib  && \
    git fetch --all --tags  && \
    git checkout tags/4.3.0  && \
    cd .. && \
    git clone https://github.com/opencv/opencv.git  && \
    cd opencv  && \
    git checkout tags/4.3.0   

RUN pwd &&\
   cd opencv  && \
   pwd &&\
   mkdir build && cd build && \
   pwd &&\
   cmake -DCMAKE_BUILD_TYPE=Release  \
     -DENABLE_CXX14=ON                 \
     -DBUILD_PERF_TESTS=OFF            \
     -DOPENCV_GENERATE_PKGCONFIG=ON    \
     -DWITH_XINE=ON                    \
     -DBUILD_TESTS=OFF                 \
     -DENABLE_PRECOMPILED_HEADERS=OFF  \
     -DCMAKE_SKIP_RPATH=ON             \
     -DBUILD_WITH_DEBUG_INFO=OFF       \
     -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules  \
     -Dopencv_dnn_superres=ON /usr/bin/ .. && \
   make -j$(nproc) && \
   make install 

RUN pip3 install zbar
WORKDIR /app
RUN npm install 
