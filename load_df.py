
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


class DataSet():

        def __init__(self, transaction_path, identity_path):    

                df_trans = self.load_transaction_dataset(transaction_path)
                df_ident = self.load_identity_dataset(identity_path)

                df_final = df_trans.set_index("TransactionID").join(df_ident.set_index("TransactionID"))  
        
                self.df = df_final 
        

        def load_transaction_dataset(self, dataset_path):
                df_trans = pd.read_csv(dataset_path)
        
                # removing unimporttant(?) features
                trans_to_remove = ["card1", "card2", "card3", "card5", "addr1", "addr2"]
                df_trans = df_trans.drop(trans_to_remove, axis=1)

                #normalizing emails domain
                df_trans["R_emaildomain"] = df_trans.R_emaildomain.apply(self.normalize_email)
                df_trans["P_emaildomain"] = df_trans.P_emaildomain.apply(self.normalize_email)

                # applying one-hot-encode for categorical features

                trans_to_apply_one_hot = ["ProductCD", "card4", "card6", "P_emaildomain", "R_emaildomain", "M1", "M2", 
                                        "M3", "M4", "M5", "M6", "M7", "M8", "M9"]

                for col in trans_to_apply_one_hot:
                        self.apply_one_hot_encode(df_trans, col)

                return df_trans

        def load_identity_dataset(self, dataset_path):

                df_ident = pd.read_csv(dataset_path)


                #removing some categorical features with dimentionality
                ident_to_remove = ["DeviceInfo", "id_13", "id_14", "id_17", "id_18", "id_19", "id_20", "id_21", "id_24", "id_25", "id_26", 
                                "id_33", "id_32"]
                df_ident = df_ident.drop(ident_to_remove, axis=1)
        

                df_ident["id_30"] = df_ident["id_30"].apply(self.normalize_os)

                df_ident["id_31"] = df_ident["id_31"].apply(self.normalize_navigator)

                ident_to_apply_one_hot = ["DeviceType", "id_12", "id_15", "id_16", "id_23", "id_27","id_28", "id_29", "id_30", "id_31",
                                        "id_34", "id_35", "id_36", "id_37",  "id_38"]

                for col in ident_to_apply_one_hot:
                        self.apply_one_hot_encode(df_ident, col)

                return df_ident

        def compute_num_unique(self, df):
                for col, values in df.iteritems():
                        num_uniques = values.nunique()
                        print ('{name}: {num_unique}'.format(name=col, num_unique=num_uniques))
                        print (values.unique())
                        print ('\n')

        def normalize_email(self, email):
                # reducing the domains IPs to a low dimention to apply on hot encode
                filters = ["hotmail", "gmail", "yahoo", "live", "msn", "outlook"]    
                
                if isinstance(email, float):
                        return "None"
                
                for base_email in filters:
                        if email.find(base_email) >= 0:
                                return base_email
                return "other"

        # reducing the navigators space
        def normalize_navigator(self, navigator):
                import re
                if isinstance(navigator, float):
                        return "None"
                
                navigator_filters = {
                        'chrome for android': 'chrome (.+?) for android',
                        'chrome for ios': 'chrome (.+?) for ios', 
                        'ie for desktop': 'ie (.+?) for desktop',
                        'ie for tablet': 'ie (.+?) for tablet',  
                        'chrome':'^chrome ?([0-9]{2}\.[0-9])?(generic)?$', 
                        'opera': '^opera ?([0-9]{2}\.[0-9])?(generic)?$',
                        'safari': 'safari ?([0-9]{2}\.[0-9])?(generic)?$',
                        'edge': '^edge ([0-9]{1,2}\.[0-9]{1,2})?', 
                        'firefox': '^firefox ([0-9]{2}\.[0-9])?(generic)?$',  
                        'samsung': '^samsung? (browser)? ([0-9]{1,2}.[0-9]{1,2})?(generic)?'
                }
                
                for value, nav_filter in navigator_filters.items():
                        if not re.search(nav_filter, navigator) == None:            
                                return value
                
                return "other"

        def normalize_os(self, os_name):
        
                if isinstance(os_name, float):
                        return "None"
                
                navigator_filters = ['Android', 'iOS', 'Mac OS', 'Windows', 'Linux' ]
                
                for navigator in navigator_filters:
                        if os_name.find(navigator) >= 0:            
                                return navigator    
                return "other"

        def apply_one_hot_encode(self, df, column):
                df[column].fillna("None",inplace=True)
                df_encoded = pd.get_dummies(df[column])
                columns = df_encoded.columns
                print(columns)
                new_columns = {item: column + "-" + "-".join(item.split(" ")) for item in columns}
                df_encoded.rename(columns=new_columns, inplace=True)
                print(df_encoded.columns)
                for col in df_encoded.columns:
                        df[col] = df_encoded[col]
                
                del df[column]

