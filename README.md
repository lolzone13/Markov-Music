
# Markov Music

This is a project to compare multiple different music generation techniques. We use MIDI files to train and generate music.




## Markov Chains

A Markov chain is a mathematical system that experiences transitions from one state to another according to certain probabilistic rules. MIDI sequences are represented as sequences of states, and the model is trained on a song to generate a transition matrix. Using this transition matrix, we perform a random walk to generate a new musical piece.

![Markov Chain](https://github.com/lolzone13/Markov-Music/blob/main/assets/markovChain.png)


## LSTMs

LSTM stands for long short-term memory networks, used in the field of Deep Learning. It is a variety of recurrent neural networks (RNNs) that are capable of learning long-term dependencies, especially in sequence prediction problems. The network is trained on a plethora of classical piano music and then used to predict a new sequence.

![LSTM](https://github.com/lolzone13/Markov-Music/blob/main/assets/lstm.png)
## GANs

GANs are a class of Generative Models, i.e, they create new models that resemble the training data. It is composed of two neural networks - a generator and a discriminator which compete against each other. The generator creates fake samples and the discriminator decides whether these samples are fake or real.

![GAN](https://github.com/lolzone13/Markov-Music/blob/main/assets/GANs.jpg)
## Music Visualization

We use Pygame to visualize the music played. The bars are generated in the frequency domain (using the fourier transform) and the height of the bars are controlled by the amplitude of the music piece. We also have different colors for different frequency ranges - mids, lows and highs.

![Viz](https://github.com/lolzone13/Markov-Music/blob/main/assets/musicviz.gif)
## Tech Stack

The project is written in python and uses the following packages

- Tensorflow
- Numpy
- PyQt5
- Scipy
- Pygame
- Music21
- Matplotlib



## Installation

To install the dependencies, activate your virtual environment and then run 

```bash
  pip install -r requirements.txt
```

## Authors

- [@lolzone13](https://www.github.com/lolzone13)
- [@SanskarKejriwal](https://www.github.com/SanskarKejriwal)
- [@The-DefaultCube](https://www.github.com/The-DefaultCube)

