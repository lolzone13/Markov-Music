import pygame
from mido import MidiFile
pygame.init()

# get trigrams from midi file

NOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', ' '] # all notes + gap



mid = MidiFile('midi\\RiverFlowsInYou.mid')
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for message in track:
        print(message)

# reading the midi file
pygame.mixer.music.load(r'midi\RiverFlowsInYou.mid')
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)



