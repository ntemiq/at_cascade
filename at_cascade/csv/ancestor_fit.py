# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: University of Washington <https://www.washington.edu>
# SPDX-FileContributor: 2021-23 Bradley M. Bell
# ----------------------------------------------------------------------------
r'''
{xrst_begin csv.ancestor_fit}

Determine Closet Ancestor With Fit and Samples
##############################################

Prototype
*********
{xrst_literal ,
   # BEGIN_DEF, # END_DEF
   # BEGIN_RETURN, # END_RETURN
}

fit_dir
*******
is the directory where the csv files are located.

job_table
*********
is the :ref:`create_job_table@job_table` for this cascade.

predict_job_id
**************
is the :ref:`create_job_table@job_table@job_id` for this prediction.

node_table
**********
is the list of dict corresponding to the node table for this cascade.

root_node_id
************
is the node_id in the node table for the root node for this cascade.
Note that csv version of the cascade does its sex split at this node.

root_split_reference_id
***********************
is the split_reference_id (sex id) for the root node of the cascade.
The cascade can begin at female, both, or male.

error_message_dict
******************
It a dictionary, with keys equal to job names, containing
the error message for this cascade.

predict_job_dir
***************
This is the directory, relative to the *fit_dir*,
that corresponds to the *predict_job_id* .
See :ref:`get_database_dir-name` .

ancestor_job_dir
****************
This is the directory, relative to the *fit_dir*,
that corresponds to the closes ancestor of *predict_job_id*
that had a successful fit and posterior sampling.
The can be equal to *predict_job_dir*  (the closest possible case).


{xrst_end csv.ancestor_fit}
'''
import os
import at_cascade

# BEGIN_DEF
# at_cascade.csv.ancestor_fit
def ancestor_fit(
   fit_dir,
   job_table,
   predict_job_id,
   node_table,
   root_node_id,
   split_reference_table,
   root_split_reference_id,
   error_message_dict,
) :
   assert type(fit_dir) == str
   assert type(job_table) == list
   assert type(predict_job_id) == int
   assert type(node_table) == list
   assert type( root_node_id ) == int
   assert type(split_reference_table) == list
   assert type( root_split_reference_id) == int
   assert type( error_message_dict ) == dict
   # END_DEF
   #
   # node_split_set
   node_split_set = { root_node_id }
   #
   # job_name, predict_node_id, predict_split_reference_id
   job_row                     = job_table[predict_job_id]
   job_name                    = job_row['job_name']
   predict_node_id             = job_row['fit_node_id']
   predict_split_reference_id  = job_row['split_reference_id']
   #
   # predict_job_dir, ancestor_job_dir
   predict_job_dir = at_cascade.get_database_dir(
      node_table              = node_table                     ,
      split_reference_table   = split_reference_table          ,
      node_split_set          = node_split_set                 ,
      root_node_id            = root_node_id                   ,
      root_split_reference_id = root_split_reference_id        ,
      fit_node_id             = predict_node_id                ,
      fit_split_reference_id  = predict_split_reference_id     ,
   )
   #
   # have_fit
   predict_node_database = f'{fit_dir}/{predict_job_dir}/dismod.db'
   if not os.path.exists( predict_node_database ) :
      have_fit = False
   elif job_name not in error_message_dict :
      have_fit = True
   else :
      have_fit  = len( error_message_dict[job_name] ) < 2
   if have_fit :
      ancestor_job_dir = predict_job_dir
      return predict_job_dir, ancestor_job_dir
   #
   # job_id, ancestor_job_dir
   job_id            = predict_job_id
   while not have_fit :
      #
      # job_id
      job_id = job_table[job_id]['parent_job_id']
      if job_id == None :
         ancestor_job_dir = None
         assert type(predict_job_dir) == str
         return predict_job_dir, ancestor_job_dir
      #
      # job_name, ancestor_node_id, ancestor_split_reference_id
      job_row                      = job_table[job_id]
      job_name                     = job_row['job_name']
      ancestor_node_id             = job_row['fit_node_id']
      ancestor_split_reference_id  = job_row['split_reference_id']
      #
      # ancestor_job_dir
      ancestor_job_dir = at_cascade.get_database_dir(
         node_table              = node_table                     ,
         split_reference_table   = split_reference_table          ,
         node_split_set          = node_split_set                 ,
         root_node_id            = root_node_id                   ,
         root_split_reference_id = root_split_reference_id        ,
         fit_node_id             = ancestor_node_id               ,
         fit_split_reference_id  = ancestor_split_reference_id     ,
      )
      #
      # have_fit
      ancestor_job_database = f'{fit_dir}/{ancestor_job_dir}/dismod.db'
      if not os.path.exists( ancestor_job_database ) :
         have_fit = False
      elif job_name not in error_message_dict :
         have_fit = True
      else :
         have_fit  = len( error_message_dict[job_name] ) < 2
   #
   # BEGIN_RETURN
   assert type(predict_job_dir) == str
   if type(ancestor_job_dir) == str :
      assert predict_job_dir.startswith(ancestor_job_dir)
   else :
      assert ancestor_job_dir == None
   #
   return predict_job_dir, ancestor_job_dir
   # END_RETURN
