# Compiling OpenCV 3.4.1 on a Raspberry pi

## Step 1: Extend your disk before proceeding

    $ sudo raspi-config

Go to "Advanced Options"
Select "Expand Filesystem", hit enter
Reboot your pi:

    $ sudo reboot

## Step 2: Reclaim space by removing LibreOffice and Wolfram Engine

    $ sudo apt-get purge wolfram-engine
    $ sudo apt-get purge libreoffice*
    $ sudo apt-get clean
    $ sudo apt-get autoremove

## Step 3: Install dependencies

    $ sudo apt-get update && sudo apt-get upgrade
    $ sudo apt-get install build-essential cmake pkg-config
    $ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
    $ sudo apt-get install libavcodec-dev libavformat-dev libswscale-de libv4l-dev
    $ sudo apt-get install libxvidcore-dev libx264-dev
    $ sudo apt-get install libgtk2.0-dev libgtk-3-dev
    $ sudo apt-get install libcanberra-gtk*
    $ sudo apt-get install libatlas-base-dev gfortran
    $ sudo apt-get install python2.7-dev python3-dev

    # Installs pip and NumPy
    $ wget https://bootstrap.pypa.io/get-pip.py
    $ sudo python get-pip.py
    $ pip install numpy

## Step 4: Download the OpenCV Source Code

    $ cd ~
    $ wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.1.zip
    $ unzip opencv.zip
    $ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.1.zip
    $ unzip opencv_contrib.zip

## Step 5: Increase size of swap file

    $ sudo nano /etc/dphys-swapfile

    # change the CONF_SWAPSIZE to 1024 from 100
    CONF_SWAPSIZE=1024

**Note:** Undo this setting once the compile is complete 

**Back up your SD Card, as increasing the size of the swap file will shorten the lifespan of your SD Card and can potentially corrupt it as well**

Restart the swap service

    $ sudo /etc/init.d/dphys-swapfile stop
    $ sudo /etc/init.d/dphys-swapfile start

## Step 6: Compile and install optimized OpenCV

    $ cd ~/opencv-3.4.1/
    $ mkdir build
    $ cd build
    $ cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.1/modules \
        -D ENABLE_NEON=ON \
        -D ENABLE_VFPV3=ON \
        -D BUILD_TESTS=OFF \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D BUILD_EXAMPLES=OFF ..
    $ sudo make -j4

If you encounter any issues while compiling, run

    $ sudo make clean
    $ sudo make

Remember to restore the swap size back to 100 and restart the swap service

## Step 7: Install the build

    $ sudo make install
    $ sudo ldconfig
    $ sudo nano /etc/ld.so.conf.d/opencv.conf

Add the following line to opencv.conf

    /usr/local/lib          # enter this in opencv.conf, NOT at the command line
                            (leave a blank line at the end of opencv.conf)
Save and exit by hitting CTRL+X, Y and then ENTER

    $ sudo ldconfig
    $ sudo nano /etc/bash.bashrc

add the following lines at the bottom of bash.bashrc

    PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig
    export PKG_CONFIG_PATH

(leave a blank line at the end of bash.bashrc)

Save and exit (CTRL+X, Y and then ENTER)

## Step 8: Reboot and verify installation

    $ sudo reboot
    $ python
    >>> import cv2
    >>> print cv2.__version__
The output should be

    '3.4.1'

## Done