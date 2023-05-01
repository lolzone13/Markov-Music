
import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
import scipy
import time


class AudioStream(object):
    def __init__(self):
        
        # stream constants
        self.CHUNK = 1024*2
        self.pause = False
        self.CHANNELS = 2
        

        self.RATE, self.data = scipy.io.wavfile.read('MoonlightSonata.wav')

        lim = (len(self.data) // self.CHUNK) * self.CHUNK
        self.data = self.data[0:lim, 0]
        # self.play_music()
        self.init_plots()

        self.start_plot()


    def play_music(self):
        playsound('MoonlightSonata.mp3', False)
        print("Playing Music")

    def init_plots(self):
        plt.style.use('dark_background')
        CB91_Blue = '#2CBDFE'
        CB91_Green = '#47DBCD'
        CB91_Pink = '#F3A0F2'
        CB91_Purple = '#9D2EC5'
        CB91_Violet = '#661D98'
        CB91_Amber = '#F5B14C'
        color_list = [ CB91_Violet,CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
                    CB91_Purple]
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

        x = np.arange(0, self.CHUNK, 1)
        xf = np.arange(0,self.CHUNK, 1)
        # create matplotlib figure and axes
        self.fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)

        # create a line object with random data
        self.line, = ax1.plot(x, np.random.rand(self.CHUNK), 'm-', lw=2)

        # create semilogx line for spectrum
        self.line_fft, = ax2.semilogx(xf, np.random.rand(self.CHUNK), 'c-', lw=2)

        # format waveform axes
        ax1.set_title('AUDIO WAVEFORM')
        ax1.set_xlabel('samples')
        ax1.set_ylabel('volume')
        ax1.set_ylim(-500, 500)
        ax1.set_xlim(0, self.CHUNK)
      

        # format spectrum axes
        ax2.set_ylim(0, 1.5)
        ax2.set_xlim(1, self.CHUNK)

        # show axes
        thismanager = plt.get_current_fig_manager()
        thismanager.window.setGeometry(5, 120, 1910, 1070)
        plt.show(block=False)

    def start_plot(self):

        print('plotting')
        frame_count = 0
        start_time = time.time()
        chunks = np.split(self.data, len(self.data) / self.CHUNK)
        for chunk in chunks:
            data = chunk
           
            self.line.set_ydata(data)

            # compute FFT and update line
            yf = scipy.fft.fft(data)

            self.line_fft.set_ydata(np.absolute(yf) / 75000) 

            # update figure canvas
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            frame_count += 1

        else:
            self.fr = frame_count / (time.time() - start_time)
            print('average frame rate = {:.0f} FPS'.format(self.fr))
            self.exit_app()

    def exit_app(self):
        print('stream closed')
        plt.close('all')

    def onClick(self, event):
        self.pause = True


if __name__ == '__main__':
    AudioStream()