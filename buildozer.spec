[app]
title = Expense Manager
package.name = expensemanager
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 0.1
requirements = python3,kivy,arabic-reshaper,python-bidi
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
name: Build APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install system packages
        run: |
          sudo apt-get update
          sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev build-essential ccache

      - name: Install Buildozer
        run: |
          pip install --upgrade pip
          pip install buildozer cython==0.29.36 virtualenv

      - name: Build APK
        run: buildozer -v android debug

      - uses: actions/upload-artifact@v4
        with:
          name: expense-app-apk
          path: bin/*.apk
