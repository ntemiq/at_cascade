# -----------------------------------------------------------------------------
# at_cascade: Cascading Dismod_at Analysis From Parent To Child Regions
#           Copyright (C) 2021-22 University of Washington
#              (Bradley M. Bell bradbell@uw.edu)
#
# This program is distributed under the terms of the
#     GNU Affero General Public License version 3.0 or later
# see http://www.gnu.org/licenses/agpl.txt
# -----------------------------------------------------------------------------
"""
{xrst_begin_parent simulate}
{xrst_spell
    dir
}

Simulate an AT Cascade Data Set
###############################

Under Construction
******************

Syntax
******
{xrst_file
        # BEGIN Syntax
        # END Syntax
}

simulate_dir
************
This ``str`` is the directory name where the CSV input and output files
are located.


Demographer Notation
********************
None of the data is in demographer notation.
For example,
:ref:`simulate_csv_in@covariate.csv@time` 1990 means the beginning of 1990,
not the time interval from 1990 to 1991.

Rectangular Grid
****************
A CSV file is said to have a rectangular grid in columns
*name_a* , *name_b*, *name_c* if the following holds:

#.  The CSV file has columns with the names
    *name_a*, *name_b*, *name_c*.

#.  :math:`( a_1 , \ldots , a_L )`
    is the vector of values in column *name_a* .

#.  :math:`( b_1 , \ldots , b_M )`
    is the vector of values in column *name_b* .

#.  :math:`( c_1 , \ldots , c_N )`
    is the vector of values in column *name_c* .

#.  For :math:`\ell = 1 , \ldots , L`,
    :math:`m = 1 , \ldots , M`,
    :math:`n = 1,  \ldots , N` ,
    there is one and only one row with
    *name_a* equal to :math:`a_\ell`,
    *name_b* equal to :math:`b_m`, and
    *name_c* equal to :math:`c_n`.

Covariates
**********
For these simulations, all the covariates are
:ref:`glossary@relative_covariate` (called country covariates at IHME).
Sex is the
:ref:`all_option_table@split_covariate_name` and is not
referred to as a covariate for this simulations.

CSV Files
*********
{xrst_child_list}

{xrst_end simulate}

===============================================================================

{xrst_begin simulate_csv_in}
{xrst_spell
    csv
    std
    cv
}

simulate CSV Input Files
#########################

option.csv
**********
This csv file has two columns,
one called ``name`` and the other called ``value``.
The rows are documented below by the name column:

std_random_effects
==================
This is the standard deviation of the random effects.
All fo the effects are in log of rate space, so this standard deviation
is also in log of rate space.

-----------------------------------------------------------------------------

node.csv
********
This csv file defines the node tree.
It has the following columns (it may have others):

node_name
=========
This text is a name describing the node in a way that is easy for a human to
remember. It be unique for each row.

node_id
=======
For each row, the value in this column is the number of rows that come before
this row, not counting the header row.
In other words, it counts the data rows starting at row index zero.

parent_node_id
==============
This integer is the node_id corresponding to the parent node for this node.
The root node of the tree has an empty entry for this column.
If a node is a parent, it must have at least two children.
This avoids fitting the same location twice as one goes from parent
to child nodes.

n_simulate
==========
This integer is the number of rows in simulate.csv that will be randomly chosen
(without replacement) for this node. This value must be less than or equal
the number of rows (not counting the header) in the simulate.csv file.
For example, we could only simulate data for the leaf nodes by setting
n_simulate to zero for the other nodes.

-----------------------------------------------------------------------------

covariate.csv
*************
This csv file specifies the value of omega and the covariates.
It has a :ref:`simulate@rectangular_grid` in the columns
``node_id``, ``sex``, ``age``, ``time`` .

node_id
=======
This integer identifies the node corresponding to this row.

sex
===
This text is ``male`` or ``female`` and identifies which sex
this row corresponds to. When estimating for both sexes, the
average of the corresponding male and female data is used.

age
===
This real is the age, in years,  corresponding to this row.

time
====
This real is the time, in years, corresponding to this row.

omega
=====
This real is the value of omega (other cause mortality) for this row.
Often other cause mortality is approximated by all cause mortality.
Omega is a rate, not a covariate.

sex
===
This is ``male`` or ``female`` and is the sex for this simulated data.

covariate_name
==============
For each covariate that we are including in this simulation,
there is a column in the header that contains the *covariate_name*.
In the other rows, this column  contain a real that is the
corresponding covariate value.

-----------------------------------------------------------------------------

multiplier.csv
**************
This csv file provides information about the covariate multipliers.
Each row of this file, except the header row, corresponds to a
different multiplier (the multipliers are constant in age and time)

rate_name
=========
This text is ``iota``, ``rho``, ``chi``, or ``pini`` and specifies
which rate this covariate multiplier is affecting.

covariate_name
==============
This text is a covariate name and specifies which covariate
is being multiplied by this multiplier.
It can be ``sex`` or any of the covariate names in covariate.csv file.
Note that for sex, the corresponding covariate values are
female = -0.5 and male = +0.5.

truth
=====
This is the value of the covariate multiplier used to simulate the data.

mean
====
This is the prior mean used when fitting this multiplier
(normal distribution).

std
===
This is the prior standard deviation used when fitting this multiplier
(normal distribution).

lower
=====
is the lower limit (during fitting) for this covariate multiplier.

upper
=====
is the upper limit (during fitting) for this covariate multiplier.
Note that using lower and upper limit are zero and the true value is non-zero,
one can simulate data that does not correspond to the model.


-----------------------------------------------------------------------------

rate.csv
********
This csv file specifies the grid points at which each rate is modeled.
This file has a
:ref:`simulate@rectangular_grid` in the columns
``rate_name``, ``age``, ``time`` .
These are no-effect rates; i.e., the rates without
the random and covariate effects.
It is the same for all nodes.
Covariate multipliers that are constrained to zero during the fitting
can be used to get variation between nodes in the
no-effect rates corresponding to the fitting.

rate_name
=========
This text is ``iota``, ``rho``, ``chi``, or ``pini`` and specifies the rate.
If one of these rates doe not appear, it is modeled as always zero.

age
===
This real is the age, in years,  corresponding to this row.

time
====
This real is the time, in years, corresponding to this row.

truth
=====
This real is the rate value for the root node (the world)
with no covariate or random effects.
It is used to simulate the data.

mean
====
This real is the mean used in the prior for the rate
without covariate or random effects
(normal distribution).

std
===
This real is the standard deviation used in the prior for the rate
without covariate or random effects
(normal distribution).

lower
=====
is the lower limit (during fitting) for this covariate multiplier.

upper
=====
is the upper limit (during fitting) for this covariate multiplier.
Note that using lower and upper limit are zero and the true value is non-zero,
one can simulate data that does not correspond to the model.

-----------------------------------------------------------------------------

simulate.csv
************
This csv file specifies the simulated data set.
Subsets of the data set will be used when fitting the data.
For each node in :ref:`simulate_csv_in@node.csv@node_id`,
sex equal to male and female,
:ref:`simulate_csv_in@node.csv@n_simulate`
a rows of simulate.csv are randomly selected (without replacement).
A simulated data point is created for each such selection.
Each such simulate data point corresponds to a row in
:ref:`simulate_csv_out@data.csv`.

simulate_id
===========
For each row, the value in this column is the number of rows that come before
this row, not counting the header row.
In other words, it counts the data rows starting at row index zero.
This column is used to select subsets of the simulation corresponding
to each node and sex.


integrand_name
==============
This text is a dismod_at integrand; e.g. ``Sincidence``.

age_lower
=========
is the lower age limit for this data row.

age_upper
=========
is the upper age limit for this data row.
Note that the age midpoint will be used to interpolate covariates values
corresponding to this data row.

time_lower
==========
is the lower time limit for this data row.

time_upper
==========
is the upper time limit for this data row.

percent_cv
==========
is the coefficient of variation as a percent of the corresponding
average integrand; i.e., the model for the integrand
without any measurement noise.
The noise will be generated with a normal distribution
that has mean equal to the average integrand and
standard deviation equal to the mean times percent_cv / 100.
If the resulting measurement value would be less than zero,
the value zero is be used; i.e.,
a censored normal is used to simulate the data.


{xrst_end simulate_csv_in}

==============================================================================

{xrst_begin simulate_csv_out}
{xrst_spell
    csv
    meas
    std
    bilinear
}

simulate CSV Output Files
##########################

data.csv
********
This is the simulate data, it as the following columns

node_id
=======
This integer identifies the node for this data row by its node_id in node.csv.

integrand_name
==============
This text identifies the integrand for this simulated data.

meas_value
==========
This real is the simulated measured value

meas_std
========
This real is the measurement standard deviation for the simulated
data point. This standard deviation is before censoring.

age_lower
=========
is the lower age limit for this data row.

age_upper
=========
is the upper age limit for this data row.
Note that the age midpoint will be used to interpolate covariates values
corresponding to this data row.

time_lower
==========
is the lower time limit for this data row.

time_upper
==========
is the upper time limit for this data row.

sex
===
This is ``male`` or ``female`` and is the sex for this simulated data.

covariate_name
==============
For each covariate that we are including in this simulation,
there is a column in the header that contains the *covariate_name*.
In the other rows, this column  contain a real that is the
corresponding covariate value at the mid point of the ages and time
intervals for this data point. This value is obtained using
bilinear interpolation of the covariate values in covariate.csv.
The interpolate is extended as constant in age (time) for points
outside the age rage (time range) in the covariate.csv file.


{xrst_end simulate_csv_out}
"""
def simulate(
# BEGIN Syntax
# at_cascade.simulate(
    simulate_dir
# )
# END Syntax
) :
    assert type(simulate_dir) == str
    assert False