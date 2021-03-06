#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import os
import inspect

from core._time import now
from config import api_configuration
from lib.ip2location import IP2Location

client = pymongo.MongoClient(
    api_configuration()["api_database"],
    serverSelectionTimeoutMS=api_configuration()["api_database_connection_timeout"]
)
database = client[api_configuration()["api_database_name"]]
honeypot_events = database.honeypot_events
network_events = database.network_events
IP2Location = IP2Location.IP2Location(
    os.path.join(
        os.path.dirname(
            inspect.getfile(IP2Location)
        ),
        "IP2LOCATION-LITE-DB1.BIN")
)


def insert_selected_modules_network_event(ip, port, module_name):
    """
    insert selected modules event to honeypot_events collection

    Args:
        ip: connected ip
        port: connected port
        module_name: module name ran on the port

    Returns:
        ObjectId(inserted_id)
    """
    return honeypot_events.insert_one(
        {
            "ip": ip,
            "port": int(port),
            "module_name": module_name,
            "date": now(),
            "country": IP2Location.get_country_short(ip)
        }
    ).inserted_id


def insert_other_network_event(ip, port):
    """
    insert other network events (port scan, etc..) to network_events collection

    Args:
        ip: connected ip
        port: connected port

    Returns:
        ObjectId(inserted_id)
    """
    return network_events.insert_one(
        {
            "ip": ip,
            "port": int(port),
            "date": now(),
            "country": IP2Location.get_country_short(ip)
        }
    ).inserted_id
