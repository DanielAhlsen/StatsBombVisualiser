#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd

class SearchEngine:

    def __init__(events_path,matches_path,lineup_path,competitions_path,self):
        self.EVENTS_PATH = events_path
        self.MATCHES_PATH = matches_path
        self.LINEUP_PATH = lineup_path
        self.COMPETITIONS_PATH = competitions_path

    def loadCompetitions(self):
        competitions = pd.read_json(DATA+"competitions.json", convert_dates=True)

    def loadMatches(self):
        
        pass

