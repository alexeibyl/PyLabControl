# B26 Lab Code
# Last Update: 2/3/15

# External connections: default channels are input 1, output 1, auxillary 0

# import libraries
import time
import re
import zhinst.utils as utils
import matplotlib.pyplot as plt
import numpy

# This class initializes an input, output, and auxillary channel on the ZIHF2, and currently has functionality to run
# a sweep, and plot and save the results.
class ZIHF2:
    # initializes values
    # amplitude: output channel amplitude (Vpk)
    # offset: auxillary channel output (V), only functions as offset if aux0 connected to inChannel add port
    # ACCoupling: turns ac coupling on (1) or off (0), default off
    # inChannel: specifies input channel number, default channel 1 as listed on device (value 0)
    # outChannel: specifies output channel number, default channel 1 as listed on device (value 0)
    # auxChannel: specifies auxillary channel to use, default channel 1 as listed on device (value 0)
    # add: turns add mode on output channel on (1) or off (0), default 1
    # range: sets output range (V), default 10
    def __init__(self, amplitude, offset, ACCoupling = 0, inChannel = 0, outChannel = 0, auxChannel = 0, add = 1, range = 10):
        # find and connect to device
        self.daq = utils.autoConnect(8005,1)
        self.device = utils.autoDetect(self.daq)
        self.options = self.daq.getByte('/%s/features/options' % self.device)
         #channel settings
        self.in_c = inChannel
        self.out_c = outChannel
        self.demod_c = 0
        self.demod_rate = 10e3
        self.osc_c = 0
        if (not re.match('MF', self.options)):
            self.out_mixer_c = 6
        else:
            self.out_mixer_c = 0
        self.plotting = 0

        # Configure the settings relevant to this experiment
        self.exp_setting = [
            ['/%s/sigins/%d/imp50'          % (self.device, self.in_c), 1],
            ['/%s/sigins/%d/ac'             % (self.device, self.in_c), ACCoupling],
            ['/%s/sigins/%d/range'          % (self.device, self.in_c), 2*amplitude],
            ['/%s/demods/%d/order'          % (self.device, self.demod_c), 4],
            ['/%s/demods/%d/rate'           % (self.device, self.demod_c), self.demod_rate],
            ['/%s/demods/%d/harmonic'       % (self.device, self.demod_c), 1],
            ['/%s/demods/%d/phaseshift'     % (self.device, self.demod_c), 0],
            ['/%s/sigouts/%d/on'            % (self.device, self.out_c), 1],
            ['/%s/sigouts/%d/range'         % (self.device, self.out_c), 10],
            ['/%s/sigouts/%d/enables/%d'    % (self.device, self.out_c, self.out_mixer_c), 1],
            ['/%s/sigouts/%d/amplitudes/%d' % (self.device, self.out_c, self.out_mixer_c), float(amplitude)/range],
            ['/%s/AUXOUTS/%d/OFFSET'% (self.device, auxChannel), offset]]

        self.exp_setting.append(['/%s/demods/%d/oscselect' % (self.device, self.demod_c), self.osc_c])
        self.exp_setting.append(['/%s/demods/%d/adcselect' % (self.device, self.demod_c), self.in_c])
        self.exp_setting.append(['/%s/sigins/%d/diff' % (self.device, self.in_c), 0])
        self.exp_setting.append(['/%s/sigouts/%d/add' % (self.device, self.out_c), add])
        self.daq.set(self.exp_setting)

    # performs a frequency sweep and stores result in self.samples
    # freqStart: initial frequency for sweep (Hz)
    # freqEnd: ending frequency for sweep (Hz)
    # sampleNum: number of samples in sweep range
    # samplesPerPt: number of samples to take at each frequency point
    # xScale: choose linear (0) or logarithmic (1) frequency scale, default linear
    # direction: choose sequential (0), binary (1), or bidirectional (2) scan modes, default sequential
    # loopcount: number of times to repeat sweep, default 1
    def sweep(self, freqStart, freqEnd, sampleNum, samplesPerPt, xScale = 0, direction = 0, loopcount = 1, timeout=10000):
        sweeper = self.daq.sweep(timeout)
        sweeper.set('sweep/device', self.device)
        sweeper.set('sweep/start', freqStart)
        sweeper.set('sweep/stop', freqEnd)
        sweeper.set('sweep/samplecount', sampleNum)
        sweeper.set('sweep/gridnode', 'oscs/%d/freq' % self.osc_c)
        #0 = linear, 1 = logarithmic
        sweeper.set('sweep/xmapping', xScale)
        #automatic bandwidth control
        sweeper.set('sweep/bandwidthcontrol', 2)
        #0 = sequential, 1 = binary (non-sequential, each point once), 2 = bidirecctional (forward then reverse)
        sweeper.set('sweep/scan', direction)
        sweeper.set('sweep/loopcount', loopcount)
        #always use samples per point, so set time to 0
        sweeper.set('sweep/averaging/tc', 0)
        #number of samples to average over
        sweeper.set('sweep/averaging/sample', samplesPerPt)

        #specify nodes to recorder data from
        path = '/%s/demods/%d/sample' % (self.device, self.demod_c)
        sweeper.subscribe(path)
        sweeper.execute()

        start = time.time()
        timeout = 60  # [s]
        print "Will perform %d sweeps...." % loopcount
        while not sweeper.finished():
            time.sleep(.2)
            progress = sweeper.progress()
            print "Individual sweep %.2f%% complete.   \r" % (100*progress),
            #read and plot data as it is collected
            data = sweeper.read(True)
            self.samples = data[path]
            self.plot()
            if (time.time() - start) > timeout:
                # If for some reason the sweep is blocking, force the end of the
                # measurement
                print "\nSweep still not finished, forcing finish..."
                sweeper.finish()
        print ""

        # Read the sweep data. This command can also be executed whilst sweeping
        # (before finished() is True), in this case sweep data up to that time point
        # is returned. It's still necessary still need to issue read() at the end to
        # fetch the rest.
        return_flat_dict = True
        data = sweeper.read(return_flat_dict)
        sweeper.unsubscribe(path)

        # Stop the sweeper thread and clear the memory
        sweeper.clear()

        # weird bug in code from sample that causes empty data dict when real time reading is implemented, code
        # disabled and this code reads any final samples if data is not empty

        # Check the dictionary returned is non-empty
        #assert data, "read() returned an empty data dictionary, did you subscribe to any paths?"
        # note: data could be empty if no data arrived, e.g., if the demods were
        # disabled or had rate 0
        if(data):
        #assert path in data, "no sweep data in data dictionary: it has no key '%s'" % path
            self.samples = data[path]
        print "sample contains %d sweeps" % len(self.samples)

    # plots data contained in self.samples
    def plot(self):
        if(self.plotting == 0):
            plt.ion()
            for i in range(0, len(self.samples)):
                # please note: the "[i][0]" indexing is known issue to be fixed in
                # an upcoming release (there shouldn't be an additional [0])
                frequency = self.samples[i][0]['frequency']
                frequency = frequency[~numpy.isnan(frequency)]
                R = numpy.sqrt(self.samples[i][0]['x']**2 + self.samples[i][0]['y']**2)
                R = R[~numpy.isnan(R)]
                plt.loglog(frequency, R)
            plt.grid(True)
            plt.title('Results of %d sweeps' % len(self.samples))
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude (V_RMS)')
            plt.autoscale()
            plt.show(block = False)
            self.plotting = 1
        else:
            for i in range(0, len(self.samples)):
                # please note: the "[i][0]" indexing is known issue to be fixed in
                # an upcoming release (there shouldn't be an additional [0])
                frequency = self.samples[i][0]['frequency']
                frequency = frequency[~numpy.isnan(frequency)]
                R = numpy.sqrt(self.samples[i][0]['x']**2 + self.samples[i][0]['y']**2)
                R = R[~numpy.isnan(R)]
                plt.loglog(frequency, R)
                plt.draw()

# test code
#if __name__ == '__main__':
#    zi = ZIHF2(1, .5)
#    zi.sweep(1e6, 50e6, 100, 10, xScale = 0)
#    zi.plot()