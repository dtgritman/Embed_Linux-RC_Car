## Setup 

Each part of the project is modularised for efficiency and fault prevention. This means each part (the nerf_module object_detection and rc_car) can work as a standalone part.  

### Raspberry Pi - Setup

##### Webserver dependencies  
The webserver requires flask to run if not already installed. To install flask you can use the command  
`~$ sudo apt-get install python-flask`

#### Hotspot Setup
We wanted to not be reliant on a router to connect to our Pi so we turned it into a hotspot to connect to it without our home or school wifi.

##### Access point in a standalone network (NAT)
**Note**: This is a short version of the raspberrypi.org tutorial. More information, it can be found [here](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md)

##### 1. Installs
Update your Pi
```bash
~$ sudo apt-get update
~$ sudo apt-get upgrade
```

Install all the required software:

```bash
~$ sudo apt-get install dnsmasq hostapd
```

Turn the new software off as follows:
```bash
~$ sudo systemctl stop dnsmasq
~$ sudo systemctl stop hostapd
```

To ensure that an updated kernel is configured correctly after install, reboot:
```bash
~$ sudo reboot 
```

##### 2. Configuring a static IP

This documentation assumes that we are using the standard 192.168.x.x IP addresses for our wireless network, so we will assign the server the IP address 192.168.4.1. It is also assumed that the wireless device being used is **wlan0**.

To configure the static IP address, edit the dhcpcd configuration file with:
```bash 
~$ sudo nano /etc/dhcpcd.conf
```

Go to the end of the file and edit it so that it looks like:

```
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
```
Now restart the dhcpcd daemon and set up the new wlan0 configuration:

```bash
~$ sudo service dhcpcd restart
```
##### 3. Configuring the DHCP server (dnsmasq)

The DHCP service is provided by dnsmasq. By default, the configuration file contains a lot of information that is not needed, and it is easier to start from scratch. Rename this configuration file, and edit a new one:

```bash 
~$ sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig  
~$ sudo nano /etc/dnsmasq.conf
```

Type or copy the following information into the dnsmasq configuration file and save it:
```
interface=wlan0      # Use the require wireless interface
  dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
```
So for **wlan0**, we are going to provide IP addresses between 192.168.4.2 and 192.168.4.20, with a lease time of 24 hours. If you are providing DHCP services for other network devices (e.g. eth0), you could add more sections with the appropriate interface header, with the range of addresses you intend to provide to that interface.

##### 4. Configuring the access point host software (hostapd)

You need to edit the hostapd configuration file. After initial install, this will be a new/empty file.

```bash
~$ sudo nano /etc/hostapd/hostapd.conf
```
Add the information below to the configuration file. This configuration assumes we are using channel 7, with a network name of **HumanVsZombies**, and a password **letmeinrightnow**. Note that the name and password should not have quotes around them. The passphrase should be between 8 and 64 characters in length.

```
interface=wlan0
driver=nl80211
ssid=HumanVsZombies
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=letmeinrightnow
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```
We now need to tell the system where to find this configuration file.

```bash 
~$ sudo nano /etc/default/hostapd
```
Find the line with #DAEMON_CONF, and replace it with this:
```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```


**Now start up the remaining services:**

```bash
~$ sudo systemctl start hostapd
~$ sudo systemctl start dnsmasq
```

**Add routing and masquerade**

Edit /etc/sysctl.conf and uncomment this line:

```
net.ipv4.ip_forward=1
```

Add a masquerade for outbound traffic on eth0:
```bash
~$ sudo iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
```
Save the iptables rule.
```bash
~$ sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```
Edit _**/etc/rc.local**_ and add this just above **"exit 0"** to install these rules on boot.
```
iptables-restore < /etc/iptables.ipv4.nat
```
**Reboot**

The network SSID you specified in the hostapd configuration should now be present, and it should be accessible with the specified password.

If SSH is enabled on the Raspberry Pi access point, it should be possible to connect to it from another Linux box (or a system with SSH connectivity present) as follows, assuming the pi account is present:
```bash
~$ ssh pi@192.168.4.1
```
By this point, the Raspberry Pi is acting as an access point, and other devices can associate with it. Associated devices can access the Raspberry Pi access point via its IP address for operations such as rsync, scp, or ssh.

#### Potental Error
If you are having an issue with logging into the wifi you need to manually set you the ipv4 password.
