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

def _ts( tpl ):
	return ''.join( map( str, tpl ) )

def draw( model, decorated = False ):
	name2node = {}
	def node( beat ):
	        if beat in name2node: return name2node[ beat ]
	        v = GRAPH.new_vertex()
	        if decorated: GRAPH.set_vertex_attribute( v, 'label', _ts( beat ) )
	        name2node[ beat ] = v
	        return v
	def edge( src, dst, step = None ):
		e = GRAPH.new_edge( node( src ), node( dst ) )
		if e > 0 and decorated: GRAPH.set_edge_attribute( e, 'label', _ts( step ) )
	GRAPH.clear()
	GRAPH.set_vertex_style_attribute( 0, 'shape', 'sphere' )
	GRAPH.set_vertex_style_attribute( 0, 'fontsize', '24' )
	GRAPH.set_edge_style_attribute( 0, 'color', '#ffffff' )
	GRAPH.set_edge_style_attribute( 0, 'width', '5.0' )
	GRAPH.set_edge_style_attribute( 0, 'fontsize', '18' )
	GRAPH.set_edge_style_attribute( 0, 'spline', 'true' )

	for src, beats in model.items():
		for dst in beats:
			edge( src, src[1:] + ( dst, ), dst )

