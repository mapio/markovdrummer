from __future__ import absolute_import # to allow for import from midi (the external library)

from pprint import PrettyPrinter; pp = PrettyPrinter( indent = 4 ).pprint

from math import ceil

import midi

from ..midi.utils import track2eventdict, eventdict2track, is_noteon
from ..midi.constants import pitch2part

def events2beat( events ):
	return tuple( sorted( set(
		map( lambda _: _.data[ 0 ], filter( is_noteon, events ) )
	) ) )

def beat2events( beat ):
	return [ midi.NoteOnEvent( tick = 0, channel = 9, data = [ pitch, 120 ] ) for pitch in beat ]

def beats2track( beats, tick, tick_off = None ):
	if tick_off is None: tick_off = tick / 4
	eventdict = dict()
	for n, beat in enumerate( beats ):
		events_at_tick = beat2events( beat )
		if events_at_tick: eventdict[ n * tick ] = events_at_tick
	tmp = eventdict2track( eventdict, tick_off )
	return midi.Track( tmp )

def track2beats( track, tick_per_quantum ):

	t2ed = track2eventdict( track )
	beats = []
	last_beat = 0
	for tick, events in sorted( t2ed.items() ):
		beat = tick / tick_per_quantum
		delta = beat - last_beat - 1
		if delta: beats.extend( [ tuple() ] * delta )
		events = events2beat( events )
		if events: beats.append( events )
		last_beat = beat
	return beats

def writetables( tables, path ):
	TABLE_HTML = """
	<!DOCTYPE html>
	<head>
	   <meta charset="utf-8">
	  <title>Explain</title>
	  <style>
	  	table {{
	  		  margin: 1em;
		}}
		table, td, th {{
		  border: 1pt solid black;
		  border-collapse: collapse;
		}}
		td {{
		  min-width: 1em;
  		  max-width: 1em;
		  width: 1em;
		}}
		.nob {{
		  border: none;
		}}
		.on {{
		  background-color: green;
		}}
		th {{
		  white-space: nowrap;
		  text-align: left;
		}}
	  </style>
	</head>
	<body>
	{}
	</body>
	</html>
	"""
	with open( path, 'w' ) as f: f.write( TABLE_HTML.format( '\n'.join( tables ) ) )

def beats2pitches( beats ):
	pitches = set()
	for beat in beats: pitches.update( beat )
	return sorted( pitches, reverse = True )

def beats2table( beats ):
	table = [ '<table>' ]
	if len( beats ) < 10:
		table.append( ''.join(
			[ '<th>&nbsp;' ] + [ '<th>{:02}'.format( n ) for n in range( 1, len( beats ) + 1 ) ]
		) )
	else:
		table.append( ''.join( [ '<th>&nbsp;' ] * ( len( beats ) + 1 ) ) )
	for pitch in beats2pitches( beats ):
		table.append( ''.join(
				[ '<tr><th>' + pitch2part( pitch ) ]
				+ [ '<td class=on>&nbsp;' if pitch in beat else '<td>&nbsp;' for beat in beats ]
		) )
	table.append( '</table>' )
	return '\n'.join( table )

def model2tables( model ):
	def _t( ngram, nexts, pitches ):
		table = [ '<table>' ]
		table.append( ''.join(
			[ '<th>&nbsp;<th colspan={}>ngram'.format( len( ngram ) ) ] + [ '<th>&nbsp;' ] * len( nexts )
		) )
		for pitch in pitches:
			table.append( ''.join(
					[ '<tr><th>' + pitch2part( pitch ) ]
					+ [ '<td class=on>&nbsp;' if pitch in beat else '<td>&nbsp;' for beat in ngram ]
					+ [ '<td class=on>&nbsp;' if pitch in beat else '<td>&nbsp;' for beat in nexts ]
			) )
		table.append( '</table>' )
		return '\n'.join( table )
	pitches = set()
	for ngram, nexts in model.items():
		pitches.update( beats2pitches( ngram + tuple( nexts ) ) )
	pitches = sorted( pitches, reverse = True )
	tables = []
	for ngram, nexts in model.items():
		tables.append( _t( ngram, nexts, pitches ) )
	return tables
