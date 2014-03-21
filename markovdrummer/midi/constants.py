# -*- coding: utf8 -*-

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


GM10_PITCH_TO_DURMPART = {
   22: '[Roland Closed Hi-hat]',
   23: '[Roland mute]',
   26: '[Roland Open Hi-hat]',
   35: 'Bass Drum 2',
   36: 'Bass Drum 1',
   37: 'Side Stick/Rimshot',
   38: 'Snare Drum 1',
   39: 'Hand Clap',
   40: 'Snare Drum 2',
   41: 'Low Tom 2',
   42: 'Closed Hi-hat',
   43: 'Low Tom 1',
   44: 'Pedal Hi-hat',
   45: 'Mid Tom 2',
   46: 'Open Hi-hat',
   47: 'Mid Tom 1',
   48: 'High Tom 2',
   49: 'Crash Cymbal 1',
   50: 'High Tom 1',
   51: 'Ride Cymbal 1',
   52: 'Chinese Cymbal',
   53: 'Ride Bell',
   54: 'Tambourine',
   55: 'Splash Cymbal',
   56: 'Cowbell',
   57: 'Crash Cymbal 2',
   58: 'Vibra Slap',
   59: 'Ride Cymbal 2',
   60: 'High Bongo',
   61: 'Low Bongo',
   62: 'Mute High Conga',
   63: 'Open High Conga',
   64: 'Low Conga',
   65: 'High Timbale',
   66: 'Low Timbale',
   67: 'High Agogô',
   68: 'Low Agogô',
   69: 'Cabasa',
   70: 'Maracas',
   71: 'Short Whistle',
   72: 'Long Whistle',
   73: 'Short Güiro',
   74: 'Long Güiro',
   75: 'Claves',
   76: 'High Wood Block',
   77: 'Low Wood Block',
   78: 'Mute Cuíca',
   79: 'Open Cuíca',
   80: 'Mute Triangle',
   81: 'Open Triangle',
}

def pitch2part( pitch ):
   if pitch in GM10_PITCH_TO_DURMPART:
      return '{} ({})'.format( GM10_PITCH_TO_DURMPART[ pitch ], pitch )
   else:
      return '{}'.format( pitch )
