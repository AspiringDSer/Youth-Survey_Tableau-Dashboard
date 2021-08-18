'''
The purpose of getsurvey.py is to streamline an API to call Youth Survey Datasets without downloading to local machine.
This also allows Users to easily create copies of the datasets. 
'''

import boto3
import pandas as pd 

##############################
# Youth Survey Data Pipeline #
##############################

class Survey:
    
    '''
    Manipulates Youth Survey datasets. Default S3 bucket is jmah-public-data.
    
    Parameters 
    ==========
    bucket: str, S3 bucket name to pull Youth Survey data from. jmah-public-data by default.
    
    Attributes
    ==========
    bucket: S3 bucket name
    s3: boto3.resource instance
    
    Methods
    =======
    get_all_filenames(): returns names of all available Youth Survey datasets retrieved 
    get_csv(key): returns a dataset for a given key 
    '''

    def __init__(self, bucket = 'jmah-public-data'):
        self.bucket = bucket
        self.s3 = boto3.resource('s3')
        
    def get_all_filenames(self, prefix = 'young-people-survey/'):

        '''
        Gets all the available datasets given a prefix on S3 Bucket
        The default is the default prefix for "jmah-public-data/young-people-survey/"
        The result is a list with all the CSV filenames. 

        Parameters
        ==========
        prefix: str, prefix on the S3 bucket where Youth Survey's datasets exist 
        '''
    
        prefix_objs = self.s3.Bucket(self.bucket).objects.filter(Prefix=prefix)
        for obj in prefix_objs:
            print(obj.key.split('/')[1])
            
    def get_csv(self, key):
        '''
        Takes in key argument
        Key argument indicates which dataset to request 
        The function returns a Pandas Dataframe

        Parameters
        ==========
        key: str, name of the csv file to retrieve 
        '''

        assert isinstance(key, (str)), 'Key must be a string datatype'
        
        key_name = 'young-people-survey/' + key
        
        df = pd.read_csv(self.s3.Object(bucket_name = self.bucket, key = key_name).get()['Body'])
        
        return df 
