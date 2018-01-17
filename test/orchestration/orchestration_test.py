from multiply_orchestration.orchestration import Orchestrator

PATH_TO_TEST_CONFIG = './test/test_data/test_config.yml'

def test_orchestration():
    Orchestrator.orchestrate(PATH_TO_TEST_CONFIG)