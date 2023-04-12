'''
Contains functions for sorting PDFs by odd or even panel quantities, height,
and length for batching
'''

import getPdfData as get_pdf_data


def calculate_full_length(glob_of_pdfs: list) -> int:
    '''
    Accepts list of PDFs, calls sortPdfsByLength to srot them by length, then
    calculates their full length.
    '''
    sorted_list = sort_pdf_list(glob_of_pdfs)
    total_pdf_length = 0
    find_odd = False
    odd_match_height = 0
    for print_pdf in sorted_list:
        pdfLength = get_pdf_data.length(print_pdf)
        pdf_odd_or_even = get_pdf_data.oddOrEven(print_pdf)
        pdf_height = get_pdf_data.height(print_pdf)
        if find_odd is False:
            total_pdf_length += pdfLength
            if pdf_odd_or_even == 1:
                find_odd = True
                odd_match_height = pdf_height
        elif find_odd is True:
            if pdf_odd_or_even == 1:
                if odd_match_height == pdf_height:
                    total_pdf_length += (pdfLength - (pdf_height + .5))
                    find_odd = False
                else:
                    total_pdf_length += pdfLength
                    odd_match_height = pdf_height
    return total_pdf_length


def sort_pdfs_by_length(pdf_dict: dict) -> dict:
    '''
    Accepts a dict of two lists of paths to PDFs and sorts them by length,
    greatest to least. Returns a dict.
    '''
    list_to_sort = []
    sorted_list = []
    for even_or_odd_list in pdf_dict:
        for height_list in pdf_dict[even_or_odd_list]:
            for print_pdf in pdf_dict[even_or_odd_list][height_list]:
                pdf_length = get_pdf_data.length(print_pdf)
                list_to_sort.append((pdf_length, print_pdf))
            list_to_sort.sort(reverse=True, key=lambda pdf: pdf[0])
            pdf_list = list_to_sort
            list_to_sort = []
            for print_pdf in pdf_list:
                sorted_list.append(print_pdf[1])
            pdf_dict[even_or_odd_list][height_list] = sorted_list
            sorted_list = []
    return pdf_dict


def sort_pdf_list_by_odds(pdf_list: list) -> dict:
    '''
    Accepts a list of paths to PDFs. Sorts them into two lists of even-quantity
    and odd-quantity, then stores them in a dict. Returns the dicts.
    '''
    sortedPdfs = {
        'even_pdfs': [],
        'odd_pdfs': [],
    }
    for print_pdf in pdf_list:
        pdfOdd = get_pdf_data.oddOrEven(print_pdf)
        if pdfOdd == 1:
            sortedPdfs['odd_pdfs'].append(print_pdf)
        else:
            sortedPdfs['even_pdfs'].append(print_pdf)
    return sortedPdfs


def sort_by_height(pdf_dict: dict) -> dict:
    '''
    Accpets a dictionary of pdfs that have been sorted by odd or even quantity,
    then sorts each pdf into a list based on height. Returns a dict of lists
    of heights.
    '''
    sorted_dict = {
        '146.25': [],
        '136.25': [],
        '124.25': [],
        '112.25': [],
        '100.25': [],
        '88.25': [],
        '76.25': [],
        '64.25': [],
        '52.25': [],
        '40.25': [],
    }
    for list_to_sort in pdf_dict:
        for print_pdf in pdf_dict[list_to_sort]:
            pdf_height = str(get_pdf_data.height(print_pdf))
            sorted_dict[pdf_height].append(print_pdf)
        pdf_dict[list_to_sort] = sorted_dict
        sorted_dict = {
            '146.25': [],
            '136.25': [],
            '124.25': [],
            '112.25': [],
            '100.25': [],
            '88.25': [],
            '76.25': [],
            '64.25': [],
            '52.25': [],
            '40.25': [],
        }
    return pdf_dict


def combine_pdf_lists(pdf_dict: dict) -> list:
    '''
    Accepts a dictionary of paths to pdfs that have been sorted by odd or even
    quantity, then height, then length. Combines them all into a single list
    and returns that list.
    '''
    sorted_list = []
    for odd_list in pdf_dict:
        for height_list in pdf_dict[odd_list]:
            for print_pdf in pdf_dict[odd_list][height_list]:
                sorted_list.append(print_pdf)
    return sorted_list


def sort_pdf_list(pdf_list: list) -> list:
    '''
    Accepts a list of PDF paths, sorts them by odd or even panels count, then
    by height, then length, and finally combines them back to a single list
    and returns the list.
    '''
    sorted_by_odds = sort_pdf_list_by_odds(pdf_list)
    sorted_by_height = sort_by_height(sorted_by_odds)
    sorted_by_length = sort_pdfs_by_length(sorted_by_height)
    pdf_list = combine_pdf_lists(sorted_by_length)
    return pdf_list
