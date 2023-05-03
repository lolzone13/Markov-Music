import mido
from music21 import converter, instrument, note, chord, stream, midi
from mido import MidiFile
import numpy
import glob
import pickle
import numpy as np
import matplotlib.pyplot as plt
import string
import pygame




def encode_vector_to_state(v):
  state = ""
  cnt = 1
  n = v.size
  for i in range(1,n):
    if v[i] == v[i-1]:
      cnt +=1
    else:
      state += str(v[i-1]) + 'x' + str(cnt) + '-'
      cnt = 1
  
  state += str(v[-1]) + 'x' + str(cnt)
  return state
  


def decode_state_to_vector(state):
  v = []
  uniq = state.split('-')
  for el in uniq:
    num, cnt = el.split('x')
    v += [int(num)]*int(cnt)
  return np.array(v)

# print(decode_state_to_vector('0x2-1x4-4x1-5x1-0x5-45x1-0x4'))

def random_walk2D(transition_prob, initial_states = [0,1], WALK_LENGTH = 100000):
    walk = [initial_states[0], initial_states[1]]
    for i in range(WALK_LENGTH):
       
        prev_state = initial_states[0]
        curr_state = initial_states[1]
        next_state = np.random.choice(np.arange(num_states), p=transition_prob[prev_state][curr_state])
        walk.append(next_state)
        initial_states[0] = curr_state
        initial_states[1] = next_state
        # print("Next State:",next_state)
    return np.array(walk)


class MIDI:
    def __init__(self):
        pass

    def msg2dict(self, msg):
        result = dict()
        if 'note_on' in msg:
            on_ = True
        elif 'note_off' in msg:
            on_ = False
        else:
            on_ = None
        result['time'] = int(msg[msg.rfind('time'):].split(' ')[0].split('=')[1].translate(
            str.maketrans({a: None for a in string.punctuation})))

        if on_ is not None:
            for k in ['note', 'velocity']:
                result[k] = int(msg[msg.rfind(k):].split(' ')[0].split('=')[1].translate(
                    str.maketrans({a: None for a in string.punctuation})))
        return [result, on_]

    def switch_note(self, last_state, note, velocity, on_=True):
        # piano has 88 notes, corresponding to note id 21 to 108, any note out of this range will be ignored
        result = [0] * 88 if last_state is None else last_state.copy()
        if 21 <= note <= 108:
            result[note-21] = velocity if on_ else 0
        return result

    def get_new_state(self, new_msg, last_state):
        new_msg, on_ = self.msg2dict(str(new_msg))
        new_state = self.switch_note(last_state, note=new_msg['note'], velocity=new_msg['velocity'], on_=on_) if on_ is not None else last_state
        return [new_state, new_msg['time']]

    def track2seq(self, track):
        # piano has 88 notes, corresponding to note id 21 to 108, any note out of the id range will be ignored
        result = []
        last_state, last_time = self.get_new_state(str(track[0]), [0]*88)
        for i in range(1, len(track)):
            new_state, new_time = self.get_new_state(track[i], last_state)
            if new_time > 0:
                result += [last_state]*new_time
            last_state, last_time = new_state, new_time
        return result

    def mid2arry(self, mid, min_msg_pct=0.1):
        tracks_len = [len(tr) for tr in mid.tracks]
        min_n_msg = max(tracks_len) * min_msg_pct
        # convert each track to nested list
        all_arys = []
        for i in range(len(mid.tracks)):
            if len(mid.tracks[i]) > min_n_msg:
                ary_i = self.track2seq(mid.tracks[i])
                all_arys.append(ary_i)
        # make all nested list the same length
        max_len = max([len(ary) for ary in all_arys])
        for i in range(len(all_arys)):
            if len(all_arys[i]) < max_len:
                all_arys[i] += [[0] * 88] * (max_len - len(all_arys[i]))
        all_arys = np.array(all_arys)
        all_arys = all_arys.max(axis=0)
        # trim: remove consecutive 0s in the beginning and at the end
        sums = all_arys.sum(axis=1)
        ends = np.where(sums > 0)[0]
        return all_arys[min(ends): max(ends)]

    def arry2mid(self, ary, tempo=500000):
        # get the difference
        new_ary = np.concatenate([np.array([[0] * 88]), np.array(ary)], axis=0)
        changes = new_ary[1:] - new_ary[:-1]
        # create a midi file with an empty track
        mid_new = mido.MidiFile()
        track = mido.MidiTrack()
        mid_new.tracks.append(track)
        track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
        # add difference in the empty track
        last_time = 0
        for ch in changes:
            if set(ch) == {0}:  # no change
                last_time += 1
            else:
                on_notes = np.where(ch > 0)[0]
                on_notes_vol = ch[on_notes]
                off_notes = np.where(ch < 0)[0]
                first_ = True
                for n, v in zip(on_notes, on_notes_vol):
                    new_time = last_time if first_ else 0
                    track.append(mido.Message('note_on', note=n + 21, velocity=v, time=new_time))
                    first_ = False
                for n in off_notes:
                    new_time = last_time if first_ else 0
                    track.append(mido.Message('note_off', note=n + 21, velocity=0, time=new_time))
                    first_ = False
                last_time = 0
        return mid_new
    def get_midi_array(self, folder_path):

        midi_files = glob.glob(folder_path + '\\*.mid')

        midi_array = np.empty((0,88))
        for mi in midi_files:
            mid = mido.MidiFile(mi, clip=True)
            midi_arr = np.array( self.mid2arry(mid))
            midi_array = np.concatenate((midi_array, midi_arr), axis=0)

        return midi_array

