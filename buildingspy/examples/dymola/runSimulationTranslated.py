from multiprocessing import Pool, freeze_support
import buildingspy.simulate.Dymola as si


# Function to set common parameters and to run the simulation
def simulateCase(s):
    ''' Set common parameters and run a simulation.

    :param s: A simulator object.

    '''
    s.setStopTime(86400)
    # Kill the process if it does not finish in 1 minute
    s.setTimeOut(60)
    s.showProgressBar(False)
    s.printModelAndTime()
    s.simulate_translated()


def main():
    ''' Main method that configures and runs all simulations
    '''
    # Build list of cases to run
    li = []

    # First model
    model = 'Modelica.Blocks.Examples.PID_Controller'
    s = si.Simulator(model, 'dymola')
    s.setOutputDirectory('case1')
    s.addParameters({'PI.k': 100})
    s.setSolver('dassl')
    s.showGUI(False)
    s.translate()
    li.append(s)

    # Second model
    import copy
    s2 = copy.deepcopy(s)
    s2.setOutputDirectory('case2')
    s2.addParameters({'PI.k': 50})
    li.append(s2)

    # Run all cases in parallel
    with Pool() as pool:
        pool.map(simulateCase, li)
    # clean up
    # s2.deleteTranslateDirectory()


# Main function
if __name__ == '__main__':
    freeze_support()
    main()
