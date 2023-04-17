# /Users/Trevor/Documents/Scripts/batch-forge python

import batch_variables as bv

def build_a_batch(batches_to_make: int,
                  material: str,
                  batch_length: int,
                  contents: int = 0,
                  include_OTs: bool = True,
                  min_length: bool = True) -> None:
    '''
    Accepts six variables: batches_to_make as an int; material as a string;
    batch_lenght as an int; contents as an int (default 0);
    include_OTs as a bool (default True); min_length as a bool (default True).

    Creates batches based on the provided arguments that are ready to import
    into Caldera. 

    Returns nothing.
    '''
    # Stars for loop to make the specified number of batches
    for batch_num in batches_to_make:

        # Resets the batch dict and available PDFs dict
        batch_dict: dict = bv.reset_batch_dict()
        available_pdfs: dict = bv.reset_available_pdfs()

        # Sets details about the batch
        batch_details = batch_dict['batch_details']
        batch_details['ID'] = bv.get_batch_id()
        batch_details['material'] = material
        batch_details['material_length'] = batch_length
        batch_details['include_OTs'] = include_OTs
        batch_details['contents'] = contents
        batch_details['care_about_minimum_length'] = min_length

        # Variables of batch_dict for easy reference
        material = batch_details['material']
        min_batch_length = batch_details['material_length'] * bv.standard_min_length

        # Gets available print PDFs
        fill_available_pdfs_dict(material, contents, include_OTs)


    return

def fill_available_pdfs_dict(material: str,
                             contents: int,
                             include_OTs: bool):
    '''
    
    '''