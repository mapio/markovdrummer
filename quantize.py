from sys import argv

from pprint import PrettyPrinter
from json import dumps

from markovdrummer.midi import clean, quantize, track2beats, beats2track, beats2table, writetables
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

	beats = track2beats( qtrack, quantize_resoluzion )

	model = analyze( beats )
	pp( model )
	gbeats = generate( model, quantize_resoluzion * 4 )
	gtrack = beats2track( gbeats, 120 )

	gmidi = midi.Pattern(
		format = original.format,
		resolution = original.resolution,
		tracks =  [ original[ 0 ], qtrack ] if ntracks == 2 else [ gtrack ]
	)
	midi.write_midifile( 'g_' + filename, gmidi )

	writetables( [ beats2table( beats ), beats2table( gbeats ) ], filename + '.html' )
