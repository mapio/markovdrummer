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
from markovdrummer.markov import generate, load
from markovdrummer.midi import beats2track

def main():

	filename, basename, _ = filebaseext( argv[ 1 ] )
	num_beats = int( argv[ 2 ] )
	tick_per_quantum = int( argv[ 3 ] )
	resolution = int( argv[ 4 ] )

	start, model = load( filename )
	beats = generate( model, num_beats, start )
	track = beats2track( beats, tick_per_quantum )

	midi.write_midifile(
		'{}.b{}-t{}-r{}.mid'.format( basename, num_beats, tick_per_quantum, resolution ),
		midi.Pattern( format = 0, resolution = resolution, tracks = [ track ] )
	)
