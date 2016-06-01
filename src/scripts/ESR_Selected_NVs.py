import numpy as np
from PySide.QtCore import Signal, QThread
from matplotlib import patches

from src.core import Script, Parameter
from src.instruments.NIDAQ import DAQ
from src.plotting.plots_2d import plot_fluorescence
from src.scripts import StanfordResearch_ESR, Correlate_Images, AutoFocus, FindMaxCounts


class ESR_Selected_NVs(Script, QThread):
    updateProgress = Signal(int)

    _DEFAULT_SETTINGS = Parameter([
        Parameter('nv_coor_path', 'Z:/Lab/Cantilever/Measurements/__test_data_for_coding/', str, 'path for NV coordinates'),
        Parameter('nv_coor_tag', 'dummy_tag', str, 'tag for NV coordinates'),
        Parameter('image_path', 'Z:/Lab/Cantilever/Measurements/__test_data_for_coding/', str, 'path for data'),
        Parameter('image_tag', 'some_name', str, 'some_name'),
        Parameter('path', 'Z:/Lab/Cantilever/Measurements/', str, 'path for data'),
        Parameter('tag', 'dummy_tag', str, 'tag for data'),
        Parameter('save', True, bool, 'save data on/off'),
        Parameter('num_between_correlate', -1, int, 'Number of ESRs between correlations, -1 to deactivate correlation'),
        Parameter('num_between_autofocus', -1, int, 'Number of ESRs between autofocuses, -1 to deactivate autofocus'),
        Parameter('autofocus_size', .1, float, 'Side length of autofocusing square in Volts')
    ])

    _INSTRUMENTS = {'daq':  DAQ}
    _SCRIPTS = {'StanfordResearch_ESR': StanfordResearch_ESR, 'Correlate_Images': Correlate_Images, 'AF': AutoFocus, 'Find_Max': FindMaxCounts}

    #updateProgress = Signal(int)

    #This is the signal that will be emitted during the processing.
    #By including int as an argument, it lets the signal know to expect
    #an integer argument when emitting.

    def __init__(self, instruments = None, scripts = None, name = None, settings = None, log_function = None, data_path = None):
        """
        Example of a script that emits a QT signal for the gui
        Args:
            name (optional): name of script, if empty same as class name
            settings (optional): settings for this script, if empty same as default settings
        """
        self._abort = False

        Script.__init__(self, name, settings = settings, instruments = instruments, scripts = scripts, log_function= log_function, data_path = data_path)

        QThread.__init__(self)

        self._plot_type = 'two'

        self.index = 0

        self.progress = 0

        self.scripts['AF'].updateProgress.connect(self._receive_signal)
        self.scripts['AF'].log_function = self.log_function
        self.scripts['Correlate_Images'].updateProgress.connect(self._receive_signal)
        self.scripts['Correlate_Images'].log_function = self.log_function
        self.scripts['Find_Max'].updateProgress.connect(self._receive_signal)
        self.scripts['Find_Max'].log_function = self.log_function
        self.scripts['StanfordResearch_ESR'].updateProgress.connect(self._receive_signal)
        self.scripts['StanfordResearch_ESR'].log_function = self.log_function

        self.image_data = None
        self.nv_locs = None

    def _receive_signal(self, progress_sub_script):
        # calculate progress of this script based on progress in subscript

        if self.current_stage == 'ESR':
            self.progress = int((float(self.index)/self.num_esrs)*100 + float(progress_sub_script)/self.num_esrs)
        self.updateProgress.emit(self.progress)

    def _function(self):
        """
        This is the actual function that will be executed. It uses only information that is provided in the settings property
        will be overwritten in the __init__
        """
        self._abort = False
        self.current_stage = None

        self.af_index = 1
        self.corr_index = 1

        self.load_coors_and_image()

        esr_settings = self.scripts['StanfordResearch_ESR'].settings
        esr_instruments = self.scripts['StanfordResearch_ESR'].instruments

        while True:
            self.data = {'image_data': self.image_data, 'nv_coors': self.nv_locs, 'ESR_freqs': [], 'ESR_data': np.zeros((len(self.nv_locs), esr_settings['freq_points']))}

            for index, pt in enumerate(self.nv_locs):
                if not self._abort:
                    self.plot_pt = pt
                    if (not self.settings['num_between_autofocus'] == -1) and (self.af_index == self.settings['num_between_autofocus']):
                        self.current_stage = 'Autofocus'
                        self.log('Autofocusing on point ' + str(index + 1) + ' of ' + str(len(self.nv_locs)))
                        daq_pt = np.transpose(np.column_stack((pt[0], pt[1])))
                        daq_pt = (np.repeat(daq_pt, 2, axis=1))

                        x_min = pt[0] - self.settings['autofocus_size']/2
                        x_max = pt[0] + self.settings['autofocus_size']/2
                        y_min = pt[1] - self.settings['autofocus_size']/2
                        y_max = pt[1] + self.settings['autofocus_size']/2
                        self.scripts['AF'].scripts['take_image'].settings['point_a'].update({'x': x_min, 'y': y_min})
                        self.scripts['AF'].scripts['take_image'].settings['point_b'].update({'x': x_max, 'y': y_max})

                        if self._abort:
                            break

                        self.scripts['AF'].run()
                        self.scripts['AF'].wait()

                        self.instruments['daq']['instance'].AO_init(["ao0", "ao1"], daq_pt)
                        self.instruments['daq']['instance'].AO_run()
                        self.instruments['daq']['instance'].AO_waitToFinish()
                        self.instruments['daq']['instance'].AO_stop()
                        self.updateProgress.emit(self.progress)

                        self.af_index = 0
                    if (not self.settings['num_between_correlate'] == -1) and (self.corr_index == self.settings['num_between_correlate']):
                        self.current_stage = 'Correlate'
                        self.log('Correlating for point ' + str(index + 1) + ' of ' + str(len(self.nv_locs)))
                        self.scripts['Correlate_Images'].settings['new_image_center'] = pt
                        if self._abort:
                            break
                        self.scripts['Correlate_Images'].run()
                        self.scripts['Correlate_Images'].wait()
                        self.updateProgress.emit(self.progress)
                        pt = self.scripts['Correlate_Images'].shift_coordinates(pt)
                        self.scripts['Correlate_Images'].settings['reset'] = False

                    self.current_stage = 'Find_Max'
                    self.log('Finding center of point ' + str(index + 1) + ' of ' + str(len(self.nv_locs)))
                    self.scripts['Find_Max'].settings['initial_point'].update({'x': pt[0], 'y': pt[1]})
                    if self._abort:
                        break
                    self.scripts['Find_Max'].run()
                    self.scripts['Find_Max'].wait()
                    self.updateProgress.emit(self.progress)

                    self.current_stage = 'ESR'
                    self.cur_pt = self.scripts['Find_Max'].data['maximum_points']
                    self.index = index
                    # self.cur_pt = pt
                    self.log('Taking ESR of point ' + str(index + 1) + ' of ' + str(len(self.nv_locs)))
                    #set laser to new point
                    daq_pt = np.transpose(np.column_stack((pt[0], pt[1])))
                    daq_pt = (np.repeat(daq_pt, 2, axis=1))
                    self.instruments['daq']['instance'].AO_init(["ao0","ao1"], daq_pt)
                    self.instruments['daq']['instance'].AO_run()
                    self.instruments['daq']['instance'].AO_waitToFinish()
                    self.instruments['daq']['instance'].AO_stop()

                    #run the ESR
                    # self.scripts['StanfordResearch_ESR']['instance'].tag = self.scripts['StanfordResearch_ESR']['instance'].tag + '_NV_no_' + index
                    if self._abort:
                        break
                    self.scripts['StanfordResearch_ESR'].run()
                    self.scripts['StanfordResearch_ESR'].wait() #wait for previous ESR thread to complete
                    self.updateProgress.emit(self.progress)

                    self.data['ESR_freqs'] = self.scripts['StanfordResearch_ESR'].data[-1]['frequency']
                    self.data['ESR_data'][index] = self.scripts['StanfordResearch_ESR'].data[-1]['data']

                    #can't call run twice on the same object, so start a new, identical ESR script for the next run
                    #update: probably not supported, but doesn't seem to have any ill effects
                    # self.scripts['StanfordResearch_ESR'] = StanfordResearch_ESR(esr_instruments, settings = esr_settings)
                    # self.scripts['StanfordResearch_ESR'].updateProgress.connect(self._receive_signal)

                    self.af_index += 1

            self.updateProgress.emit(100)
            if self.settings['save']:
                self.save_b26()
                self.save_data()

    def stop(self):
        self._abort = True
        self.scripts['AF'].stop()
        self.scripts['Correlate_Images'].stop()
        self.scripts['Find_Max'].stop()
        self.scripts['StanfordResearch_ESR'].stop()

    def plot(self, axes_Image, axes_ESR):
        if self.image_data is None or self.nv_locs is None:
            self.load_coors_and_image()
            print(self.nv_locs)
        image = self.image_data
        extend = [self.x_min, self.x_max, self.y_max, self.y_min]
        plot_fluorescence(image, extend, axes_Image)

        if self.isRunning():
            patch = patches.Circle((self.plot_pt[0], self.plot_pt[1]), .0005, fc='b', alpha=.75)
            axes_Image.add_patch(patch)
        else:
            for pt in self.nv_locs:
                patch = patches.Circle((pt[0], pt[1]), .0005, fc='b')
                axes_Image.add_patch(patch)

        if self.current_stage == 'Autofocus':
            self.scripts['AF'].plot(axes_Image, axes_ESR)
        elif self.current_stage == 'Correlate':
            self.scripts['Correlate_Images'].plot(axes_Image, axes_ESR)
        elif self.current_stage == 'Find_Max':
            self.scripts['Find_Max'].plot(axes_ESR)
        elif self.current_stage == 'ESR':
            self.scripts['StanfordResearch_ESR'].plot(axes_ESR)

    def load_coors_and_image(self):
        self.image_data = Script.load_data(self.settings['image_path'], data_name_in='image_data')
        bounds = Script.load_data(self.settings['image_path'], data_name_in='bounds')
        self.x_min = bounds[0][0]
        self.x_max = bounds[1][0]
        self.y_min = bounds[2][0]
        self.y_max = bounds[3][0]

        print('settings', self.settings)
        self.nv_locs = Script.load_data(self.settings['nv_coor_path'], data_name_in='nv_locations')
        self.num_esrs = len(self.nv_locs)


if __name__ == '__main__':
    from src.core import Instrument

    script, failed, instruments = Script.load_and_append(script_dict={'ESR_Selected_NVs':'ESR_Selected_NVs'})

    print(script)
    print(failed)
    print(instruments)