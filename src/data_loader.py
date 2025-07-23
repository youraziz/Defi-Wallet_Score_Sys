# Sometimes pandas can handle MongoDB JSON directly
try:
    df = pd.read_json('aave_v2_raw.json', lines=False)
    print("Loaded successfully with standard read_json")
    print(df.head())
except:
    print("Standard approach failed, trying the custom loader above")
