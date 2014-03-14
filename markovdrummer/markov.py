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
