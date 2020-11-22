from typing import List
from requests.api import get
from math import ceil


def get_urls() -> List:
    """Get all the urls of details of the properties (for apartment and house)

    Returns:
        list: the list of the urls
    """
    search_values = ["apartment", "house"]
    nbr_pages = 1  
    all_url = []
    for value in search_values:
        url = f"https://www.immoweb.be/fr/search-results/{value}/a-vendre?countries=BE&page=1&orderBy=relevance"
        response = get(url)
        source = None
        if response.status_code == 200:
            source = response.json()

        if source:
            totalItems = source["totalItems"]
            # number of elements in a page
            nbr_elements = len(source["results"])
            nbr_pages = ceil(totalItems/nbr_elements)
            all_url += __get_detail_urls__(value,nbr_pages)
    return all_url

def __get_detail_urls__(search_value: str, nbr_pages: int) -> List:
    """construct each detail url

    Args:
        search_value (str): the property we search (apartment or gouse)
        nbr_pages (int): the number of page for the property searched

    Returns:
        list: the list of the urls for the property searched
    """
    detail_urls = []
    for i in range(nbr_pages):
        # get a search page
        url = f"https://www.immoweb.be/fr/search-results/{search_value}/a-vendre?countries=BE&page={i}&orderBy=relevance"
        response = get(url)
        source = None
        if response.status_code == 200:
            source = response.json()

        if source:
            results = source["results"]
            for j in range(len(results)):
                id_ = results[j]["id"]
                locality = results[j]["property"]["location"]["locality"]
                postal_code = results[j]["property"]["location"]["postalCode"]

                #for each result in the search page, get the detail url
                detail_urls.append(
                    f"https://www.immoweb.be/fr/annonce/{search_value}/a-vendre/{locality}/{postal_code}/{id_}")  
    return detail_urls


# TEST
if __name__ == '__main__':
    urls = get_urls()
    print(len(urls))
