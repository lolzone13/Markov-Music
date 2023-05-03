
import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
import scipy
import time



class MusicVisualizer(object):
    def __init__(self):
        
        
        self.pause = False
        self.CHANNELS = 2
        
        self.RATE, self.data = scipy.io.wavfile.read('MoonlightSonata.wav')
        self.duration = len(self.data) / self.RATE

        self.CHUNK = int(len(self.data) // (13 * self.duration))
      
        lim = (len(self.data) // self.CHUNK) * self.CHUNK
   
        self.data = self.data[0:lim, 0]

        self.st = time.time()
        
        self.init_plots()
        
        self.start_plot()


    def play_music(self):
        playsound('MoonlightSonata.wav', False)
        print("Playing Music")

    def init_plots(self):

        # Add Plot styles
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


        self.fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        self.line, = ax1.plot(x, np.random.rand(self.CHUNK), 'm-', lw=2)
        self.line_fft, = ax2.semilogx(xf, np.random.rand(self.CHUNK), 'c-', lw=2)

        ax1.set_title('AUDIO WAVEFORM')
        ax1.set_xlabel('samples')
        ax1.set_ylabel('volume')
        ax1.set_ylim(-1000, 1000)
        ax1.set_xlim(0, self.CHUNK)
      
        ax2.set_ylim(0, 1.5)
        ax2.set_xlim(1, self.CHUNK)

        thismanager = plt.get_current_fig_manager()
        thismanager.window.setGeometry(5, 120, 1910, 1070)
        plt.show(block=False)

    def start_plot(self):

        print('plotting')
        frame_count = 0
        start_time = time.time()
        chunks = np.split(self.data, len(self.data) / self.CHUNK)
        self.play_music()
        for chunk in chunks:
            temp_start = time.time()
            data = chunk
           
            self.line.set_ydata(data)

            yf = scipy.fft.fft(data)


            yf_amp = np.absolute(yf) / 50000

            self.line_fft.set_ydata(yf_amp) 

            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            frame_count += 1

            self.fr = frame_count / (time.time() - start_time)


            current_fps = 1 / (time.time() - temp_start) 
            print("Current FPS: {}".format(current_fps))

        else:
            self.fr = frame_count / (time.time() - start_time)
            print('average frame rate = {:.0f} FPS'.format(self.fr))
            self.exit_app()

    def exit_app(self):
        print("End time: ", time.time() - self.st)
        print('stream closed')
        plt.close('all')

    def onClick(self, event):
        self.pause = True


if __name__ == '__main__':
    MusicVisualizer()