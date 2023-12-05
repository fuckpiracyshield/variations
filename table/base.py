import sys
import os

current = os.path.dirname('../')
sys.path.append(current)

from util.airtable_request import AirtableRequest

class Base:

    request = None

    def __init__(self):
        self.request = AirtableRequest()
