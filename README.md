# find-broken-desktop

Find desktop entry files (\*.desktop) with broken executables.
By default searches common applications directories as well as some autostart directories.

Can be used to check a single \*.desktop file or preset folders.

Forked https://github.com/AndyCrowd/fbrokendesktop with the following changes:

-  Written in python and use pyxdg for better portability
-  Improved command line interface
-  Added option to list only entries owned by the current user
