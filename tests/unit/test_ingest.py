from services.streamlit_app.app.utils.ingest import profile_df
import pandas as pd

def test_profile_df():
    df = pd.DataFrame({'a':[1,2,None],'b':[4,5,6]})
    p = profile_df(df)
    assert p['rows'] == 3
    assert 'a' in p['cols']
