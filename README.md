# Water Treatment Plant Data Generator

This simple project explores a wastewater treatment dataset and generates synthetic data for the purpose of testing data pipelines. We process the data and write it into a database.

The data generation process involves interpolating the original daily data down to 10-minute intervals, and adding some random noise to better mimic real-world time-series data. 

**Note:** While the generated data might mimic real-world data when plotted, it is important to understand that the complex relationships between the different variables have not been accounted for during the generation process. Thus, the generated data is not suitable for modeling or prediction tasks. The main purpose of this data generation is to create a synthetic dataset for testing data pipelines.

Please refer to the Jupyter notebook for more details about the data generation process. The app that utilizes this data is deployed [here](http://wwtp-data-app.herokuapp.com/).
