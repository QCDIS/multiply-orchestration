from datetime import datetime, timedelta
from multiply_data_access import DataAccessComponent
from multiply_core.util import AttributeDict
from multiply_prior_engine import PriorEngine
from shapely import geometry, wkt
import yaml

__author__ = "Tonio Fincke (Brockmann Consult GmbH)"


class Orchestrator(object):
    """
    This class serves to depict a basic workflow that might be used during the User Workshop in Frascati.
    """

    @staticmethod
    def orchestrate(dir: str) -> None:
        """
        This function deals with orchestration it does not take any arguments and creates all input and output by
        itself.
        :return:
        """

        roi = 'POLYGON ((48.0 11.3, 48.2 11.3, 48.1 11.1, 48.0 11.0, 48.0 11.3))'
        start_time_as_string = '2017-01-01'
        end_time_as_string = '2017-01-10'

        data_access_component = DataAccessComponent()
        data_access_component.read_data_stores(dir + '/frascati_data_stores.yml')
        # data_access_component.read_data_stores(
        #     'C:/Users/tonio/Projekte/multiply/workshop/frascati-20180205/frascati_data_stores.yml')
        priors_sm_dir = data_access_component.get_data_urls(roi, start_time_as_string, end_time_as_string,
                                                            'SoilMoisture')[0]
        priors_veg_dir = data_access_component.get_data_urls(roi, start_time_as_string, end_time_as_string,
                                                             'Vegetation')[0]

        config = Orchestrator._get_config(priors_sm_dir=priors_sm_dir, priors_veg_dir=priors_veg_dir, roi=roi,
                                          start_time=start_time_as_string, end_time=end_time_as_string)
        config_file_name = dir + '/config.yml'
        yaml.dump(config, open(config_file_name, 'w+'))
        config_as_dict = AttributeDict(**config)

        # mcd43_urls = data_access_component.get_data_urls(roi, start_time_as_string, end_time_as_string, 'MCD43')

        # todo get SAR pre-processed data
        # todo get MODIS data
        # todo get S2 pre-processed data

        # todo get priors
        parameters = config_as_dict['Inference']['parameters']
        start_time = datetime.strptime(config_as_dict['General']['start_time'], "%Y-%m-%d")
        end_time = datetime.strptime(config_as_dict['General']['end_time'], "%Y-%m-%d")
        time_interval = config_as_dict['General']['time_interval']
        time_interval_unit = config_as_dict['General']['time_interval_unit']
        current_time = start_time
        prior_file_dicts = []
        while current_time < end_time:
            time_string = current_time.strftime("%Y-%m-%d")
            prior_engine = PriorEngine(datestr=time_string, variables=parameters, config=(config_file_name))
            prior_file_dicts.append(prior_engine.get_priors())
            current_time = Orchestrator._increase_time_step(current_time, time_interval, time_interval_unit)

        # todo get this from DAC
        # emulator = config['Inference']['emulator']

        # todo get optical data from dac
        # todo define grid from optical data
        # path_to_state_mask = config['General']['state_mask']
        # todo open state mask




# todo resample -> do resampling within inference engine ... for now

    @staticmethod
    def _increase_time_step(current_time: datetime, time_interval: int, time_interval_unit: str) -> None:
        if time_interval_unit is 'days':
            current_time += timedelta(days=time_interval)
        elif time_interval_unit is 'weeks':
            current_time += timedelta(weeks=time_interval)
        return current_time


    @staticmethod
    def _get_config(priors_sm_dir: str, priors_veg_dir: str, start_time: str, end_time: str, roi: str) -> dict:
        config = {}
        config['General'] = Orchestrator._get_general_config(start_time=start_time, end_time=end_time, roi=roi)
        config['Inference'] = Orchestrator._get_inference_config()
        config['Prior'] = Orchestrator._get_prior_config(priors_sm_dir=priors_sm_dir, priors_veg_dir=priors_veg_dir)
        return config

    @staticmethod
    def _get_general_config(start_time: str, end_time: str, roi: str) -> dict:
        start_time_as_string = start_time
        end_time_as_string = end_time
        time_interval = 1
        time_interval_unit = 'days'
        spatial_resolution_x = 10
        spatial_resolution_x_unit = 'm'
        spatial_resolution_y = 10
        spatial_resolution_y_unit = 'm'
        path_to_state_mask = '/path/to/my/state_mask.tif'
        output_directory_root = '/some/where/'
        general_dict = {}
        general_dict['roi'] = roi
        general_dict['start_time'] = start_time_as_string
        general_dict['end_time'] = end_time_as_string
        general_dict['time_interval'] = time_interval
        general_dict['time_interval_unit'] = time_interval_unit
        general_dict['spatial_resolution_x'] = spatial_resolution_x
        general_dict['spatial_resolution_x_unit'] = spatial_resolution_x_unit
        general_dict['spatial_resolution_y'] = spatial_resolution_y
        general_dict['spatial_resolution_y_unit'] = spatial_resolution_y_unit
        general_dict['state_mask'] = path_to_state_mask
        general_dict['output_directory_root'] = output_directory_root
        return general_dict

    @staticmethod
    def _get_inference_config() -> dict:
        parameters = ['sm', 'lai', 'cab']
        optical_operator_library = 'some_operator.nc'
        sar_operator_library = 'some_other_operator.nc'
        a_matrix = 'identity'
        inflation = 1e3
        inference_dict = {}
        inference_dict['parameters'] = parameters
        inference_dict['optical_operator_library'] = optical_operator_library
        inference_dict['sar_operator_library'] = sar_operator_library
        inference_dict['a_matrix'] = a_matrix
        inference_dict['inflation'] = inflation
        return inference_dict

    @staticmethod
    def _get_prior_config(priors_sm_dir: str, priors_veg_dir: str) -> dict:
        general_prior_directory = priors_veg_dir
        prior_general_dict = {}
        prior_general_dict['directory_data'] = general_prior_directory
        prior_sm_climatology_directory = priors_sm_dir
        prior_sm_climatology_dict = {}
        prior_sm_climatology_dict['climatology_dir'] = prior_sm_climatology_directory
        prior_sm_dict = {}
        prior_sm_dict['climatology'] = prior_sm_climatology_dict
        prior_lai_dict = {}
        prior_lai_dict['database'] = None
        prior_cab_dict = {}
        prior_cab_dict['database'] = None
        prior_dict = {}
        prior_dict['General'] = prior_general_dict
        prior_dict['sm'] = prior_sm_dict
        prior_dict['lai'] = prior_lai_dict
        prior_dict['cab'] = prior_cab_dict
        return prior_dict