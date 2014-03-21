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

from pickle import loads, dumps
from random import choice

def analyze( lst, n = 2 ):
	ngram = tuple( lst[:n] )
	model = {}
	for nxt in lst[n:]:
		model.setdefault( ngram, [] ).append( nxt )
		ngram = ngram[ 1 : ] + ( nxt, )
	return model

def generate( model, num_beats ):
	res = []
	while True:
		ngram = choice( list( model.keys() ) )
		res.extend( ngram )
		while ngram in model:
			nxt = choice( model[ ngram ] )
			ngram = ngram[ 1 : ] + ( nxt, )
			res.append( nxt )
			if len( res ) >= num_beats: return res

def load( path ):
	with open( path ) as f: return loads( f.read() )

def save( model, path ):
	with open( path, 'w' ) as f: f.write( dumps( model ) )
