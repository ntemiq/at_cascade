# -----------------------------------------------------------------------------
# at_cascade: Cascading Dismod_at Analysis From Parent To Child Regions
#           Copyright (C) 2021-21 University of Washington
#              (Bradley M. Bell bradbell@uw.edu)
#
# This program is distributed under the terms of the
#     GNU Affero General Public License version 3.0 or later
# see http://www.gnu.org/licenses/agpl.txt
# -----------------------------------------------------------------------------
import csv
import at_cascade.ihme
# -----------------------------------------------------------------------------
#
# write_all_option_table
def write_all_option_table(
    root_node_name               = None,
    shift_prior_std_factor       = None,
    perturb_optimization_scaling = None,
    max_abs_effect               = None,
    max_fit                      = None,
    max_number_cpu               = None,
) :
    assert type(root_node_name)               == str
    assert type(max_abs_effect)               == float
    assert type(shift_prior_std_factor)       == float
    assert type(perturb_optimization_scaling) == float
    assert type(max_fit)                      == int
    assert type(max_number_cpu)               == int
    #
    # all_option
    all_option = {
        'absolute_covariates'          : 'one',
        'split_covariate_name'         : 'sex',
        'root_split_reference_name'    : 'Both',
        'root_node_name'               : root_node_name,
        'max_abs_effect'               : max_abs_effect,
        'max_fit'                      : max_fit,
        'max_number_cpu'               : max_number_cpu,
        'shift_prior_std_factor'       : shift_prior_std_factor,
        'perturb_optimization_scaling' : perturb_optimization_scaling,
    }
    #
    # all_option_table
    all_option_table = list()
    for key in all_option :
        row = { 'option_name' : key , 'option_value' : all_option[key] }
        all_option_table.append( row )
    #
    # all_option_table_file
    all_option_table_file = at_cascade.ihme.all_option_table_file
    #
    at_cascade.ihme.write_csv(all_option_table_file, all_option_table)