from __future__ import absolute_import # to allow for import from midi (the external library)

import midi

def events2pitch( events ):
   return tuple( sorted(
      map( lambda _: _.data[ 0 ], filter( is_noteon, events ) )
   ) )

def sym2track( cartesian, tick, tick_off = None ):
   if tick_off is None: tick_off = tick / 4
   dd = dict()
   for n, beat in enumerate( cartesian ):
      print n, beat
      events_at_tick = []
      for note in beat:
         events_at_tick.append( midi.NoteOnEvent( tick = 0, channel = 9, data = [ note, 64 ] ) )
      if events_at_tick: dd[ n * tick ] = events_at_tick
   return midi.Track( PIPPO( dd, tick_off ) )

def track2sym( track, quantize_resolution ):

   t2ed = track2eventdict( track )
   tick_per_quantum = max( t2ed.keys() ) / quantize_resolution
   res = []

   last_beat = 0
   for tick, events in sorted( t2ed.items() ):
      beat = int( ceil( tick / tick_per_quantum ) )
      delta = beat - last_beat - 1
      if delta: res.extend( [ tuple() ] * delta )
      res.append( events2pitch( events ) )
      last_beat = beat

   return res

   TABLE_HTML = """
<!DOCTYPE html>
<head>
   <meta charset="utf-8">
  <title>Explain</title>
  <style>
    table, td, th {{
      border: 1pt solid black;
      border-collapse: collapse;
      margin: 1em;
    }}
    td {{
      width: 1em;
    }}
    .nob {{
      border: none;
    }}
    .on {{
      background-color: green;
    }}
    th {{
      text-align: left;
    }}
  </style>
</head>
<body>
{}
</body>
</html>
"""

def explain( cartesians ):
   def _explain( cartesian ):
      notes = set()
      for beat in cartesian:
         notes.update( beat )
      notes = sorted( notes, reverse = True )
      table = [ '<table>' ]
      table.append( ''.join(
         [ '<th>&nbsp;' ] + [ '<th>{}'.format( n ) for n, beat in enumerate( cartesian, 1 ) ]
      ) )
      for note in notes:
         table.append( ''.join(
            [ '<tr><th>{}'.format( GM10_PITCH_TO_DURMPART[ note ] if note in GM10_PITCH_TO_DURMPART else note ) ]
            + [ '<td class=on>&nbsp;' if note in beat else '<td>&nbsp;' for beat in cartesian ]
          ) )
      table.append( '</table>' )
      return '\n'.join( table )
   return TABLE_HTML.format( ' \n '.join( [ _explain( _ ) for _ in cartesians ] ) )


