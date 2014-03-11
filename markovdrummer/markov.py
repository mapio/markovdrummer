from pickle import loads, dumps
from random import choice

def analyze( lst, n = 2 ):
	ngram = tuple( lst[:n] )
	model = {}
	for nxt in lst[n:]:
		model.setdefault( ngram, [] ).append( nxt )
		ngram = ngram[ 1 : ] + ( nxt, )
	return model

def generate( model, max_beats ):
	ngram = choice( list( model.keys() ) )
	res = []
	res.extend( ngram )
	while ngram in model and len( res ) < max_beats:
		nxt = choice( model[ ngram ] )
		ngram = ngram[ 1 : ] + ( nxt, )
		res.append( nxt )
	return res

def load( path ):
	with open( path ) as f: return loads( f.read() )

def save( model, path ):
	with open( path, 'w' ) as f: f.write( dumps( model ) )
