from multiply_orchestration.frascati_orchestration import Orchestrator
import os
import shutil

__author__ = "Tonio Fincke (Brockmann Consult GmbH)"

TEST_PATH = './test/test_data/out'

def test_orchestrate():
    if os.path.exists(TEST_PATH):
        shutil.rmtree(TEST_PATH)
    os.mkdir(TEST_PATH)
    Orchestrator.orchestrate(TEST_PATH)
    shutil.rmtree(TEST_PATH)