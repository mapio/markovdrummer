from sys import argv

from pprint import PrettyPrinter
from json import dumps

from markovdrummer.midi import clean, quantize, track2sym, sym2track
from markovdrummer.markov import analyze, generate

import midi

pp = PrettyPrinter( indent = 4 ).pprint

if __name__ == '__main__':

	filename = argv[ 1 ]
	quantize_resoluzion = int( argv[ 2 ] )

	original = midi.read_midifile( filename )
	ntracks = len( original )

	track = clean( original[ 1 ] if ntracks == 2 else original[ 0 ] )
	qtrack = quantize( track, quantize_resoluzion )
	qmidi = midi.Pattern(
		format = original.format,
		resolution = original.resolution,
		tracks =  [ original[ 0 ], qtrack ] if ntracks == 2 else [ qtrack ]
	)

	midi.write_midifile( 'q_' + filename, qmidi )

	sym = track2sym( qtrack, quantize_resoluzion )
	#with  open( filename + '.html', 'w' ) as f: f.write( explain( [ sym ] ) )
	model = analyze( sym )
	pp( model )
	gcart = generate( model, quantize_resoluzion * 4 )
	gtrack = sym2track( gcart, 120 )

	#with  open( 'g_' + filename + '.html', 'w' ) as f: f.write( explain( [ gcart ] ) )

	gmidi = midi.Pattern(
		format = original.format,
		resolution = original.resolution,
		tracks =  [ original[ 0 ], qtrack ] if ntracks == 2 else [ gtrack ]
	)
	midi.write_midifile( 'g_' + filename, gmidi )
