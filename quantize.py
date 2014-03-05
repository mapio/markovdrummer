from sys import argv

from pprint import PrettyPrinter
from json import dumps

from markovdrummer.midi import clean, quantize, track2sym, sym2track
from markovdrummer.makov import analyze, generate

import midi

pp = PrettyPrinter( indent = 4 ).pprint

if __name__ == '__main__':

	original = midi.read_midifile( argv[ 1 ] )
	ntracks = len( original )

	if ntracks == 2:
		track = clean( original[ 1 ] )
	else:
		track = clean( original[ 0 ] )

	qtrack = quantize( track, int( argv[ 2 ] ) )
	if ntracks == 2:
		qmidi = midi.Pattern( format = original.format, resolution = original.resolution, tracks = [ original[ 0 ], qtrack ] )
	else:
		qmidi = midi.Pattern( format = original.format, resolution = original.resolution, tracks = [ qtrack ] )

	midi.write_midifile( 'q_' + argv[ 1 ], qmidi )

	# cart = cartesian( qtrack, int( argv[ 2 ] ) )
	# with  open( argv[ 1 ] + '.html', 'w' ) as f:
	#   f.write( explain( [ cart ] ) )
	# model = analyze( cart )
	# pp( model )
	# gcart = generate( model, int( argv[ 2 ] ) * 4 )
	# gtrack = cart2midi( gcart, 120 )

	# with  open( 'g_' + argv[ 1 ] + '.html', 'w' ) as f:
	#   f.write( explain( [ gcart ] ) )

	# if ntracks == 2:
	# 	gmidi = midi.Pattern( format = original.format, resolution = original.resolution, tracks = [ original[ 0 ], gtrack ] )
	# else:
	# 	gmidi = midi.Pattern( format = original.format, resolution = original.resolution, tracks = [ gtrack ] )

	# midi.write_midifile( 'g_' + argv[ 1 ], gmidi )
