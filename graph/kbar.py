#-*- encoding:utf8 -*-

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc


# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
date1 = (2016, 3, 10)
date2 = (2016, 4, 6)


mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
alldays = DayLocator()              # minor ticks on the days
dateFormatter = DateFormatter('%Y-%m-%d')  # e.g., 2013-2-12
dayFormatter = DateFormatter('%Y-%m-%d')      # e.g., 12

quotes = quotes_historical_yahoo_ohlc('AAPL', date1, date2)
if len(quotes) == 0:
    raise SystemExit

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(dateFormatter)

# ax.xaxis.set_minor_formatter(dayFormatter)
x = [(731621.0,23,33,12,22)]
# plot_day_summary(ax, quotes, ticksize=3)
candlestick_ohlc(ax, quotes, width=0.6,colorup='r', colordown='g')

ax.xaxis_date()
ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

plt.show()