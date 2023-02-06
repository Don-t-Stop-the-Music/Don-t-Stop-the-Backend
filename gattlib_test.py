#!/usr/bin/python3

"""PyBluez ble example beacon.py
Advertises a bluethooth low energy beacon for 60 seconds.
"""



import time

from gattlib import BeaconService

service = BeaconService()

service.start_advertising("11111111-2222-3333-4444-555555555555",1, 1, 1, 200)
time.sleep(60)

service.stop_advertising()

print("Done.") 
