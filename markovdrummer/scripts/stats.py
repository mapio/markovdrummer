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

from markovdrummer.midi import quantize, trackstats, pitch2part

def main():

	filename = argv[ 1 ]

	original = midi.read_midifile( filename )

	print 'format: {}\nresolution: {}'.format( original.format, original.resolution )

	for n, track in enumerate( original ):

		qstats, _ = quantize( track )
		print 'track #{} qstats:'.format( n )
		for delta, count in qstats:
			print '\ttick {}: # {}'.format( delta, count )

		print 'track #{} pitches:'.format( n )
		for pitch, count in trackstats( track ):
			print '\tpitch {}: # {}'.format( pitch2part( pitch ), count )
