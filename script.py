import pygame
from music21 import converter, instrument, note, chord
from mido import MidiFile
import numpy
import glob
import pickle
pygame.init()

# get trigrams from midi file

NOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', ' '] # all notes + gap



mid = MidiFile('midi\\RiverFlowsInYou.mid')


# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for message in track:
#         print(message)
#         if hasattr(message, 'key'):
#             print(message.key)

# reading the midi file

def get_notes():
    """ Get all the notes and chords from the midi files in the ./midi_songs directory """
    notes = []

    for file in glob.glob("midi/RondoAllaTurca.mid"):
        midi = converter.parse(file)
        print(midi.isStream)
        
        print("Parsing %s" % file)

        notes_to_parse = None

        try: # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse() 
        except: # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        

        for element in notes_to_parse:
            
            if isinstance(element, note.Note):                
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                # print(element, '.'.join(str(n) for n in element.normalOrder))
                notes.append('.'.join(str(n) for n in element.normalOrder))

    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)

    return notes

def prepare_sequences(notes, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    sequence_length = 100

    # get all pitch names
    pitchnames = sorted(set(item for item in notes))

     # create a dictionary to map pitches to integers
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

    network_input = []
    network_output = []

    # create input sequences and the corresponding outputs
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    network_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
    # normalize input
    network_input = network_input / float(n_vocab)

    network_output = np_utils.to_categorical(network_output)

    return (network_input, network_output)


notes = get_notes()
# print(notes, len(notes))

# pygame.mixer.music.load(r'midi\NuvoleBianche.mid')
# pygame.mixer.music.play()

# while pygame.mixer.music.get_busy():
#     pygame.time.wait(1000)





