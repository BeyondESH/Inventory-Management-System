#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
食品服务公司管理系统安装脚本
"""

from setuptools import setup, find_packages

setup(
    name="inventory-management-system",
    version="2.0.0",
    description="食品服务公司管理系统",
    author="Developer",
    author_email="developer@company.com",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        # tkinter is usually included with Python
    ],
    entry_points={
        "console_scripts": [
            "inventory-system=src.system_launcher:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
