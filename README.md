# Project Overview

In this project, I will use Python to analyze Fair Value Gaps (FVGs) in major Forex currency pairs using data sourced from Yahoo Finance. Specifically, I will examine the "three-candle structure" that defines bullish and bearish FVGs to determine their reliability. By focusing on pairs like EUR/USD, GBP/USD, and USD/JPY across multiple timeframes (30-minute to 4-hours), I aim to answer a critical research question: How frequently are these gaps filled, and how successful are they at predicting price continuation?

## Motivation

This project intends to present a more empirical view of the reliability of FVGs, moving beyond theoretical trading concepts to data-driven analysis. The findings will verify whether specific market conditions—such as gap size or dominant trend direction—influence the probability of a gap filling.

Ultimately, this analysis will allow traders to distinguish between high-probability setups and market noise, testing the hypothesis that if Fair Value Gaps are reasonable tools for the market price prediction.
## Description of Datasets

I will be utilizing financial market data accessed via the Yahoo Finance API:

**1. Forex OHLC Data (Yahoo Finance)**
* **Content:** Open, High, Low, and Close (OHLC) price data.
* **Scope:** Major currency pairs including EUR/USD, GBP/USD, and USD/JPY.
* **Timeframes:** Data will be collected across 30-minute, 1-hour and 4-hour intervals.
* **Duration:** A historical period ranging from 30 minutes to one year.

## Plan

### Data Collection and Exploratory Data Analysis (EDA)
* Data will be scraped/downloaded for the specified pairs and timeframes.
* Key features will be extracted from the OHLC data, including gap length and trend direction.
* Also the mean, median, standart deviation, min and max of the price data will be calculated for each dataset

### Algorithm Design and Detection
* An algorithm will be developed to detect valid FVG patterns (bullish and bearish three-candle structures).
* The system will analyze future price movements using the ML methods to classify gaps as completely filled, partially filled, or remaining open.
* Time-to-fill metrics will be calculated to gauge how quickly the market reacts to these gaps.

### Statistical Analysis and Visualization
* **Fill Rate Analysis:** Comparing how gap size and trend alignment (dominant trend vs. counter-trend) affect fill probability.
* **Continuation Accuracy:** Gauging whether identified FVGs correctly predict continued price movement in the expected direction.
* **Hypothesis Testing:** Validating if smaller gaps fill faster and if higher-timeframe gaps offer higher reliability compared to lower timeframes.
