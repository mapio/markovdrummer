# -*- coding: utf8 -*-

GM10_PITCH_TO_DURMPART = dict((
   (35,'Bass Drum 2'),
   (36,'Bass Drum 1'),
   (37,'Side Stick/Rimshot'),
   (38,'Snare Drum 1'),
   (39,'Hand Clap'),
   (40,'Snare Drum 2'),
   (41,'Low Tom 2'),
   (42,'Closed Hi-hat'),
   (43,'Low Tom 1'),
   (44,'Pedal Hi-hat'),
   (45,'Mid Tom 2'),
   (46,'Open Hi-hat'),
   (47,'Mid Tom 1'),
   (48,'High Tom 2'),
   (49,'Crash Cymbal 1'),
   (50,'High Tom 1'),
   (51,'Ride Cymbal 1'),
   (52,'Chinese Cymbal'),
   (53,'Ride Bell'),
   (54,'Tambourine'),
   (55,'Splash Cymbal'),
   (56,'Cowbell'),
   (57,'Crash Cymbal 2'),
   (58,'Vibra Slap'),
   (59,'Ride Cymbal 2'),
   (60,'High Bongo'),
   (61,'Low Bongo'),
   (62,'Mute High Conga'),
   (63,'Open High Conga'),
   (64,'Low Conga'),
   (65,'High Timbale'),
   (66,'Low Timbale'),
   (67,'High Agogô'),
   (68,'Low Agogô'),
   (69,'Cabasa'),
   (70,'Maracas'),
   (71,'Short Whistle'),
   (72,'Long Whistle'),
   (73,'Short Güiro'),
   (74,'Long Güiro'),
   (75,'Claves'),
   (76,'High Wood Block'),
   (77,'Low Wood Block'),
   (78,'Mute Cuíca'),
   (79,'Open Cuíca'),
   (80,'Mute Triangle'),
   (81,'Open Triangle'),
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
   events = []
   for event in track:
      if must_keep( event ): events.append( event )
   return midi.Track( events )

def tick2event( track ):
   res = dict()
   cum_tick = 0
   for event in track:
      cum_tick += event.tick
      if not is_noteoff( event ):
         res.setdefault( cum_tick, [] ).append( event )
   return res

def quantize( track ):

   quantize_resolution = 64 * 3
   t2e = tick2event( track )
   sorted_ticks = sorted( t2e.keys() )
   max_tick = sorted_ticks[ -1 ]
   tick_per_quantum = max_tick / quantize_resolution

   def qt( tick ):
      return int( floor( 0.5 + ( 0.0 + tick ) / tick_per_quantum ) * tick_per_quantum )

   def add_events( events, tick ):
      res = []
      first = events.pop( 0 )
      first = first.copy()
      first.tick = tick
      res.append( first )
      for other in events:
         other = other.copy()
         other.tick = 0
         res.append( other )
      return res

   def to_off( events ):
      res = []
      for event in events:
         if is_noteon( event ):
            res.append( midi.NoteOffEvent( tick = 0, channel = 9, data = [ event.data[ 0 ] , 0 ] )
      return res

   qtick2event = dict()
   for tick in sorted_ticks:
      qtick2event.setdefault( qt( tick, tick_per_quantum ), [] ).extend( tick2event[ tick ] )

   qevents = []
   last_seen_qtick = 0
   for qtick, events in sorted( qtick2event.items() ):
      on = add_events( events, qtick - last_seen_qtick )
      last_seen_qtick = qtick
      off = to_off( on )
      qevents.extend( on )
      if off:
         off = add_events( off, 10 )
         qevents.extend( off )
         last_seen_qtick += 10
   return midi.Track( qevents )

original = midi.read_midifile( argv[ 1 ] )
track = clean( original[ 1 ] )
qtrack = quantize( track )
qmidi = midi.Pattern( format = 0, resolution = 240, tracks = [ qtrack ] )

print qmidi

midi.write_midifile( 'q_' + argv[ 1 ], qmidi )



