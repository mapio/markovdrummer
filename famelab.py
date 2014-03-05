# -*- coding: utf8 -*-

from math import floor, ceil
from sys import argv
import midi

GM10_PITCH_TO_DURMPART = dict((
   (35, 'Bass Drum 2'),
   (36, 'Bass Drum 1'),
   (37, 'Side Stick/Rimshot'),
   (38, 'Snare Drum 1'),
   (39, 'Hand Clap'),
   (40, 'Snare Drum 2'),
   (41, 'Low Tom 2'),
   (42, 'Closed Hi-hat'),
   (43, 'Low Tom 1'),
   (44, 'Pedal Hi-hat'),
   (45, 'Mid Tom 2'),
   (46, 'Open Hi-hat'),
   (47, 'Mid Tom 1'),
   (48, 'High Tom 2'),
   (49, 'Crash Cymbal 1'),
   (50, 'High Tom 1'),
   (51, 'Ride Cymbal 1'),
   (52, 'Chinese Cymbal'),
   (53, 'Ride Bell'),
   (54, 'Tambourine'),
   (55, 'Splash Cymbal'),
   (56, 'Cowbell'),
   (57, 'Crash Cymbal 2'),
   (58, 'Vibra Slap'),
   (59, 'Ride Cymbal 2'),
   (60, 'High Bongo'),
   (61, 'Low Bongo'),
   (62, 'Mute High Conga'),
   (63, 'Open High Conga'),
   (64, 'Low Conga'),
   (65, 'High Timbale'),
   (66, 'Low Timbale'),
   (67, 'High Agogô'),
   (68, 'Low Agogô'),
   (69, 'Cabasa'),
   (70, 'Maracas'),
   (71, 'Short Whistle'),
   (72, 'Long Whistle'),
   (73, 'Short Güiro'),
   (74, 'Long Güiro'),
   (75, 'Claves'),
   (76, 'High Wood Block'),
   (77, 'Low Wood Block'),
   (78, 'Mute Cuíca'),
   (79, 'Open Cuíca'),
   (80, 'Mute Triangle'),
   (81, 'Open Triangle'),
))

def is_noteoff( event ):
   return isinstance( event, midi.NoteOffEvent ) or ( isinstance( event, midi.NoteOnEvent ) and event.data[ 1 ] == 0 )

def is_noteon( event ):
   return isinstance( event, midi.NoteOnEvent ) and event.data[ 1 ] > 0

def must_keep( event ):
   return  ( isinstance( event, midi.ProgramChangeEvent ) or
      isinstance( event, midi.NoteOnEvent ) or
      isinstance( event, midi.NoteOffEvent ) or
      isinstance( event, midi.EndOfTrackEvent )
   )


def clean( track ):
   return midi.Track( filter( must_keep, track ) )

def tick2event( track ):
   res = dict()
   cum_tick = 0
   for event in track:
      cum_tick += event.tick
      if not is_noteoff( event ):
         res.setdefault( cum_tick, [] ).append( event )
   return res

def events2pitch( events ):
   return tuple( sorted(
      map( lambda _: _.data[ 1 ], filter( is_noteon, events ) )
   ) )

def cartesian( track, quantize_resolution ):

   t2e = tick2event( track )
   tick_per_quantum = max( t2e.keys() ) / quantize_resolution
   res = []

   last_beat = 0
   for tick, events in sorted( t2e.items() ):
      beat = int( ceil( tick / tick_per_quantum ) )
      if beat - last_beat > 1:
         res.extend( [ tuple() ] * ( beat - last_beat - 1 ) )
      res.append( events2pitch( events ) )
      last_beat = beat

   return res


def quantize( track, quantize_resolution ):

   t2e = tick2event( track )
   sorted_ticks = sorted( t2e.keys() )
   tick_per_quantum = sorted_ticks[ -1 ] / quantize_resolution
   tick_off = tick_per_quantum / 4

   def qt( tick ):
      return int( floor( 0.5 + ( 0.0 + tick ) / tick_per_quantum ) * tick_per_quantum )

   def add_events( events, tick ):

      def _set_tick( event, tick = 0 ):
         if not isinstance( event, midi.MetaEvent ): event = event.copy()
         event.tick = tick
         return event

      return [ _set_tick( events.pop( 0 ), tick ) ] + map( _set_tick, events )

   def to_off( events ):
      return map(
         lambda _: midi.NoteOffEvent( tick = 0, channel = 9, data = [ _.data[ 0 ], 0 ] ),
         filter( is_noteon, events )
      )

   qtick2event = dict()
   for tick in sorted_ticks:
      qtick2event.setdefault( qt( tick ), [] ).extend( t2e[ tick ] )

   qevents = []
   last_seen_qtick = 0
   for qtick, events in sorted( qtick2event.items() ):
      on = add_events( events, qtick - last_seen_qtick )
      qevents.extend( on )
      last_seen_qtick = qtick
      off = to_off( on )
      if off:
         qevents.extend( add_events( off, tick_off ) )
         last_seen_qtick += tick_off

   return midi.Track( qevents )
