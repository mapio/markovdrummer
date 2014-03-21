Markov drummer
==============

This is a **highly experimental** educational package that explores
algorithmic generation of *drum grooves* using *Markov chains*.

The idea is that, given a MIDI file containing a drum goorve, one can obtain a
Markov chain modeling the beat and then use such model to generate new
(original) beats. It is also possible to "merge" different chains to obtain a
kind of "fusion" of different grooves.

How to use the package
----------------------

First download and uncompress the latest release with

	curl -sLO https://github.com/mapio/markovdrummer/archive/master.zip
	unzip master.zip
	rm -f master.zip

then create a [virtualenv](http://www.virtualenv.org/en/latest/)

	mkvirtualenv markovdrummer

and install the reqiurements using

	pip install -r requirements

finally, install this package as

	pip install .

Once this steps are performed, you can for instance analyze and generate a
groove for instance as

	preprocess data/bossa.mid
	stats bossa.p.mid
	quantize bossa.p.mid 240
	analyze bossa.p.q240.mid 120 2
	generate bossa.p.q240.t120-m2.model 100 240 480

where

* the fist step cleans the MIDI file (removing extra events and remapping some pitches),
* the second steps allows you to get the most frequent interval among ticks (that you'll be going to use a the quantization interval in the next step)
* the third step performs time quantization,
* the fouth step computes the Markov chain,
* the last step generates a new beat using the chain obtained at the previous step.

If you have installed [fluidsynth](http://sourceforge.net/apps/trac/fluidsynth/)
and obtained a suitable [soundfont](http://sourceforge.net/apps/trac/fluidsynth/wiki/SoundFont) file, you can then listen to the generated beat using

	fluidsynth -i path/to/soundfont.sf2 bossa.p.q240.t120-m2.b100-t240-r480.mid

