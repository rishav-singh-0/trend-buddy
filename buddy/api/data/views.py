from django.http import HttpResponse
from .get_data import YahooFinanceDataFetcher


def index(request):

    fetcher = YahooFinanceDataFetcher("TCS", "NSE")
    fetcher.fetch_data("1-1-2020", "25-8-2023")
    data = fetcher.save_to_database()
    print(data)
    
    return HttpResponse("Data Home Page")