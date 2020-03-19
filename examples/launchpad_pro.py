#!/usr/bin/env python3
#
# Launchpad Pro tests
# 
#
# FMMT666(ASkr) 7/2013..2/2018
# www.askrprojects.net
#

import sys

try:
	import launchpad_py as launchpad
except ImportError:
	try:
		import launchpad
	except ImportError:
		sys.exit("ERROR: loading launchpad.py failed")

import random
import time


def CountdownPrint( n ):
	for i in range(n,0,-1):
		sys.stdout.write( str(i) + " ")
		sys.stdout.flush()
		time.sleep(0.001 * 500)


def main():

	# some basic info
	print( "\nRunning..." )
	print( " - Python " + str( sys.version.split()[0] ) )

	# create an instance
	lp = launchpad.LaunchpadPro();

	# open the first Launchpad Pro
	if lp.Open( 0, "pro" ):
		print( " - Launchpad Pro: OK" )
	else:
		print( " - Launchpad Pro: ERROR" )
		return

	# Clear the buffer because the Launchpad remembers everything
	lp.ButtonFlush()

	# List the class's methods
	print( " - Available methods:" )
	for mName in sorted( dir( lp ) ):
		if mName.find( "__") >= 0:
			continue
		if callable( getattr( lp, mName ) ):
			print( "     " + str( mName ) + "()" )

	# LedAllOn() test
	print( " - Testing LedAllOn()" )
	for i in [ 5, 21, 79, 3]:
		lp.LedAllOn( i )
		time.sleep(0.001 * 500)

	# LedCtrlXY() test
	# -> LedCtrlRaw()
	#    -> midi.RawWriteSysEx()
	#       -> devOut.write_sys_ex()
	print( " - Testing LedCtrlXY(), Pro Mode" )
	colors = [ [63,0,0],[0,63,0],[0,0,63],[63,63,0],[63,0,63],[0,63,63],[63,63,63] ]
	for i in range(5):
		for y in range( i, 10 - i ):
			for x in range( i, 10 - i ):
				lp.LedCtrlXY( x, y, colors[i][0], colors[i][1], colors[i][2], mode = "pro" )
		time.sleep(0.001 * 500)

	print( " - Testing LedCtrlXY(), Classic Mode" )
	for i in range(4,-1,-1):
		for y in range( i, 10 - i ):
			for x in range( i, 10 - i ):
				if x == 0:
					x = 10
				lp.LedCtrlXY( x-1, y, colors[3-i+2][0], colors[4-i+2][1], colors[4-i+2][2] )
		time.sleep(0.001 * 500)

	i = 1
	for y in range( i, 10 - i ):
		for x in range( i, 10 - i ):
			lp.LedCtrlXY( x, y, 0, 0, 0, mode = "pro" )
	time.sleep(0.001 * 100)

	# LedCtrlChar() test
	# -> LedCtrlRaw()
	#    -> midi.RawWriteSysEx()
	#       -> devOut.write_sys_ex()
	print( " - Testing LedCtrlChar()" )
	for i in range( -7, 7, 1):
		lp.LedCtrlChar( 'A', 63, 0, 0, i, 0 )
		if   i == -6:
			print( "   - left edge" )
			time.sleep(0.001 * 2000)
		elif i ==  6:
			print( "   - right edge" )
			time.sleep(0.001 * 2000)
		else:
			time.sleep(0.001 * 250)
	lp.LedAllOn( 0 )

	# LedCtrlRawByCode() test
	# -> midi.RawWrite()
	#    -> devOut.write_short()
	print( " - Testing LedCtrlRawByCode()" )
	print( "   - matrix" )
	for y in range( 10, 90, 10 ):
		for x in range(8):
			lp.LedCtrlRawByCode( y + x + 1, x+y )
			time.sleep(0.001 * 50)
	print( "   - bottom" )
	for i in range( 1, 9, 1 ):
		lp.LedCtrlRawByCode( i, 5 )
		time.sleep(0.001 * 200)
	print( "   - right" )
	for i in range( 19, 99, 10 ):
		lp.LedCtrlRawByCode( i, 17 )
		time.sleep(0.001 * 200)
	print( "   - top" )
	for i in range( 98, 90, -1 ):
		lp.LedCtrlRawByCode( i, 79 )
		time.sleep(0.001 * 200)
	print( "   - left" )
	for i in range( 80, 0, -10 ):
		lp.LedCtrlRawByCode( i, 3 )
		time.sleep(0.001 * 200)


	time.sleep(0.001 * 2000)

	# turn all LEDs off
	print( " - Testing Reset()" )
	lp.Reset()

	# close this instance
	print( " - More to come, goodbye...\n" )
	lp.Close()


if __name__ == '__main__':
	main()