Parser = MIDI()
mid = mido.MidiFile('midi\\NuvoleBianche.mid', clip=True)
midi_array = Parser.mid2arry(mid)




# midi_array = Parser.get_midi_array('midi\\kaggle\\mozart')
uniq_midi_rows = np.unique(midi_array, axis=0)
num_states = uniq_midi_rows.shape[0]
states = [encode_vector_to_state(uniq_midi_rows[i]) for i in range(num_states)]


state_to_index = {states[i]: i for i in range(len(states))}


transition_prob = np.zeros((num_states, num_states, num_states))
for i in range(1,midi_array.shape[0]-1):

    prev_st = encode_vector_to_state(midi_array[i-1])
    curr_st = encode_vector_to_state(midi_array[i])
    next_st = encode_vector_to_state(midi_array[i+1])

    # print(prev_st, curr_st, next_st)
    transition_prob[state_to_index[prev_st], state_to_index[curr_st], state_to_index[next_st]] += 1





start_state = [state_to_index[encode_vector_to_state(midi_array[0])], state_to_index[encode_vector_to_state(midi_array[1])]]

epsilon = 1e-12
for i in range(num_states):
  for j in range(num_states):
    sum = np.sum(transition_prob[i][j])
    transition_prob[i][j] = transition_prob[i][j]/(sum + epsilon)
    err = 1 - np.sum(transition_prob[i][j])
    transition_prob[i,j,0] += err
    
generated_midi_seq_idx = random_walk2D(transition_prob, start_state)

print("generated sequence:", generated_midi_seq_idx)
generated_midi_array = np.zeros((generated_midi_seq_idx.size, 88))
i = 0
for idx in generated_midi_seq_idx:
  state = states[idx]
  vector = decode_state_to_vector(state).reshape(1,-1)
  generated_midi_array[i] = vector
  i += 1

generated_midi_array = generated_midi_array.astype('int')


mid_new = Parser.arry2mid(generated_midi_array, 500000)
mid_new.save('midi_test_2d.mid')


print("\n\nPLAYING MUSIC! \n\n")
pygame.init()
pygame.mixer.music.load(r'midi_test_2d.mid')
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)


