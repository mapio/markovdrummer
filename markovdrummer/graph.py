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

# this package draws the model graph using http://ubietylab.net/ubigraph/

import xmlrpclib

SERVER_URL = 'http://127.0.0.1:20738/RPC2'
GRAPH = xmlrpclib.Server( SERVER_URL ).ubigraph

def draw( model ):
	name2node = {}
	def node( beat ):
	        if beat in name2node: return name2node[ beat ]
	        v = GRAPH.new_vertex()
	        name2node[ beat ] = v
	        return v
	def edge( src, dst ):
		GRAPH.new_edge( node( src ), node( dst ) )
	GRAPH.clear()
	for src, beats in model.items():
		succ = src
		for dst in beats:
			prec, succ = succ, succ[1:] + ( dst, )
			edge( prec, succ )

if __name__ == '__main__':
	from sys import argv
	from markovdrummer.markov import load
