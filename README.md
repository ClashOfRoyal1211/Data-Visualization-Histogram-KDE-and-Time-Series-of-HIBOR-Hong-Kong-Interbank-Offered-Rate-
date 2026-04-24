# Sky-Hackathon-2026

All of the code was generated using Gemini and Github Copilot Chat. This was a project I created out of an attempt to vizualise the Hong Kong's interest settlement rates--the rate at which banks and financial institutions lend and borrow between one another within the Hong Kong market. This is used to maintain the linked exchange rate of the Hong Kong dollar (HKD) against the US dollar.

<img width="2674" height="1028" alt="combined_rates_plot_sources" src="https://github.com/user-attachments/assets/bdaf7f6c-8fbc-46f6-a173-f8361996c8ed" />
Note: The data from the .csv and .php files were retrieved from the Hong Kong Government's Website, Accessed: 17 April, 2026. https://data.gov.hk/en-data/dataset/hk-censtatd-tablechart-340-45022.

Explanation on what each file of program does:
  json_parser 
    CPP file that converts the data from "get.php.json" to a .csv file, specifically "hkd_rates.csv" by filtering out bits of data like the "period" and allocating it to a coloumn on "hkd_rates.csv". 

  cppProcessData
    CPP file that organized the data from "../Table 340-45022_en.csv" and moves it to "hibor_processed.csv". I wanted to represent each interval shift in data by quarters (Q1, Q2, Q3, Q4), so only the data from the 3 months column in the original table was used.

  hkd_analysis.py

  
  combined_plot.py
    Combined the data generated from "cppProcessData" and "json_parser", and generated an image containing a intrest rate vs time series graph, and well as a histogram overlaid onto a Kernel Density Estimation (KDE) graph displaying frequency against the 3-month interest rate(%)

  
