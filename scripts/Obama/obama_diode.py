#===============================================================================
# EXTRACTION SCRIPT obama_diode.py
#===============================================================================
'''
eqtime: 8
'''

def main():
    info('Obama unknown laser analysis')
    gosub('obama:PrepareForDiodeAnalysis')
 
    gosub('obama:IsolateDiodeColdfinger')
    
    '''
    keep pumping bone while cold finger isolated
    '''
    
    open(description='Bone to Turbo')
  
    set_motor('beam',beam_diameter)   

    if analysis_type=='blank':
        info('Blank Analyis. No laser heating')

        '''
        sleep cumulative time to account for blank
        during a multiple position analysis
        '''
        numPositions=len(position)

        sleep(duration*numPositions)
    else:
        info('Diodelaser enabled. Heating sample.')


        '''
        this is the most generic way to move and fire the laser
        position is always a list even if only one hole is specified
        '''
        enable()
        for pi in position:
            ''' 
            position the laser at pi, pi can be an holenumber or (x,y)
            '''
            move_to_position(pi)
            do_extraction()
            if disable_between_positions:
                extract(0)
        info('Diode laser disabled.')
        disable()
      
    gosub('obama:EquilibrateThenIsolateDiodeColdfinger')    
    
    sleep(cleanup)


def do_extraction():
    
    if ramp_rate>0:
        '''
        style 1.
        '''
        #               begin_interval(duration)
        #               info('ramping to {} at {} {}/s'.format(extract_value, ramp_rate, extract_units)
        #               ramp(setpoint=extract_value, rate=ramp_rate)
        #               complete_interval()
        '''
        style 2.
        '''
        elapsed=ramp(setpoint=extract_value, rate=ramp_rate)
        pelapsed=execute_pattern(pattern)
        sleep(min(0, duration-elapsed-pelapsed))

    else:
        begin_interval(duration)
        
        info('set extract to {} ({})'.format(extract_value, extract_units))
        extract()
        sleep(2)

        if pattern:
            info('executing pattern {}'.format(pattern))
            execute_pattern(pattern)

        complete_interval()


#===============================================================================
# POST EQUILIBRATION SCRIPT obama_pump_extraction_line.py
#===============================================================================
def main():
    info('Pump after analysis')
    gosub('obama:PumpBone')
    if get_resource_value(name='ObamaMiniboneFlag'):
        gosub('obama:PumpMinibone')
#===============================================================================
# POST MEASUREMENT SCRIPT obama_pump_ms.py
#===============================================================================
def main():
	info('Pumping spectrometer')
	open(name='V')
	