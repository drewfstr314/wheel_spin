|---------------|
| wheel_spin.py |
|---------------|

Drew Foster
drewfstr314@gmail.com

version 1.2.2
April 02, 2017

=========
Updates:
=========
v 1.2.1:
 * Added command-line argument support

v 1.2.2:
 * Fixed command-line argument support to use argparse (instead of poorly written custom code)
 * Changed wheel_spin.init_colors() to wheel_spin.init_colors(ncolors) to generate `ncolors` enough colors
   depending on the number of colors (equally spaced in HSV-space)
 * This also removed the need for colors.txt

===================
Required Packages:
===================
 * stdlib: argparse, random, sys, collections, time, winsound, colorsys
 * pygame (v1.9.2b1)

========================
Command-Line Arguments:
========================

-h, --help
:: display help message and descriptions for each argument

-tickets T1 T2 T3 ... TN
:: provide the ticket values for the sectors
:: Default = 1 2 3 4 5 6 7
:: Note the use of single-dash

--nr, --norandom
:: prevent the tickets being assigned to colors in a random order
:: default behavior = random

--x X
:: set the window size to X pixels across
:: Default = 1200

--y Y
:: set the window size to Y pixels high
:: Default = 900

--nfs, --nofullscreen, --window, --w
:: prevent the window from opening in fullscreen
:: default behavior = fullscreen

--nb, --nobeep
:: prevent the wheel from beeping for each ticket won
:: default behavior = beep