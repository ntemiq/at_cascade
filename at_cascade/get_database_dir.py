# -----------------------------------------------------------------------------
# at_cascade: Cascading Dismod_at Analysis From Parent To Child Regions
#           Copyright (C) 2021-21 University of Washington
#              (Bradley M. Bell bradbell@uw.edu)
#
# This program is distributed under the terms of the
#     GNU Affero General Public License version 3.0 or later
# see http://www.gnu.org/licenses/agpl.txt
# -----------------------------------------------------------------------------
'''
{xsrst_begin get_database_dir}
{xsrst_spell
    dir
}

Get Database Directory Corresponding To a Fit
#############################################

Syntax
******
{xsrst_file
    # BEGIN syntax
    # END syntax
}

node_table
**********
is the node_table for this cascade as a ``list'' of ``dict``.
It can't be ``None``.

split_reference_table
*********************
is the :ref:`split_reference_table` as a ``list`` of ``dict``.
It can't be ``None``.
If the list has lenght zero,
we say that the table is empty.

node_split_set
**************
If :ref:`split_reference_table` is empty,
this argument must be None.
Otherwise it is a ``set`` of ``int`` containing the
:ref:`node_split_table.node_id` values that appear in the
node_spit table.

root_node_id
************
is the node_id for the :ref:`glossary.root_node`.

root_split_reference_id
***********************
If :ref:`split_reference_table` is empty,
this argument must be None.
Otherwise it is an ``int`` specifying the
:ref:`split_reference_table.split_reference_id`
that the root node corresponds to.

fit_node_id
***********
This argument is an ``int`` is the node_id for the  :ref:`glossary.fit_node`.
It can't be ``None``.

fit_split_reference_id
**********************
If :ref:`split_reference_table` is empty,
this argument must be None.
Otherwise it is an ``int`` specifying the
:ref:`split_reference_table.split_reference_id`
that the fit corresponds to.

database_dir
************
The return value is a ``str`` containg the name of the directory
where the database corresponding to he fit is located.


{xsrst_end get_database_dir}
'''
import dismod_at
# ----------------------------------------------------------------------------
def get_database_dir(
# BEGIN syntax
# database_dir = at_cascade.get_database_dir(
    node_table              = None,
    split_reference_table   = None,
    node_split_set          = None,
    root_node_id            = None,
    root_split_reference_id = None,
    fit_node_id             = None ,
    fit_split_reference_id  = None,
# )
# END syntax
) :
    #
    # fit_split_reference_name
    row = split_reference_table[fit_split_reference_id]
    fit_split_reference_name = row['split_reference_name']
    #
    # database_dir
    database_dir = ''
    #
    # node_id, split_reference_id
    node_id            = fit_node_id
    split_reference_id = fit_split_reference_id
    #
    while node_id is not None :
        #
        # split
        split = root_split_reference_id != split_reference_id \
            and node_id in node_split_set
        #
        # next node_id, split_reference_id pair
        if split :
            # database_dir
            database_dir      = f'{fit_split_reference_name}/{database_dir}'
            split_reference_id = root_split_reference_id
        else :
            # database_dir
            node_name     = node_table[node_id]['node_name']
            database_dir = f'{node_name}/{database_dir}'
            node_id       = node_table[node_id]['parent']
    #
    # database_dir
    database_dir = database_dir[:-1]
    return database_dir