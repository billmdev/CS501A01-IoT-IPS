# CS501A01-IoT-IPS
## A Simple Indoor Positioning System

This is a little implementation software for the IoT course.
Nowadays people are constantly using their phones at nearly all times. From this observation we realized that we could determine the number of people in a given room by developing a program that sniffs Wifi beacons in the air and tell us the number of devices(people) in a room.

This program counts the number of people around you :family_man_woman_boy: by monitoring wifi signals :satellite:.

It calculates the number of people in the vicinity using the approximate number of smartphones as a proxy (since [~65% of people have smartphones nowadays](https://twitter.com/conradhackett/status/701798230619590656)). 
A cellphone is determined to be in proximity to the computer based on sniffing WiFi probe 
requests. Possible uses of this program includes: monitoring foot traffic in your house
with Raspberry Pis, seeing if your roommates are home, etc.

Tested on Linux (Raspbian and Ubuntu) and Mac OS X.


### **It may be illegal** to monitor networks for MAC addresses, especially on networks that *you do not own*. Please check your country's laws.

Getting started
===============

## Dependencies

Python 2.7 or preferably Python 3 must be installed on your machine with the `pip` command also available.
```
  python -V
  pip -V
```

### WiFi adapter that supports monitor mode

There are a number of possible USB WiFi adapters that support monitor mode. Here's a list that are popular:

- [USB Rt3070 $14](https://www.amazon.com/gp/product/B00NAXX40C/ref=as_li_tl?ie=UTF8&tag=scholl-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B00NAXX40C&linkId=b72d3a481799c15e483ea93c551742f4)
- [Panda PAU5 $14](https://www.amazon.com/gp/product/B00EQT0YK2/ref=as_li_tl?ie=UTF8&tag=scholl-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B00EQT0YK2&linkId=e5b954672d93f1e9ce9c9981331515c4)
- [Panda PAU6 $15](https://www.amazon.com/gp/product/B00JDVRCI0/ref=as_li_tl?ie=UTF8&tag=scholl-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B00JDVRCI0&linkId=e73e93e020941cada0e64b92186a2546)
- [Panda PAU9 $36](https://www.amazon.com/gp/product/B01LY35HGO/ref=as_li_tl?ie=UTF8&tag=scholl-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B01LY35HGO&linkId=e63f3beda9855abd59009d6173234918)
- [Alfa AWUSO36NH $33](https://www.amazon.com/gp/product/B0035APGP6/ref=as_li_tl?ie=UTF8&tag=scholl-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B0035APGP6&linkId=b4e25ba82357ca6f1a33cb23941befb3)
- [Alfa AWUS036NHA $40](https://www.amazon.com/gp/product/B004Y6MIXS/ref=as_li_tl?ie=UTF8&tag=scholl-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B004Y6MIXS&linkId=0277ca161967134a7f75dd7b3443bded)
- [Alfa AWUS036NEH $40](https://www.amazon.com/gp/product/B0035OCVO6/ref=as_li_tl?ie=UTF8&tag=scholl-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B0035OCVO6&linkId=bd45697540120291a2f6e169dcf81b96)
- [Sabrent NT-WGHU $15 (b/g) only](https://www.amazon.com/gp/product/B003EVO9U4/ref=as_li_tl?ie=UTF8&tag=scholl-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B003EVO9U4&linkId=06d4784d38b6bcef5957f3f6e74af8c8)

Namely you want to find a USB adapter with one of the following chipsets: Atheros AR9271, Ralink RT3070, Ralink RT3572, or Ralink RT5572.

### Mac OS X
```
  brew install wireshark
  brew cask install wireshark-chmodbpf
```

### Linux [tshark](https://www.wireshark.org/docs/man-pages/tshark.html) 
```
sudo apt-get install tshark
```

Then update it so it can be run as non-root:
```
sudo dpkg-reconfigure wireshark-common     (select YES)
sudo usermod -a -G wireshark ${USER:-root}
newgrp wireshark
```

## Install
```
pip install IPS
```


## Run

### Quickstart

To run, simply type in
```bash
$ IPS
Using wlan1 adapter and scanning for 60 seconds...
[==================================================] 100%        0s left
There are about 3 people around.
```

You will be prompted for the WiFi adapter to use for scanning. Make sure to use
an adapter that supports "monitor" mode.


### Options

You can modify the scan time, designate the adapter, or modify the output using some command-line options.
```bash
$ IPS --help

Options:
  -a, --adapter TEXT   adapter to use
  -z, --analyze TEXT   analyze file
  -s, --scantime TEXT  time in seconds to scan
  -o, --out TEXT       output cellphone data to file
  -v, --verbose        verbose mode
  --number             just print the number
  -j, --jsonprint      print JSON of cellphone data
  -n, --nearby         only quantify signals that are nearby (rssi > -70)
  --nocorrection       do not apply correction
  --loop               loop forever
  --sort               sort cellphone data by distance (rssi)
```

### Print JSON

You can generate an JSON-formatted output to see what kind of phones are around:
```bash
$ IPS -o test.json -a wlan1
[==================================================] 100%         0s left
There are about 4 people around.
$ cat test.json | python3 -m json.tool
[
  {
    "rssi": -86.0,
    "mac": "90:e7:c4:xx:xx:xx",
    "company": "HTC Corporation"
  },
  {
    "rssi": -84.0,
    "mac": "80:e6:50:xx:xx:xx",
    "company": "Apple, Inc."
  },
  {
    "rssi": -49.0,
    "mac": "ac:37:43:xx:xx:xx",
    "company": "HTC Corporation"
  }
]
```

A higher rssi means closer devices to the raspberry. 

### Run forever

You can add `--loop` to make this run forever and append new lines an output file, `test.json`:
```bash
$ IPS -o test.json -a wlan1 --loop
```

### Visualize 

You can visualize the output from a looped command via a browser using:
```bash
$ IPS --analyze test.json 
Wrote index.html
Open browser to http://localhost:8001
Type Ctl+C to exit
```

Then just open up `index.html` in a browser and you should see plots.


How does it work?
==================

It counts the number of probe requests coming from cellphones in a given amount of time.
The probe requests can be "sniffed" from a monitor-mode enabled WiFi adapter using `tshark`. An acccurate count does depend on everyone having cellphone and also scanning long enough (1 - 10 minutes) to capture the packet when a phone pings the WiFi network (which happens every 1 to 10 minutes unless the phone is off or WiFi is disabled).

This is a barebones program as it can be extended to add localization functionalities and show the positions of devices(people) visually on a map.