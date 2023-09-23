from PIL import Image
import requests
from io import BytesIO

# Returns the dominant color in an image from a url
def main_image_color(url):
    response= requests.get(url)
    rgba_image = Image.open(BytesIO(response.content))

    rgb_image = Image.new("RGB", rgba_image.size, (255, 255, 255))
    rgb_image.paste(rgba_image, mask=rgba_image.split()[3])

    image = rgb_image

    color_count = {}

    for x in range(0,image.size[0],10):
        for y in range(0,image.size[1],10):
            pixel = image.getpixel((x,y))
            # Ignore colors close to white
            if not (pixel[0] > 150 and pixel[1] > 150 and pixel[2] > 150):
                color_count[pixel] = color_count.get(pixel, 0) + 1

    # If no non white colors, return greyish color
    if len(color_count) == 0:
        return '#BEBEBE'
    
    main_color = max(color_count, key=color_count.get)
    return '#' + ''.join(f'{i:02X}' for i in main_color)

from itertools import groupby
from django.db.models.functions import TruncDate

def group_transactions(transactions, interval, dict=True):

    transactions = transactions.annotate(date=TruncDate('time'))

    if interval == "day":
        key = lambda x: x.date
    elif interval == "time":
        key = lambda x: x.time
    elif interval == "month":
        key = lambda x: x.date.replace(day=1)
     
    groups = groupby(sorted(transactions,key=key,reverse=True), key=key)

    if dict:
        daily_transaction_sum = {str(date): sum(t.amount for t in group) for date, group in groups}
        return daily_transaction_sum
    else:
        return groups

def bar_data(transactions, interval):
    groups = group_transactions(transactions, interval, False)
    labels = []
    values = []
    for date, group in groups:
        if interval == 'day':
            labels.append(date.strftime("%d"))
        else:
            labels.append(date.strftime("%B"))
        values.append(sum(t.amount for t in group).amount)

    labels.reverse()
    values.reverse()

    data = group_transactions(transactions, interval)
    data = {date: amount.amount for date, amount in data.items()}
    return {'labels':labels,'values':values,'data':data}

def calculate_balance_history(transactions, balance, interval='day', format=True):

    # Group transactions by date
    daily_transaction_sum = group_transactions(transactions, interval)
    dates = sorted(daily_transaction_sum,reverse=True)

    daily_balances = {}
    for d in dates:
        if format:
            daily_balances[str(d)] = str(balance)
        else:
            daily_balances[str(d)] = balance.amount
        balance -= daily_transaction_sum[d]
    
    return daily_balances

from django.db.models import Max, Min, StdDev, Avg, Variance, Sum


def calculate_metrics(transactions, bar_interval='month'):
    res= {}

    res['total_amount_of_transactions'] = len(transactions)
    res['highest_transaction'] = transactions.aggregate(Max('amount')).get('amount__max') or 0
    res['lowest_transaction'] = transactions.aggregate(Min('amount')).get('amount__min') or 0
    res['average_transaction'] = transactions.aggregate(Avg('amount')).get('amount__avg') or 0
    res['variance'] = transactions.aggregate(Variance('amount')).get('amount__variance') or 0
    res['standard_deviation'] = transactions.aggregate(StdDev('amount')).get('amount__stddev') or 0

    res['bar_data']= bar_data(transactions, interval=bar_interval)

    res['net'] = transactions.aggregate(Sum('amount')).get('amount__sum')
    return res
    
def calculate_metrics_all(transactions,balance,bar_interval='month'):
    res= {}
    positive = transactions.filter(amount__gt=0)
    negative = transactions.filter(amount__lt=0)

    res['positive'] = calculate_metrics(positive, bar_interval)
    res['negative'] = calculate_metrics(negative, bar_interval)
    res['both'] = calculate_metrics(transactions, bar_interval)

    balance_history= calculate_balance_history(transactions, balance, interval='day', format=False)
    
    res['balance_history'] = calculate_balance_history(transactions, balance, interval='day', format=False)
    res['highest_balance'] = max(balance_history.items(), key=lambda x: x[1], default=('',0))[1]
    res['lowest_balance'] = min(balance_history.items(), key=lambda x: x[1], default=('',0))[1]

    res['total_money_in'] = positive.aggregate(Sum('amount')).get('amount__sum') or 0
    res['total_money_out'] = negative.aggregate(Sum('amount')).get('amount__sum') or 0
    res['net'] = transactions.aggregate(Sum('amount')).get('amount__sum',0)
    return res