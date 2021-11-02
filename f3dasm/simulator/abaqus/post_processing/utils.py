'''
Created on 2020-09-17 19:10:47
Last modified on 2020-09-30 11:39:22

@author: L. F. Pereira (lfpereira@fe.up.pt))
'''

# imports

# standard library
import os
import pickle
from collections import OrderedDict

# local library
import f3dasm
from ..utils.file_handling import InfoReport
from ..post_processing import collect_raw_data


# object definition

def get_updated_sims_state(raw_data=None, example_name=None,
                           points=None, sims_dir_name='analyses',):
    '''
    Parameters
    ----------
    raw_data : pd.Series or str or None.
        Data is gatherer according to `raw_data` type. The possibilities are:
            None: simulation folders
            str: raw data file
            pandas.Series: uses itself.
    points : array
        If None, considers all created simulation folders or folders available
        in `raw_data` file. Only applicable if `raw_data` is a path to a file
        or None.
    '''

    # get raw data
    if type(raw_data) is str or raw_data is None:
        raw_data = collect_raw_data(example_name, sims_dir_name=sims_dir_name,
                                    sim_numbers=points, delete=False,
                                    raw_data_filename=raw_data)

    # getting sims state
    error_sims = []
    successful_sims = []
    for point, data_sim in raw_data.iteritems():
        success = data_sim.get('success', None)
        if success:
            successful_sims.append(point)
        elif success is False:
            error_sims.append(point)

    return set(error_sims), set(successful_sims)


def get_sims_info(example_name, data_filename='DoE.pkl',
                  sims_dir_name='analyses', print_info=True, report=''):
    # TODO: move to stats?

    # initialization
    info = InfoReport(sections=['run_info'])
    run_info_sec = info['run_info']

    # access data
    with open(os.path.join(example_name, data_filename), 'rb') as file:
        data = pickle.load(file)

    # running simulations
    running_sims = data['run_info']['running_sims']
    error_sims_, successful_sims_ = get_updated_sims_state(
        example_name=example_name, points=running_sims,
        sims_dir_name=sims_dir_name, raw_data=None,)
    n_running_sims = len(running_sims)
    n_running_sims_miss = len(set(running_sims) - error_sims_ - successful_sims_)

    # other simulations
    n_missing_sims = len(data['run_info']['missing_sims']) + n_running_sims_miss
    n_error_sims = len(data['run_info']['error_sims']) + len(error_sims_)
    n_successful_sims = len(data['run_info']['successful_sims']) + len(successful_sims_)
    n_run = n_error_sims + n_successful_sims
    n_total = n_missing_sims + n_run

    # compute information
    if n_running_sims:
        run_info_sec.add_info(
            'Missing simulations (running): {}/{} ({:.1f}%)'.format(
                n_running_sims_miss, n_running_sims,
                n_running_sims_miss / n_running_sims * 100))
    run_info_sec.add_info('Missing simulations (total): {}/{} ({:.1f}%)'.format(
        n_missing_sims, n_total, n_missing_sims / n_total * 100))
    if n_run:
        run_info_sec.add_info('With errors: {}/{} ({:.1f}%)'.format(
            n_error_sims, n_run, n_error_sims / n_run * 100))
        run_info_sec.add_info('Successful: {}/{} ({:.1f}%)'.format(
            n_successful_sims, n_run, n_successful_sims / n_run * 100))

    # print information
    if print_info:
        info.print_info(print_headers=False)

    # create report
    if report:
        with open(report, 'w') as file:
            info.write_report(file, print_headers=False)

    return info


def update_run_info(example_name, data_filename='DoE.pkl',
                    sims_dir_name='analyses'):
    '''
    Updates information about simulations. Assumes simulations are not being
    ran. It is supposed to correct possible outdated files due to running of
    simulations in different machines.
    '''
    # TODO: review

    # access data
    with open(os.path.join(example_name, data_filename), 'rb') as file:
        data = pickle.load(file)

    # compute information
    points = list(range(len(data['points'])))
    error_sims, successful_sims = get_updated_sims_state(
        example_name, points, sims_dir_name)
    missing_sims = list(set(points) - set(error_sims) - set(successful_sims))

    # dump information
    data['run_info']['missing_sims'] = missing_sims
    data['run_info']['running_sims'] = []
    data['run_info']['error_sims'] = error_sims
    data['run_info']['successful_sims'] = successful_sims
    with open(os.path.join(example_name, data_filename), 'wb') as file:
        pickle.dump(data, file)


def _manipulate_sim_dict(sim_dict):
    name = sim_dict['name']
    del sim_dict['name']

    return name, sim_dict
