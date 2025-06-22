#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proxy module to expose the DataManager from modules.
"""
from modern_system.modules.data_manager import DataManager

# Instantiate global DataManager
# Use this singleton across the application
data_manager = DataManager()
