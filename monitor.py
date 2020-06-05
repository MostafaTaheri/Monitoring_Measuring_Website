import json
import requests
import pandas as pd
import urllib
import time
import io
import datetime
import os


class Monitor(object):
    def __init__(self):
        self.response_object = {}
        self.df_pagespeed_results = None

    def monitoring(self, file_name, *args):
        """Monitoring and measurinng the website perofomance.
          
         Attributes:
               args: It contains url of websites.
               file_name: That is teh name of file which stored in json format.
         """
        try:
            for item in args:
                self.file_name = "{}.json".format(file_name)
                self.page_speed_results = self.__request(item)
                self.json_result = json.loads(self.page_speed_results)
                self.response_object[item] = self.json_result
                time.sleep(10)
            self.__make_json_file(self.file_name, self.response_object)
            self.__data_frame()
            self.__metrics(args, file_name=self.file_name)
            self.summary = self.df_pagespeed_results
            self.df_pagespeed_results.head()
            self.summary.to_csv(self.file_name.replace('json', 'csv'))
        except Exception as ex:
            return ex

    @staticmethod
    def __request(url):
        """API request to obtain content."""
        try:
            return urllib.request.urlopen(
                "https://www.googleapis.com/pagespeedonline/v5/" +
                "runPagespeed?url={}/&strategy=mobile".format(url)).read(
                ).decode('UTF-8')
        except Exception as ex:
            return ex

    def __data_frame(self):
        """Create dataframe to store responses."""
        try:
            self.df_pagespeed_results = pd.DataFrame(columns=[
                'url', 'Overall_Category', 'Largest_Contentful_Paint',
                'First_Input_Delay', 'Cumulative_Layout_Shift',
                'First_Contentful_Paint', 'Time_to_Interactive',
                'Total_Blocking_Time', 'Speed_Index'
            ])
            print(self.df_pagespeed_results)
        except Exception as ex:
            return ex

    def __metrics(self, *args, file_name):
        """Extract the metrics from the object response."""
        try:
            self.counter = 0
            for item in args:
                for (args, x) in zip(self.response_object.keys(),
                                     range(0, len(self.response_object))):
                    self.df_pagespeed_results.loc[x,
                                                  'url'] = item[self.counter]
                    self.df_pagespeed_results.loc[
                        x, 'Overall_Category'] = self.response_object[item[
                            self.
                            counter]]['loadingExperience']['overall_category']
                    self.df_pagespeed_results.loc[
                        x, 'Largest_Contentful_Paint'] = self.response_object[
                            item[self.counter]]['lighthouseResult']['audits'][
                                'largest-contentful-paint']['displayValue']
                    self.fid = self.response_object[item[self.counter]][
                        'loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']
                    self.df_pagespeed_results.loc[
                        x, 'First_Input_Delay'] = self.fid['percentile']
                    self.df_pagespeed_results.loc[
                        x, 'Cumulative_Layout_Shift'] = self.response_object[
                            item[self.counter]]['lighthouseResult']['audits'][
                                'cumulative-layout-shift']['displayValue']
                    self.df_pagespeed_results.loc[
                        x, 'First_Contentful_Paint'] = self.response_object[
                            item[self.counter]]['lighthouseResult']['audits'][
                                'first-contentful-paint']['displayValue']
                    self.df_pagespeed_results.loc[
                        x, 'Time_to_Interactive'] = self.response_object[item[
                            self.counter]]['lighthouseResult']['audits'][
                                'interactive']['displayValue']
                    self.df_pagespeed_results.loc[
                        x, 'Total_Blocking_Time'] = self.response_object[item[
                            self.counter]]['lighthouseResult']['audits'][
                                'total-blocking-time']['displayValue']
                    self.df_pagespeed_results.loc[
                        x, 'Speed_Index'] = self.response_object[item[
                            self.counter]]['lighthouseResult']['audits'][
                                'speed-index']['displayValue']
                    self.counter += 1
        except Exception as ex:
            print(ex)
            return ex

    def __make_json_file(self, file_name, content):
        """create json file."""
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
            with open(file_name, 'a') as file:
                json.dump(content, file)
        except Exception as ex:
            return ex

    @staticmethod
    def __download(url, file_name, output):
        """
            Downlaod and save file into your path
        """
        try:
            if not os.path.exists(output):
                os.makedirs(output)
            request.urlretrieve(url, "{}/{}".format(output, file_name))
            return True
        except:
            return False

    @staticmethod
    def read_json(file):
        try:
            with open(file, 'r') as json_file:
                return json.load(json_file)
        except:
            None
