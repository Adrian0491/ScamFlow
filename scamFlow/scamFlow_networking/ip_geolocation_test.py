import datetime
import geopy
import json
import requests
import unittest

from datetime import *
from geopy.geocoders import Nominatim
from scamFlow.scamFlow_networking.ip_geolocation import get_geolocation
from unittest.mock import patch