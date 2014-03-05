from __future__ import absolute_import # to allow for import from midi (the external library)

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
   return midi.Track( filter( must_keep, track ) )

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

   events = []
   last_tick = 0
   for tick, events in sorted( eventdict.items() ):
      on = add_events( events, tick - last_tick )
      events.extend( on )
      last_tick = tick
      off = _to_off( on )
      if off:
         events.extend( add_events( off, tick_off ) )
         last_tick += tick_off

   return midi.Track( events )


def quantize( track, quantize_resolution ):

   t2ed = track2eventdict( track )
   sorted_ticks = sorted( t2ed.keys() )
   tick_per_quantum = sorted_ticks[ -1 ] / quantize_resolution

   def _qt( tick ):
      return int( floor( 0.5 + ( 0.0 + tick ) / tick_per_quantum ) * tick_per_quantum )

   qtrack2eventdict = dict()
   for tick in sorted_ticks:
      qtrack2eventdict.setdefault( _qt( tick ), [] ).extend( t2ed[ tick ] )

   return eventdict2track( qtrack2eventdict, tick_per_quantum / 4 )
