import sys
import yaml
from multiply_core.util import AttributeDict
from multiply_data_access import DataAccessComponent
import multiply_high_res_pre_processing
from sar_pre_processing import SARPreProcessor

class Orchestrator(object):

    @classmethod
    def orchestrate(cls, path_to_config: str) -> None:
        assert path_to_config is not None, 'ERROR: Configuration file needs to be provided'
        with open(path_to_config, 'r') as config_file:
            yaml_config = yaml.load(config_file)
            config = AttributeDict(**yaml_config)
        data_access_component = DataAccessComponent()
        # sar_pre_processor = SARPreProcessor()
        # sar_pre_processor.pre_process_step1()
        # sar_pre_processor.pre_process_step2()
        # sar_pre_processor.pre_process_step3()




        return None

def main(args=None) -> int:
    return Orchestrator.orchestrate()

if __name__ == '__main__':
    sys.exit(main())