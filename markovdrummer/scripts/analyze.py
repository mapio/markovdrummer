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
from markovdrummer.markov import analyze, save
from markovdrummer.midi import track2beats

def main():

	filename, basename, _ = filebaseext( argv[ 1 ] )
	tick_per_quantum = int( argv[ 2 ] )
	memory = int( argv[ 3 ] )

	original = midi.read_midifile( filename )

	beats = track2beats( original[ 0 ], tick_per_quantum )
	model = analyze( beats, memory )

	save( model, '{}.t{}-m{}.model'.format( basename, tick_per_quantum, memory ) )

