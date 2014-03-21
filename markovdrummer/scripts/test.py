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

import midi

from markovdrummer.midi import track2eventdict, eventdict2track, track2beats, beats2track

def main():

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
