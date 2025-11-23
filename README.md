This project in Python analyzes Fair Value Gaps (FVGs) in major Forex currency pairs using data from Yahoo Finance. FVGs, defined by a three-candle structure, will be analyzed in both their bullish and bearish forms. The main research question of this review focuses on how frequently these FVGs are filled and how successful they are at predicting price continuation. Other aspects include whether there is a difference in the behavior of bullish and bearish FVGs, how gap size influences the fill probability, and whether FVGs created against the dominant market trend fill less frequently.



Data for pairs like the EUR/USD, GBP/USD, and USD/JPY will be collected over 30-minute, 1-hour, 4-hour, and 1-day timeframes over periods of six months to one year. Features like gap length, trend direction, volatility, liquidity zones, and time-to-fill will be extracted from the OHLC data. This will involve designing an algorithm that will detect FVGs; analyze the future price movement to determine whether the gaps fill completely, partially, or remain open; and gauge whether the identified FVGs correctly predict continued price movement in the expected direction. Comparison of fill rates, continuation accuracy, and behavior in various market conditions will be done through statistical analysis and visualizations. The project is guided by hypotheses that most FVGs will eventually fill, smaller gaps fill faster, higher-timeframe gaps are more reliable, and a valid FVG should correlate to price continuation in their respective direction.


Overall, this project intends to present a more empirical view of the reliability of FVGs by comparing their fill rates against their efficiency in predicting future price continuation.



