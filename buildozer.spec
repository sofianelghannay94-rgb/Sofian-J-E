[app]
title = Expense Manager
package.name = expensemanager
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 0.1
requirements = python3,kivy,arabic-reshaper==3.0.0,python-bidi==0.4.2,six
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
