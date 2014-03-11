from __future__ import absolute_import # to allow for import from midi (the external library)

from collections import Counter
from math import floor, ceil
import midi

def is_noteoff( event ):
   return isinstance( event, midi.NoteOffEvent ) or ( isinstance( event, midi.NoteOnEvent ) and event.data[ 1 ] == 0 )

def is_noteon( event ):
   return isinstance( event, midi.NoteOnEvent ) and event.data[ 1 ] > 0

def must_keep( event ):
   return ( isinstance( event, midi.ProgramChangeEvent ) or
      isinstance( event, midi.NoteOnEvent ) or
      isinstance( event, midi.NoteOffEvent ) or
      isinstance( event, midi.EndOfTrackEvent )
   )

def clean( track ):
   events = []
   cum_tick = 0
   for event in track:
      if must_keep( event ):
         event.tick += cum_tick
         cum_tick = 0
         events.append( event )
      else:
         cum_tick += event.tick
   return midi.Track( events )

def eventdictstats( eventdict ):
   deltas = []
   sorted_ticks = sorted( eventdict.keys() )
   cur_tick = sorted_ticks.pop( 0 )
   for tick in sorted_ticks:
      deltas.append( tick - cur_tick )
      cur_tick = tick
   return Counter( deltas )

def track2eventdict( track ):
   eventdict = dict()
   cum_tick = 0
   for event in track:
      cum_tick += event.tick
      if not is_noteoff( event ):
         eventdict.setdefault( cum_tick, [] ).append( event )
   return eventdict

def eventdict2track( eventdict, tick_off ):

   def add_events( events, tick ):

      def _set_tick( event, tick = 0 ):
         if not isinstance( event, midi.MetaEvent ): event = event.copy()
         event.tick = tick
         event.channel = 9
         return event

      return [ _set_tick( events.pop( 0 ), tick ) ] + map( _set_tick, events )

   def _to_off( events ):
      return map(
         lambda _: midi.NoteOffEvent( tick = 0, channel = 9, data = [ _.data[ 0 ], 0 ] ),
         filter( is_noteon, events )
      )

   tevents = []
   last_tick = 0
   for tick, events in sorted( eventdict.items() ):
      on = add_events( events, tick - last_tick )
      tevents.extend( on )
      last_tick = tick
      off = _to_off( on )
      if off:
         tevents.extend( add_events( off, tick_off ) )
         last_tick += tick_off

   return midi.Track( tevents )


def quantize( track, tick_per_quantum ):

   def _qt( tick ):
      return int( floor( 0.5 + ( 0.0 + tick ) / tick_per_quantum ) * tick_per_quantum )

   t2ed = track2eventdict( track )
   qtrack2eventdict = dict()
   for tick in sorted( t2ed.keys() ):
      qtrack2eventdict.setdefault( _qt( tick ), [] ).extend( t2ed[ tick ] )

   return eventdictstats( qtrack2eventdict ), eventdict2track( qtrack2eventdict, tick_per_quantum / 4 )
