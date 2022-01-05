#! /bin/bash

wl pkteng_stop tx
wl down
wl band auto
wl mpc 0
wl country ALL
wl mimo_txbw 4
wl $1 $2
wl bi 65535
wl up
wl phy_watchdog 0
wl scansuppress 1
wl phy_forcecal 1
wl reset_cnts

