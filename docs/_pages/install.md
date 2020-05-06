---
permalink: /install/

title: "Installation and use"

sidebar:
  nav: "docs"

---
## What to install

For this project you wil need two things:

- [Anaconda](https://www.anaconda.com/): an open platform geared towards scientific computing using Python, it includes Jupyter Notebook which is the platform used for this project. It also has several of the python libraries necessary for image processing such as Numpy.

- [OpenCV](https://opencv.org/): a Python library aimed at real-tiem computer vision.

## Installing anaconda

First download the Anaconda installer with Python 3.7 according to your operating system from [here](https://www.anaconda.com/products/individual)

![Anaconda installer options](/assets/images/install/installers.png)

### On Ubuntu

On the terminal move to the folder where you downloaded the installer and execute:
```
$bash Anaconda3-2020.02-Linux-x86_64.sh
```
The ouput will ask you to review the terms and services:

![Bash output](/assets/images/install/bashoutput.png)

press enter until your asked to accept he terms writing 'yes'.

Following the license agreement the prompt will suggest a location for the installation, press enter to accept the default location or specify a different one.

Once the installation is finished you will be asked if you wish the installer to initialize anaconda3 by runnig conda init, type 'yes'.

Activate the installation with:

```
$source ~/.bashrc

```
to check if the installation has been successful type:

```
$source ~/.bashrc

```
this will give a list of all the packages installed with anaconda.

### On Windows 10

Once the installer download is complete double click the installer launch

![Installer launch](/assets/images/install/installerlaunch.png)

This will open the windows installer, on the first page press next and 'I agree' to the terms and services in the next page.

![Windows Installer](/assets/images/install/windowsinstaller.png)

Then it will give you the options of install 'just for me' or for 'all users', it's recommended to install 'just for me'

![Just for me](/assets/images/install/justme.png)

Next, choose a destination folder, it should give you a default one. In advanced options choose "Register Anaconda as my default Python 3.7" and click on next.

Once it ends click finish to exit the installer. To check if the installation is correct search anaconda on the Windows search bar, it shouldo look like this:

![Search bar](/assets/images/install/searchbar.png)
