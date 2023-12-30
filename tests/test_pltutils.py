from hdtimelines import pltutils
import pandas as pd

def test_check_dataframe():
    df = pd.read_csv('./test_data/Playwrights_extract_ok.csv', na_filter=False)
    result, message =  pltutils.check_dataframe(df)
    assert result

    df = pd.read_csv('./test_data/British Monarchs_extract_ok.csv', na_filter=False)
    result, message =  pltutils.check_dataframe(df)
    assert result
    
    assert pltutils.check_dataframe(df)
    df = pd.read_csv('./test_data/British Monarchs_extract_notok_no_label.csv', na_filter=False)
    result, message =  pltutils.check_dataframe(df)
    assert not result
    assert message == "Error: KeyError('label')"
    
