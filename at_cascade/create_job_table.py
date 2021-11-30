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
{xsrst_begin create_job_table}

Table of Jobs That Can Run in Parallel
######################################

Under Construction
******************

Syntax
******
{xsrst_file
    # BEGIN syntax
    # END syntax
}

Purpose
*******
This routine returns a list of shift (node_id, split_reference_id) pairs
with a corresponding fit (node_id, split_reference_id) pair.
Each shift pairs requires the corresponding fit pair to have completed before
it can be run.

all_node_database
*****************
is a python string specifying the location of the
:ref:`all_node_db<all_node_db>`
relative to the current working directory.
This argument can't be ``None``.

fit_node_database
*****************
is a python string specifying the location of a
:ref:`glossary.fit_node_database`
relative to the current working directory.
This argument can't be ``None``.

start_node_id
*************
This, together with *start_split_reference_id*
corresponds to a completed fit that we are starting from.

start_split_reference_id
************************
This, together with *start_node_id*
corresponds to a completed fit that we are starting from.
Only jobs that depend on the start jobs completion will be included in
the job table.

fit_goal_set
************
This is the :ref:`glossary.fit_goal_set`.

job_table
*********
The return value *job_table* is a ``list``.
Each row of the list is a ``dict`` with the following keys:
node_id, split_reference_id, job_id.
The pair node_id, split_reference_id identifies a job that can be run.
In the special case where the pair is start_node_id, start_split_reference_id,
the job_id is None.


{xsrst_end create_job_table}
'''
# -----------------------------------------------------------------------------
import dismod_at
import at_cascade
# -----------------------------------------------------------------------------
def get_shift_job_table(
    job_id                     ,
    fit_node_id                ,
    fit_split_reference_id     ,
    root_split_reference_id    ,
    split_reference_table      ,
    node_split_set             ,
    fit_children               ,
) :
    #
    # already_split
    already_split = root_split_reference_id != fit_split_reference_id
    #
    # shift_reference_set
    if already_split or fit_node_id not in node_split_set :
        shift_reference_set = { fit_split_reference_id }
    else :
        shift_reference_set = set( range( len(split_reference_table) ) )
        shift_reference_set.remove( root_split_reference_id )
    #
    # shift_node_set
    if fit_node_id in node_split_set and not already_split :
        shift_node_set = { fit_node_id }
    else :
        shift_node_set = fit_children[ fit_node_id ]
    #
    # shift_job_table
    shift_job_table = list()
    for shift_split_reference_id in shift_reference_set :
        for shift_node_id in shift_node_set :
            row = {
                'node_id'            : shift_node_id,
                'split_reference_id' : shift_split_reference_id,
                'job_id'             : job_id,
            }
            shift_job_table.append( row )
    #
    return shift_job_table
# -----------------------------------------------------------------------------
def create_job_table(
# BEGIN syntax
# job_table = at_cascade.create_job_table(
    all_node_database          = None,
    fit_node_database          = None,
    start_node_id              = None,
    start_split_reference_id   = None,
    fit_goal_set               = None,
# )
# END syntax
) :
    #
    # node_table, covariate_table
    new             = False
    connection      = dismod_at.create_connection(fit_node_database, new)
    node_table      = dismod_at.get_table_dict(connection, 'node')
    covariate_table = dismod_at.get_table_dict(connection, 'covariate')
    connection.close()
    #
    # all_table
    all_table = dict()
    new        = False
    connection = dismod_at.create_connection(all_node_database, new)
    tbl_list   =  [ 'all_option', 'split_reference', 'node_split' ]
    for name in tbl_list :
        all_table[name] = dismod_at.get_table_dict(connection, name)
    connection.close()
    #
    # node_split_set
    node_split_set = set()
    for row in all_table['node_split'] :
        node_split_set.add( row['node_id'] )
    #
    # root_node_name
    root_node_name = None
    for row in all_table['all_option'] :
        if row['option_name'] == 'root_node_name' :
            root_node_name = row['option_value']
    assert root_node_name is not None
    #
    # root_node_id
    root_node_id = at_cascade.table_name2id(node_table, 'node', root_node_name)
    #
    # fit_children
    fit_children = at_cascade.get_fit_children(
        root_node_id, fit_goal_set, node_table
    )
    #
    # root_split_reference_id
    root_split_reference_name = None
    for row in all_table['all_option'] :
        if row['option_name'] == 'root_split_reference_name' :
            root_split_reference_name = row['option_value']
    if root_split_reference_name is None :
        root_split_reference_id = None
    else :
        root_split_reference_id = at_cascade.table_name2id(
            all_table['split_reference'],
            'split_reference',
            root_split_reference_name
        )
    #
    # job_table
    job_table = [ {
        'node_id'            : start_node_id,
        'split_reference_id' : start_split_reference_id,
        'job_id'             : None,
    } ]
    #
    # job_id
    job_id = 0
    #
    while job_id < len(job_table) :
        #
        # node_id, split_reference
        row                = job_table[job_id]
        node_id            = row['node_id']
        split_reference_id = row['split_reference_id']
        #
        # child_job_table
        child_job_table    = get_shift_job_table(
            job_id,
            node_id,
            split_reference_id,
            root_split_reference_id,
            all_table['split_reference'],
            node_split_set,
            fit_children,
        )
        #
        # job_table
        job_table += child_job_table
        #
        # job_id
        job_id += 1
    #
    return job_table