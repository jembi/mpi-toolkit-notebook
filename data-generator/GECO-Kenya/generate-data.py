# generate-data.py - Python module to generate synthetic data based on
#                    look-up files and error tables for Record Linkage purpose.
#
# The original program with some attributes was written by Peter Christen
# and Dinusha Vatsalan in January-March 2012.
# Modified by Sepideh Mosaferi 07/01/2017.
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

import random
import sys

import attrgenfunct  # Functions to generate independent attribute values
# Import the necessary other modules of the data generator
#
import basefunctions  # Helper functions
import corruptor  # Main classes to corrupt attribute values and records
import generator  # Main classes to generate records and the data set

random.seed(42)  # Set seed for random generator, so data generation can
#                       be repeated

#@title Run Data Generator

#define variables (this section is in seperate cells in the notebook)
#@title Data Generator Variables

#Probability Distribution for Attributes
given_name_val= 0.22
family_name_val= 0.16
gender_val=0.08
dob_val=0.19
city_val=0.09
pn_val=0.07
nid_val=0.19

# Data Generator parameters 
max_duplicate_per_record =  2 

num_duplicates_distribution = 'zipf' 

max_modification_per_attr = 1 

num_modification_per_record = 4 

#Given Name Corruptor

missing_val_FN = 0.1 
name_misspell_FN = 0.1 
edit_FN = 0.1 
ocr_FN = 0.1 
keyboard_FN = 0.1 
phonetic_FN = 0.5 

#Family Name Corruptor

missing_val_LN = 0.1 
name_misspell_LN = 0.1 
edit_LN = 0.1 
ocr_LN = 0.1 
keyboard_LN = 0.1 
phonetic_LN = 0.5 

#Gender at Birth Corruptor

missing_val_GAB = 0.2 
ocr_GAB = 0.4 
keyboard_GAB = 0.4

#Date of Birth Corruptor

missing_val_DOB = 0.5 
keyboard_DOB = 0.5 

#City Corruptor

missing_val_C = 0.2 
edit_C = 0.4 
phonetic_C = 0.4 


#Phone Number Corruptor

missing_val_PN = 0.2 
edit_PN = 0.4 
keyboard_PN = 0.4

#National ID Corruptor

missing_val_NID = 0.4 
ocr_NID = 0.2 
keyboard_NID = 0.4 



number_of_originals =  1000 
number_of_duplicates =  500

##


output.create_file()= 'data-{}-{}.csv'.format(num_org_rec, num_dup_rec)


ATTR_NAME = "Given Name"  # IN
ATTR_LAST_NAME = "Family Name"  # IN
ATTR_GENDER = "Gender at Birth"  # IN
ATTR_DOB = "Date of Birth"  # IN
ATTR_CITY = "City"  # IN
ATTR_PHONE_NUMBER = "Phone Number"  # IN [optional]
ATTR_NATIONAL_ID = "National ID"  # IN [optional]

# Set the Unicode encoding for this data generation project. This needs to be
# changed to another encoding for different Unicode character sets.
# Valid encoding strings are listed here:
# http://docs.python.org/library/codecs.html#standard-encodings
#
unicode_encoding_used = 'utf_8'

# ascii was used previouisly but caused encoding errors 

# The name of the record identifier attribute (unique value for each record).
# This name cannot be given as name to any other attribute that is generated.
#
rec_id_attr_name = 'ID'

# Set how many original and how many duplicate records are to be generated.
#

num_org_rec = int(number_of_originals)
num_dup_rec = int(number_of_duplicates)

# Set the file name of the data set to be generated (this will be a comma
# separated values, CSV, file).
#
out_file_name = 'data-{}-{}.csv'.format(num_org_rec, num_dup_rec)



# Check if the given the unicode encoding selected is valid.
#
basefunctions.check_unicode_encoding_exists(unicode_encoding_used)

# -----------------------------------------------------------------------------
# Define the attributes to be generated (using methods from the generator.py
# module).
#


