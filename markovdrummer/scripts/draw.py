#!/usr/bin/env python

# Copyright 2014 Massimo Santini, Raffaella Migliaccio
#
# This file is part of MarkovDrummer.
#
# MarkovDrummer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MarkovDrummer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MarkovDrummer.  If not, see <http://www.gnu.org/licenses/>.

from sys import argv

import midi

from markovdrummer import filebaseext
from markovdrummer.markov import load
from markovdrummer.midi import quantize, track2beats, beats2table, model2tables, writetables

def main():

	filename, basename, ext = filebaseext( argv[ 1 ] )

	if ext == '.mid':
		original = midi.read_midifile( filename )
		track = original[ 0 ] if original.format == 0 else original[ 1 ]
		qstats, _ = quantize( track )
		tick_per_quantum = min( qstats )[ 0 ]
		print 'tick_per_quantum = {} '.format( tick_per_quantum )
		writetables( [ beats2table( track2beats( track, tick_per_quantum ) ) ], basename + ext + '.html' )
	elif ext == '.model':
		model = load( filename )
		writetables( model2tables( model ), basename + ext + '.html' )
