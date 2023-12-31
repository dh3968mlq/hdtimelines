import sys
sys.path.insert(0,".") # For Github
sys.path.insert(0,"./hdtimelines") # in case this is run when a submodule

import glob
from hdtimelines import pltutils
import pandas as pd

def test_check_dataframe():
    # Find test data path
    if glob.glob('./hdtimelines/test_data/'):
        path = './hdtimelines/test_data'
    else:
        path = './test_data'

    df = pd.read_csv(f'{path}/Playwrights_extract_ok.csv', na_filter=False)
    result, message =  pltutils.check_dataframe(df)
    assert result

    df = pd.read_csv(f'{path}/British Monarchs_extract_ok.csv', na_filter=False)
    result, message =  pltutils.check_dataframe(df)
    assert result
    
    assert pltutils.check_dataframe(df)
    df = pd.read_csv(f'{path}/British Monarchs_extract_notok_no_label.csv', na_filter=False)
    result, message =  pltutils.check_dataframe(df)
    assert not result
    assert message == "Error: KeyError('label')"
    