name_gender_attr = \
    generator.GenerateCateCateCompoundAttribute(
        categorical1_attribute_name=ATTR_NAME,
        categorical2_attribute_name=ATTR_GENDER,
        lookup_file_name='/content/mpi-toolkit-notebook/data-generator/GECO-Kenya/lookup-files/given-name-gender-freq.csv',
        has_header_line=False,
        unicode_encoding=unicode_encoding_used)
    
lastName_attr = \
    generator.GenerateFreqAttribute(
        attribute_name=ATTR_LAST_NAME,
        freq_file_name='/content/mpi-toolkit-notebook/data-generator/GECO-Kenya/lookup-files/family-name-freq.csv',
        has_header_line=False,
        unicode_encoding=unicode_encoding_used)
    
date_of_birth_attr = \
    generator.GenerateFuncAttribute(
        attribute_name=ATTR_DOB,
        function=attrgenfunct.generate_date_of_birth)
    
city_attr = \
    generator.GenerateFreqAttribute(
         attribute_name=ATTR_CITY,
         freq_file_name='/content/mpi-toolkit-notebook/data-generator/GECO-Kenya/lookup-files/city-freq.csv',
         has_header_line=False,
         unicode_encoding=unicode_encoding_used)

phone_num_attr = \
    generator.GenerateFuncAttribute(
        attribute_name=ATTR_PHONE_NUMBER,
        function=attrgenfunct.generate_phone_number_ethiopia)

national_id_attr = \
    generator.GenerateFuncAttribute(
        attribute_name=ATTR_NATIONAL_ID,
        function=attrgenfunct.generate_national_id_number)


# -----------------------------------------------------------------------------
# Define how the generated records are to be corrupted (using methods from
# the corruptor.py module).

# For a value edit corruptor, the sum or the four probabilities given must
# be 1.0.
#
edit_corruptor = \
    corruptor.CorruptValueEdit(
        position_function=corruptor.position_mod_normal,
        char_set_funct=basefunctions.char_set_ascii,
        insert_prob=0.5,
        delete_prob=0.5,
        substitute_prob=0.0,
        transpose_prob=0.0)

edit_corruptor2 = \
    corruptor.CorruptValueEdit(
        position_function=corruptor.position_mod_uniform,
        char_set_funct=basefunctions.char_set_ascii,
        insert_prob=0.25,
        delete_prob=0.25,
        substitute_prob=0.25,
        transpose_prob=0.25)

name_misspell_corruptor = \
    corruptor.CorruptCategoricalValue(
        lookup_file_name='/content/mpi-toolkit-notebook/data-generator/GECO-Kenya/lookup-files/name-misspell.csv',
        has_header_line=False,
        unicode_encoding=unicode_encoding_used)

name_m_misspell_corruptor = \
    corruptor.CorruptCategoricalValue(
        lookup_file_name='/content/mpi-toolkit-notebook/data-generator/GECO-Kenya/lookup-files/name-m-misspell.csv',
        has_header_line=False,
        unicode_encoding=unicode_encoding_used)


ocr_corruptor = corruptor.CorruptValueOCR(
    position_function=corruptor.position_mod_normal,
    lookup_file_name='/content/mpi-toolkit-notebook/data-generator/GECO-Kenya/lookup-files/ocr-variations.csv',
    has_header_line=False,
    unicode_encoding=unicode_encoding_used)

keyboard_corruptor = corruptor.CorruptValueKeyboard(
    position_function=corruptor.position_mod_normal,
    row_prob=0.5,
    col_prob=0.5)

phonetic_corruptor = corruptor.CorruptValuePhonetic(
    lookup_file_name='/content/mpi-toolkit-notebook/data-generator/GECO-Kenya/lookup-files/phonetic-variations.csv',
    has_header_line=False,
    unicode_encoding=unicode_encoding_used)

missing_val_corruptor = corruptor.CorruptMissingValue()

# -----------------------------------------------------------------------------
# Define the attributes to be generated for this data set, and the data set
# itself.
#
attr_name_list = [ATTR_NAME,
                  ATTR_LAST_NAME,
                  ATTR_GENDER,
                  ATTR_DOB,
                  ATTR_CITY,
                  ATTR_PHONE_NUMBER,
                  ATTR_NATIONAL_ID
                 
                  ]

