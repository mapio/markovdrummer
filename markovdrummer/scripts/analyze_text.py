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

from markovdrummer import filebaseext
from markovdrummer.markov import analyze, save

def main():

	filename, basename, _ = filebaseext( argv[ 1 ] )
	memory = int( argv[ 2 ] )

	with open( filename, 'r' ) as f:
		chars = f.read()

	start_model = analyze( chars, memory )

	save( start_model, '{}.text-m{}.model'.format( basename, memory ) )

