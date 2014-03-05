# -*- coding: utf8 -*-

from sys import argv

from famelab import clean, quantize, cartesian
import midi

if __name__ == '__main__':

   original = midi.read_midifile( argv[ 1 ] )
   track = clean( original[ 1 ] )
   qtrack = quantize( track, int( argv[ 2 ] ) )
   qmidi = midi.Pattern( format = original.format, resolution = original.resolution, tracks = [ original[ 0 ], qtrack ] )
   midi.write_midifile( 'q_' + argv[ 1 ], qmidi )
   print cartesian( qtrack, int( argv[ 2 ] ) )


