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
from markovdrummer.midi import clean, remap, quantize

def main():

	filename, basename, _ = filebaseext( argv[ 1 ] )

	original = midi.read_midifile( filename )
	track = original[ 0 ] if original.format == 0 else original[ 1 ]

	ptrack = remap( clean( track, set( [ 23 ] ) ), {
			26:42,
			46:42,
			22:42,
			40:38
		}
	)

	midi.write_midifile( basename + '.p.mid', midi.Pattern( format = 0, resolution = original.resolution, tracks = [ ptrack ] ) )
