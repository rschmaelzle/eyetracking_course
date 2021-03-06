from exptools.core.session import EyelinkSession
from trial import PRTrial
from psychopy import visual, clock
import numpy as np
import os
import exptools
import json
import glob
from stimulus import VonMisesDotStim


class PRSession(EyelinkSession):

    def __init__(self, *args, **kwargs):

        super(PRSession, self).__init__(*args, **kwargs)

        config_file = os.path.join(os.path.abspath(os.getcwd()), 'default_settings.json')

        with open(config_file) as config_file:
            config = json.load(config_file)

        self.config = config
        self.create_trials()
        self.setup_stimuli()

        self.stopped = False


    def create_trials(self):
        """creates trials by creating a restricted random walk through the display from trial to trial"""

        self.trial_parameters = [{'fixation_duration': 0, #1 + np.random.exponential(1.5),
                                  'random_dots1_duration' : 1 + np.random.exponential(1.5),
                                  'coherent_dots_duration': 1 + np.random.exponential(1.5),
                                  'random_dots2_duration': 1 + np.random.exponential(1.5),
                                  'direction':np.random.choice([0, 180], 1)
                                  } for i in xrange(self.config['nTrials'])]
        self.trial_parameters[0]['fixation_duration'] = 30

    def setup_stimuli(self):
        size_fixation_pix = self.deg2pix(self.config['size_fixation_deg'])
        size_dotfield_pix = self.deg2pix(self.config['diameter_dotcloud_deg'])
        size_dot_pix = self.deg2pix(self.config['size_dot_deg'])
        speed_dot_pix = self.deg2pix(self.config['speed_dot_deg'])

        self.fixation = visual.GratingStim(self.screen,
                                           tex='sin',
                                           mask='circle',
                                           size=size_fixation_pix,
                                           texRes=512,
                                           color='white',
                                           sf=0)

        self.dots = VonMisesDotStim(self.screen, 
                                    kappa=1,
                                    fieldSize=size_dotfield_pix,
                                    fieldShape='circle',
                                    speed=speed_dot_pix,
                                    dotSize=size_dot_pix,
                                    nDots=self.config['nDots'], 
                                    noiseDots=self.config['noiseDots'],
                                    signalDots='direction',
                                    dotLife=self.config['dotLife'],
                                    coherence=0.0)

        this_instruction_string = """What direction do the dots start to move in?\nPress 'f' for left and 'j' for right. \nPress either key to start."""
        self.instruction = visual.TextStim(self.screen, 
            text = this_instruction_string, 
            font = 'Helvetica Neue',
            pos = (0, 0),
            italic = True, 
            height = 20, 
            alignHoriz = 'center',
            color=(1,0,0))
        self.instruction.setSize((1200,50))

    def run(self):
        """run the session"""
        # cycle through trials


        for trial_id, parameters in enumerate(self.trial_parameters):

            trial = PRTrial(ti=trial_id,
                           config=self.config,
                           screen=self.screen,
                           session=self,
                           parameters=parameters,
                           tracker=self.tracker)
            trial.run()

            if self.stopped == True:
                break

        self.close()
