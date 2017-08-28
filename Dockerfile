FROM ubuntu:16.04

MAINTAINER Paulo Victor Moura "paulo.victor.moura@accenture.com"

RUN \
    apt-get update -y && apt-get upgrade -y && apt-get -y install build-essential cmake pkg-config && \
    apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev -y && \
    apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y && apt-get install libxvidcore-dev libx264-dev -y && apt-get install libgtk-3-dev -y && \
    apt-get install libatlas-base-dev gfortran -y && apt-get install python2.7-dev python3.5-dev -y && \
    apt-get install libatlas-base-dev gfortran -y && apt-get install python2.7-dev python3.5-dev -y && apt-get install wget unzip git -y

RUN cd ~ && wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip && \
   unzip opencv.zip && \
   wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip && unzip opencv_contrib.zip

RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py && \
   pip install numpy && cd ~/opencv-3.1.0/ && mkdir build && cd build/ && \
   cmake -D CMAKE_BUILD_TYPE=RELEASE     -D CMAKE_INSTALL_PREFIX=/usr/local     -D INSTALL_PYTHON_EXAMPLES=ON     -D INSTALL_C_EXAMPLES=OFF     -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules     -D PYTHON_EXECUTABLE=/usr/bin/python/     -D BUILD_EXAMPLES=ON .. && \
   make -j4 && make install && ldconfig
   
RUN  git clone https://github.com/paulovsm/coronaDetector.git && cd coronaDetector/ && cd / && mkdir videos && mkdir videos/input && mkdir videos/output

COPY detector.sh /

RUN chmod 755 detector.sh && cd /

ENTRYPOINT ["./detector.sh"]