attr_data_list = [  name_gender_attr,
    lastName_attr,
    date_of_birth_attr,
    city_attr,
    phone_num_attr,
    national_id_attr,

    ]

# Nothing to change here - set-up the data set generation object.
#
test_data_generator = generator.GenerateDataSet(
    output_file_name=out_file_name,
    write_header_line=True,
    rec_id_attr_name=rec_id_attr_name,
    number_of_records=num_org_rec,
    attribute_name_list=attr_name_list,
    attribute_data_list=attr_data_list,
    unicode_encoding=unicode_encoding_used)

# Define the probability distribution of how likely an attribute will be
# selected for a modification.
# Each of the given probability values must be between 0 and 1, and the sum of
# them must be 1.0.
# If a probability is set to 0 for a certain attribute, then no modification
# will be applied on this attribute.
#
attr_mod_prob_dictionary = {
    ATTR_NAME: given_name_val,
    ATTR_LAST_NAME: family_name_val,
    ATTR_GENDER:gender_val,
    ATTR_DOB: dob_val,
    ATTR_CITY: city_val,
    ATTR_PHONE_NUMBER: pn_val,
    ATTR_NATIONAL_ID: nid_val,
    
    }


# Define the actual corruption (modification) methods that will be applied on
# the different attributes.
# For each attribute, the sum of probabilities given must sum to 1.0.
#
attr_mod_data_dictionary = {   
    ATTR_NATIONAL_ID: [(missing_val_NID, missing_val_corruptor),
                       (ocr_NID, ocr_corruptor),
                       (keyboard_NID, keyboard_corruptor)],
    ATTR_NAME: [(missing_val_FN, missing_val_corruptor),
                (name_misspell_FN, name_misspell_corruptor),
                (edit_FN, edit_corruptor2),
                (ocr_FN, ocr_corruptor),
                (keyboard_FN, keyboard_corruptor),
                (phonetic_FN, phonetic_corruptor)],
    ATTR_LAST_NAME: [(missing_val_LN, missing_val_corruptor),
                        (name_misspell_LN, name_m_misspell_corruptor),
                        (edit_LN, edit_corruptor2),
                        (ocr_LN, ocr_corruptor),
                        (keyboard_LN, keyboard_corruptor),
                        (phonetic_LN, phonetic_corruptor)],
    ATTR_GENDER: [(missing_val_GAB, missing_val_corruptor),
                  (ocr_GAB, ocr_corruptor),
                  (keyboard_GAB, keyboard_corruptor)],
    ATTR_DOB: [(missing_val_DOB, missing_val_corruptor),
               (keyboard_DOB, keyboard_corruptor)],
    ATTR_CITY: [(missing_val_C, missing_val_corruptor),
                (edit_C, edit_corruptor),
                (phonetic_C, phonetic_corruptor)],
    ATTR_PHONE_NUMBER: [(missing_val_PN, missing_val_corruptor),
                        (edit_PN, edit_corruptor2),
                        (keyboard_PN, keyboard_corruptor)]
   
}

# Nothing to change here - set-up the data set corruption object
#
test_data_corruptor = corruptor.CorruptDataSet(
    number_of_org_records=num_org_rec,
    number_of_mod_records=num_dup_rec,
    attribute_name_list=attr_name_list,
    max_num_dup_per_rec=max_duplicate_per_record,
    num_dup_dist=num_duplicates_distribution,
    max_num_mod_per_attr=max_modification_per_attr,
    num_mod_per_rec=num_modification_per_record,
    attr_mod_prob_dict=attr_mod_prob_dictionary,
    attr_mod_data_dict=attr_mod_data_dictionary)

# =============================================================================
# No need to change anything below here

# Start the data generation process
#
rec_dict = test_data_generator.generate()

# Check the number of generated records
assert len(rec_dict) == num_org_rec

# Corrupt (modify) the original records into duplicate records
#
rec_dict = test_data_corruptor.corrupt_records(rec_dict)

# Check total number of records
assert len(rec_dict) == num_org_rec + num_dup_rec

# Write generate data into a file
#
test_data_generator.write()

# End.
# =============================================================================

