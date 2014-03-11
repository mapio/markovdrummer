from pprint import PrettyPrinter; pp = PrettyPrinter( indent = 4 ).pprint

import midi

from markovdrummer.midi import track2eventdict, eventdict2track, track2beats, beats2track

track = [
	midi.NoteOnEvent(tick=0, channel=9, data=[36, 64]),
	midi.NoteOnEvent(tick=0, channel=9, data=[42, 64]),
	midi.NoteOffEvent(tick=10, channel=9, data=[36, 0]),
	midi.NoteOffEvent(tick=0, channel=9, data=[42, 0]),

	midi.NoteOnEvent(tick=90, channel=9, data=[42, 64]),
	midi.NoteOffEvent(tick=10, channel=9, data=[42, 0]),

	midi.NoteOnEvent(tick=90, channel=9, data=[38, 64]),
	midi.NoteOnEvent(tick=0, channel=9, data=[42, 64]),
	midi.NoteOffEvent(tick=10, channel=9, data=[38, 0]),
	midi.NoteOffEvent(tick=0, channel=9, data=[42, 0]),

	midi.NoteOnEvent(tick=90, channel=9, data=[42, 64]),
	midi.NoteOffEvent(tick=10, channel=9, data=[42, 0]),

	midi.NoteOnEvent(tick=90, channel=9, data=[36, 64]),
	midi.NoteOnEvent(tick=0, channel=9, data=[42, 64]),
	midi.NoteOffEvent(tick=10, channel=9, data=[36, 0]),
	midi.NoteOffEvent(tick=0, channel=9, data=[42, 0]),

	#midi.NoteOnEvent(tick=90, channel=9, data=[42, 64]),
	#midi.NoteOffEvent(tick=10, channel=9, data=[42, 0]),

	midi.NoteOnEvent(tick=190, channel=9, data=[38, 64]),
	midi.NoteOnEvent(tick=0, channel=9, data=[42, 64]),
	midi.NoteOffEvent(tick=10, channel=9, data=[38, 0]),
	midi.NoteOffEvent(tick=0, channel=9, data=[42, 0]),

	midi.NoteOnEvent(tick=90, channel=9, data=[42, 64]),
	midi.NoteOffEvent(tick=10, channel=9, data=[42, 0]),
	midi.EndOfTrackEvent(tick=90, data=[])
]

midi.write_midifile(
	'test.mid',
	midi.Pattern( format = 0, resolution = 100, tracks = [ track ] )
)

print track == eventdict2track( track2eventdict( track ), 10 )

beats = track2beats( track, 100 )

print  track[:-1] == beats2track( beats, 100, 10 )
