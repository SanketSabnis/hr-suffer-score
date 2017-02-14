#!/usr/bin/python
import json
import xmltodict
from pprint import pprint
import dateutil
import datetime
import time

suffer_score_coeffs = {
    "0": 0,
    "1": 12,
    "2": 24,
    "3": 45,
    "4": 100,
    "5": 120
}

hr_zones = { 
    "0": (0, 95),
    "1": (95, 113),
    "2": (113, 132),
    "3": (132, 151),
    "4": (151, 170),
    "5": (170, 209)
}

def get_hr_zone(hr):
    for zone,bounds in hr_zones.items():
        if hr > bounds[0] and hr <= bounds[1]:
            return zone

if __name__ == "__main__":
    for gpx in ["Palos_Verdes.gpx", "Los_Angeles_Run_Cyclemeter.gpx"]:
        with open(gpx) as f:
            doc = xmltodict.parse(f.read())
            trk = doc["gpx"]["trk"]
            name = trk["name"]
            zone_time = {}
            prevstamp = None
            for pkt in trk["trkseg"]["trkpt"]:
                #t = dateutil.parser.parse(pkt["time"])
                t = datetime.datetime.strptime(pkt["time"], "%Y-%m-%dT%H:%M:%SZ")
                timestamp = int(time.mktime(t.timetuple()))
                if not prevstamp:
                    start = timestamp
                    prevstamp = timestamp
                hr = pkt["extensions"]["gpxtpx:TrackPointExtension"]["gpxtpx:hr"]
                zone = get_hr_zone(int(hr))
                zone_time[zone] = zone_time.get(zone, 0) + (timestamp - prevstamp)
                prevstamp = timestamp

            score = 0
            total_secs = 0
            for zone, secs in zone_time.items():
                score += suffer_score_coeffs[zone]*secs/3600.0
                total_secs += secs
            norm_score = score*100/float(total_secs)

            print "Activity: %s Suffer Score: %s Norm Score: %.2f Time: %s" % (name,int(score), norm_score, datetime.timedelta(seconds=total_secs))
