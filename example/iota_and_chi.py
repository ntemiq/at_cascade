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
{xsrst_begin_parent iota_and_chi}
{xsrst_spell
    avg
    dtime
    dage
    integrands
}

Example Estimation of iota and chi
##################################

Under Construction
******************
This example is not yet working.

Nodes
*****
The following is a diagram of the node tree for this example.
The :ref:`glossary.root_node` is n0,
the :ref:`glossary.fit_goal_set` and the leaf node set
are both {n3, n4, n5, n6} for this example::

                n0
          /-----/\-----\
        n1              n2
       /  \            /  \
    (n3)  (n4)      (n5)  (n6)

fit_goal_set
============
{xsrst_file
    # BEGIN fit_goal_set
    # END fit_goal_set
}

Rates
*****
The non-zero dismod_at rates for this example are
:ref:`glossary.iota`, :ref:`glossary.chi`, and :ref:`glossary.omega`.
We use *iota(a, n, I)* , *chi(a, n, I)*
to denote the value for *iota* and *chi*
as a function of age *a*, node number *n*, and income *I*.
We use *omega(a, n)* and *omega_n* to denote the value for *omega*
as a function of age *a* and node number *n*.


Covariate
*********
There are two covariates for this example is *income* and *one*.
The reference value for *income* is the average income corresponding
to the :ref:`glossary.fit_node`.
The *one* covariate is always equal to 1 and its reference is always zero.

r_n
===
We use *r_n* for the reference value of *income* at node *n*.
The code below sets this reference using the name avg_income:
{xsrst_file
    # BEGIN avg_income
    # END avg_income
}

alpha
=====
We use *alpha*
for the :ref:`glossary.rate_value` covariate multiplier
which multiplies *income*.
This multiplier affects the value of *iota*.
The true value for *alpha* (used which simulating the data) is
{xsrst_file
    # BEGIN alpha_true
    # END alpha_true
}

gamma
=====
We use *gamma_prevalence* ( *gamma_mtexcess* )
for the :ref:`glossary.meas_noise` covariate multiplier
which multiplies *one* add affects prevalence noise ( mtexcess noise) .
These multipliers adds to the nose level in log space,
because the corresponding densities are log Gaussian.


Random Effects
**************
For each node, there is a random effect on *iota* and *chi* that is constant
in age and time. Note that the leaf nodes have random effect for the node
above them as well as their own random effect.

s_n
===
We use *s_n* to denote the sum of the random effects for node *n*.
The code below sets this sum using the name sum_random:
{xsrst_file
    # BEGIN sum_random
    # END sum_random
}

Simulated Data
**************
For this example everything is constant in time so the
functions below do not depend on time.

Random Seed
===========
The random seed can be used to reproduce results.
If the original value of this setting is zero, the clock is used get
a random seed. The actual value or *random_seed* is always printed.
{xsrst_file
    # BEGIN random_seed
    # END random_seed
}

rate_true(rate, a, n, I)
========================
For *rate* equal to iota, chi, and omega,
this is the true value for *rate* in node *n* at age *a* and income *I*:
{xsrst_file
    # BEGIN rate_true
    # END rate_true
}


y_i
===
The simulated integrands for this example are
:ref:`glossary.prevalence` and :ref:`glossary.mtspecific`.
The data is simulated without any noise
but it is modeled as having noise.

n_i
===
Data is only simulated for the leaf nodes; i.e.,
each *n_i* is in the set { n3, n4, n5, n6 }.
Since the data does not have any nose, the data residuals are a measure
of how good the fit is for the goal nodes.

a_i
===
For each leaf node, data is generated on the following *age_grid*:
{xsrst_file
    # BEGIN age_grid
    # END age_grid
}

I_i
===
For each leaf node and each age in *age_grid*,
data is generated for the following *income_grid*:
{xsrst_file
    # BEGIN income_grid
    # END income_grid
}
Note that the check of the fit for the goal nodes expects much more accuracy
when the income grid is not chosen randomly.

Parent Smoothing
****************

omega
=====
The parent smoothing constrains *omega* to be equal to
*rate_true(omega, a, n, I)* where  *a* is each value in the age grid and
*n* is the current node and *I* is he reference income for that node *r_n*.

iota and chi
============
This is the smoothing used in the *fit_node* model for the rates.
Note that the value part of this smoothing is only used for the *root_node*.
This smoothing uses the *age_gird* and one time point.
There are no dtime priors because there is only one time point.

Value Prior
-----------
The *fit_node* value prior is uniform with lower limit
equal to the true rate for the root node at age zero divided by 10.
The upper limit is the true rate at age 100 time 10
and the mean is the true rate at age 50.
The mean is only used to initialize the optimization.

Dage Prior
-----------
The prior for age differences is log Gaussian with mean zero,
standard deviation 1.0, and :ref:`glossary.eta` equal to
the minimum of the true *chi* and *iota* at age 50 times 1e-3.

Child Smoothing
***************

omega
=====
The child smoothing constrains *omega* to be equal to
*rate_true(omega, a, n, I)* where  *a* is each value in the age grid,
*n* is the child node, and *I* is the reference income for the child node.

iota and chi
============
The same smoothing used is used for the *iota* and *chi*
random effect for each child of the *fit_node*.
The smoothing only has one age and one time point; i.e.,
the corresponding function is constant in age and time.
There are no dage or dtime priors because there is only one
age and one time point.

Value Prior
-----------
This value prior is gaussian with mean zero and standard deviation 1.0.
There are no upper or lower limits in this prior.

Alpha Smoothing
***************
This is the smoothing used in the model for *alpha*.
There are no dage or dtime priors because there is only one
age and one time point in this smoothing.

Value Prior
===========
This value prior is uniform with lower limit *-10\*|alpha_true|*,
upper limit *+10\*|alpha_true|* and mean zero.
(The mean is used to initialize the optimization.)

Checking The Fit
****************
The results of the fit are in the
:ref:`cascade_fit_node.dismod_db.predict` and
:ref:`cascade_fit_node.dismod_db.c_predict_fit_var`
tables of the fit_node_database corresponding to each node.
The ``check_fit`` routine uses these tables to check that fit
against the truth.

{xsrst_end iota_and_chi}
------------------------------------------------------------------------------
{xsrst_begin iota_and_chi_py}

iota_and_chi: Python Source Code
#################################

{xsrst_file
    BEGIN iota_and_chi source code
    END iota_and_chi source code
}

{xsrst_end iota_and_chi_py}
'''
# BEGIN iota_and_chi source code
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import sys
import os
import copy
import time
import csv
import random
import numpy
import shutil
import distutils.dir_util
import dismod_at
import math
#
# import at_cascade with a preference current directory version
current_directory = os.getcwd()
if os.path.isfile( current_directory + '/at_cascade/__init__.py' ) :
    sys.path.insert(0, current_directory)
import at_cascade
# -----------------------------------------------------------------------------
# global variables
# -----------------------------------------------------------------------------
# BEGIN fit_goal_set
fit_goal_set = { 'n3', 'n4', 'n5', 'n6' }
# END fit_goal_set
#
# BEGIN random_seed
# random_seed = 1629371067
random_seed = 0
if random_seed == 0 :
    random_seed = int( time.time() )
    random.seed(random_seed)
print('iota_and_chi: random_seed = ', random_seed)
# END random_seed
#
# BEGIN alpha_true
alpha_true = - 0.2
# END alpha_true
#
# BEGIN avg_income
avg_income       = { 'n3':1.0, 'n4':2.0, 'n5':3.0, 'n6':4.0 }
avg_income['n2'] = ( avg_income['n5'] + avg_income['n6'] ) / 2.0
avg_income['n1'] = ( avg_income['n3'] + avg_income['n4'] ) / 2.0
avg_income['n0'] = ( avg_income['n1'] + avg_income['n2'] ) / 2.0
# END avg_income
#
# BEGIN sum_random_effect
size_level1      = 0.2
size_level2      = 0.2
sum_random       = { 'n0': 0.0, 'n1': size_level1, 'n2': -size_level1 }
sum_random['n3'] = sum_random['n1'] + size_level2;
sum_random['n4'] = sum_random['n1'] - size_level2;
sum_random['n5'] = sum_random['n2'] + size_level2;
sum_random['n6'] = sum_random['n2'] - size_level2;
# END sum_random_effect
#
# BEGIN age_grid
age_grid = [0.0, 20.0, 40.0, 60.0, 80.0, 100.0 ]
# END age_grid
#
# BEGIN income_grid
random_income = False
income_grid   = dict()
for node in [ 'n3', 'n4', 'n5', 'n6' ] :
    max_income  = 2.0 * avg_income[node]
    if random_income :
        n_income_grid = 10
        income_grid[node] = \
            [ random.uniform(0.0, max_income) for j in range(n_income_grid) ]
        income_grid[node] = sorted( income_grid[node] )
    else :
        n_income_grid = 3
        d_income_grid = max_income / (n_income_grid - 1)
        income_grid[node] = [ j * d_income_grid for j in range(n_income_grid) ]
# END income_grid
# ----------------------------------------------------------------------------
# functions
# ----------------------------------------------------------------------------
# BEGIN rate_true
def rate_true(rate, a, n, I ) :
    s_n           = sum_random[n]
    r_0           = avg_income['n0']
    income_effect = alpha_true * ( I - r_0 )
    # The true random effect for iota and chi is the same
    if rate == 'iota' :
        return (1 + a / 100) * 1e-4 * math.exp( s_n + income_effect  )
    if rate == 'chi' :
        return (1 + a / 100) * 1e-1 * math.exp( s_n + income_effect )
    if rate == 'omega' :
        return (1 + a / 100) * 1e-2 * math.exp( income_effect )
    assert False
# END rate_true
# ----------------------------------------------------------------------------
def average_integrand(integrand_name, age, node_name, income) :
    def iota(a, t) :
        return rate_true('iota', a, node_name, income)
    def chi(a, t) :
        return rate_true('chi', a, node_name, income)
    def omega(a, t) :
        return rate_true('omega', a, node_name, income)
    rate           = { 'iota': iota,  'chi': chi, 'omega': omega }
    grid           = { 'age' : [age], 'time': [2000.0] }
    abs_tol        = 1e-6
    avg_integrand   = dismod_at.average_integrand(
        rate, integrand_name, grid,  abs_tol
    )
    return avg_integrand
# ----------------------------------------------------------------------------
def root_node_db(file_name) :
    #
    # prior_table
    iota_50 = rate_true('iota', 50.0, 'n0', avg_income['n0'])
    chi_50  = rate_true('chi',  50.0, 'n0', avg_income['n0'])
    prior_table = [
        {   # prior_iota_n0_value
            'name':    'prior_iota_n0_value',
            'density': 'gaussian',
            'lower':   iota_50 / 10.0,
            'upper':   iota_50 * 10.0,
            'mean':    iota_50,
            'std' :    iota_50 * 10.0,
            'eta':     iota_50 * 1e-3,
        },{ # prior_chi_n0_value
            'name':    'prior_chi_n0_value',
            'density': 'gaussian',
            'lower':   chi_50 / 10.0,
            'upper':   chi_50 * 10.0,
            'mean':    chi_50,
            'std':     chi_50 * 10.0,
            'eta':     chi_50 * 1e-3,
        },{ # prior_child_dage
            'name':    'prior_child_dage',
            'density': 'log_gaussian',
            'mean':    0.0,
            'std':     4.0,
            'eta':     min(iota_50 , chi_50 ) * 1e-3,
        },{ # prior_child_value
            'name':    'prior_child_value',
            'density': 'gaussian',
            'mean':    0.0,
            'std':     1.0,
        },{ # prior_alpha_n0_value
            'name':    'prior_alpha_n0_value',
            'density': 'gaussian',
            'lower':   - 10 * abs(alpha_true),
            'upper':   + 10 * abs(alpha_true),
            'mean':    0.0,
            'std':     + 10 * abs(alpha_true),
        },
    ]
    #
    # smooth_table
    smooth_table = list()
    #
    # smooth_iota_n0
    fun = lambda a, t : ('prior_iota_n0_value', 'prior_child_dage', None)
    smooth_table.append({
        'name':       'smooth_iota_n0',
        'age_id':     range( len(age_grid) ),
        'time_id':    [0],
        'fun':        fun,
    })
    #
    # smooth_chi_n0
    fun = lambda a, t : ('prior_chi_n0_value', 'prior_child_dage', None)
    smooth_table.append({
        'name':       'smooth_chi_n0',
        'age_id':     range( len(age_grid) ),
        'time_id':    [0],
        'fun':        fun,
    })
    #
    # smooth_child
    fun = lambda a, t : ('prior_child_value', None, None)
    smooth_table.append({
        'name':       'smooth_child',
        'age_id':     [0],
        'time_id':    [0],
        'fun':        fun,
    })
    #
    # smooth_alpha_n0
    fun = lambda a, t : ('prior_alpha_n0_value', None, None)
    smooth_table.append({
        'name':       'smooth_alpha_n0',
        'age_id':     [0],
        'time_id':    [0],
        'fun':        fun,
    })
    #
    # smooth_gamma
    # constant gamma = 1.0
    fun = lambda a, t : (1.0, None, None)
    smooth_table.append({
        'name':       'smooth_gamma',
        'age_id':     [0],
        'time_id':    [0],
        'fun':        fun
    })
    #
    # node_table
    node_table = [
        { 'name':'n0',        'parent':''   },
        { 'name':'n1',        'parent':'n0' },
        { 'name':'n2',        'parent':'n0' },
        { 'name':'n3',        'parent':'n1' },
        { 'name':'n4',        'parent':'n1' },
        { 'name':'n5',        'parent':'n2' },
        { 'name':'n6',        'parent':'n2' },
    ]
    #
    # rate_table
    rate_table = [ {
            'name':           'iota',
            'parent_smooth':  'smooth_iota_n0',
            'child_smooth':   'smooth_child' ,
        },{
            'name':           'chi',
            'parent_smooth':  'smooth_chi_n0',
            'child_smooth':   'smooth_child' ,
    } ]
    #
    # covariate_table
    covariate_table = [
        { 'name':'income',   'reference':avg_income['n0'] },
        { 'name':'one',      'reference':0.0              },
    ]
    #
    # mulcov_table
    mulcov_table = [
        {   # alpha
            'covariate':  'income',
            'type':       'rate_value',
            'effected':   'iota',
            'group':      'world',
            'smooth':     'smooth_alpha_n0',
        },{ # gamma_Sincidence
            'covariate':  'one',
            'type':       'meas_noise',
            'effected':   'Sincidence',
            'group':      'world',
            'smooth':     'smooth_gamma',
        },{ # gamma_mtexcess
            'covariate':  'one',
            'type':       'meas_noise',
            'effected':   'mtexcess',
            'group':      'world',
            'smooth':     'smooth_gamma',
    } ]
    #
    # subgroup_table
    subgroup_table = [ {'subgroup': 'world', 'group':'world'} ]
    #
    # integrand_table
    integrand_table = [
        {'name': 'Sincidence'},
        {'name': 'mtexcess' },
        {'name': 'prevalence'},
        {'name': 'mtspecific'},
        {'name': 'mulcov_0'},
        {'name': 'mulcov_1'},
        {'name': 'mulcov_2'},
    ]
    #
    # avgint_table
    avgint_table = list()
    row = {
        'node':         'n0',
        'subgroup':     'world',
        'weight':       '',
        'time_lower':   2000.0,
        'time_upper':   2000.0,
        'income':       None,
        'one':          1.0,
    }
    for age in age_grid :
        row['age_lower'] = age
        row['age_upper'] = age
        for integrand in [ 'Sincidence', 'mtexcess' ] :
            row['integrand'] = integrand
            avgint_table.append( copy.copy(row) )
    #
    # data_table
    data_table = list()
    leaf_set   = [ 'n3', 'n4', 'n5', 'n6' ]
    for node in leaf_set :
        row = {
            'subgroup':     'world',
            'weight':       '',
            'time_lower':   2000.0,
            'time_upper':   2000.0,
            'density':      'log_gaussian',
            'hold_out':     False,
            'one':          1.0,
        }
        row_list       = list()
        max_meas_value =  {
            'mtexcess': 0.0, 'Sincidence': 0.0
        }
        for (age_id, age) in enumerate( age_grid ) :
            for income in income_grid[node] :
                row['node']       = node
                row['age_lower']  = age
                row['age_upper']  = age
                row['income']     = income
                for integrand in max_meas_value :
                    meas_value = average_integrand(
                        integrand, age, node, income
                    )
                    row['integrand']  = integrand
                    row['meas_value'] = meas_value
                    max_meas_value[integrand]  = max(
                        meas_value, max_meas_value[integrand]
                    )
                    row_list.append( copy.copy(row) )
        n_row = len(age_grid) * n_income_grid * len(max_meas_value)
        assert len(row_list) == n_row
        for row in row_list :
            # The model for the measurement noise is small so a few
            # data points act like lots of real data points.
            # The actual measruement noise is zero.
            for integrand in max_meas_value :
                if row['integrand'] == integrand :
                    row['meas_std'] = max_meas_value[integrand] / 50.0
                    row['eta']      = 1e-4 * max_meas_value[integrand]
        #
        data_table += row_list
    #
    # time_grid
    time_grid = [ 2000.0 ]
    #
    # weight table:
    weight_table = list()
    #
    # nslist_table
    nslist_table = dict()
    #
    # option_table
    option_table = [
        { 'name':'parent_node_name',      'value':'n0'},
        { 'name':'rate_case',             'value':'iota_pos_rho_zero'},
        { 'name': 'zero_sum_child_rate',  'value':'iota chi'},
        { 'name':'quasi_fixed',           'value':'false'},
        { 'name':'print_level_fixed',     'value':'5'},
        { 'name':'max_num_iter_fixed',    'value':'50'},
        { 'name':'max_num_iter_random',   'value':'200'},
        { 'name':'tolerance_fixed',       'value':'1e-8'},
        { 'name':'tolerance_random',      'value':'1e-8'},
        { 'name':'bound_random',          'value':1.0},
        { 'name':'meas_noise_effect',     'value':'add_std_scale_none'},
        { 'name':'random_seed',           'value':str(random_seed)},
    ]
    # ----------------------------------------------------------------------
    # create database
    dismod_at.create_database(
        file_name,
        age_grid,
        time_grid,
        integrand_table,
        node_table,
        subgroup_table,
        weight_table,
        covariate_table,
        avgint_table,
        data_table,
        prior_table,
        smooth_table,
        nslist_table,
        rate_table,
        mulcov_table,
        option_table
    )
# ----------------------------------------------------------------------------
def check_fit(goal_database) :
    #
    # connection
    new        = False
    connection = dismod_at.create_connection(goal_database, new)
    #
    # goal_name
    path_list = goal_database.split('/')
    assert len(path_list) >= 2
    assert path_list[-1] == 'dismod.db'
    goal_name = path_list[-2]
    #
    # table
    table = dict()
    for name in [
        'avgint',
        'age',
        'integrand',
        'node',
        'predict',
        'c_predict_fit_var',
    ] :
        table[name] = dismod_at.get_table_dict(connection, name)
    #
    n_avgint  = len(table['avgint'])
    n_predict = len(table['predict'])
    n_sample  = int( n_predict / n_avgint )
    #
    assert n_avgint == len( table['c_predict_fit_var'] )
    assert n_predict % n_avgint == 0
    #
    # sumsq
    sumsq = n_avgint * [0.0]
    for (predict_id, predict_row) in enumerate( table['predict'] ) :
        # avgint_row
        avgint_id  = predict_row['avgint_id']
        avgint_row = table['avgint'][avgint_id]
        assert avgint_id == predict_id % n_avgint
        #
        # sample_index
        sample_index = predict_row['sample_index']
        assert sample_index * n_avgint + avgint_id == predict_id
        #
        # integrand_name
        integrand_id = avgint_row['integrand_id']
        integrand_name = table['integrand'][integrand_id]['integrand_name']
        assert integrand_name in ['Sincidence', 'mtexcess']
        #
        # node_name
        node_id   = avgint_row['node_id']
        node_name = table['node'][node_id]['node_name']
        assert node_name == goal_name
        #
        # age
        age = avgint_row['age_lower']
        assert age == avgint_row['age_upper']
        #
        # avg_integrand
        avg_integrand = table['c_predict_fit_var'][avgint_id]['avg_integrand']
        #
        # sample_value
        sample_value = predict_row['avg_integrand']
        #
        # sumsq
        sumsq[avgint_id] += (sample_value - avg_integrand)**2
    #
    # income
    income  = avg_income[goal_name]
    #
    # (avgint_id, row)
    for (avgint_id, row) in enumerate(table['c_predict_fit_var']) :
        assert avgint_id == row['avgint_id']
        #
        # avgint_row
        avgint_row = table['avgint'][avgint_id]
        #
        # age
        age = avgint_row['age_lower']
        #
        # avg_integrand
        avg_integrand = row['avg_integrand']
        #
        # sample_std
        sample_std = math.sqrt( sumsq[avgint_id] )
        #
        # integrand_name
        integrand_id = avgint_row['integrand_id']
        integrand_name = table['integrand'][integrand_id]['integrand_name']
        #
        # check_value
        if integrand_name == 'Sincidence' :
            rate        = 'iota'
        else :
            assert integrand_name == 'mtexcess'
            rate        = 'chi'
        #
        check_value = rate_true(rate, age, goal_name, income)
        rel_error   = 1.0 - avg_integrand / check_value
        #
        # check the fit
        print(rate, age, rel_error, check_value - avg_integrand, sample_std)
        # assert abs(rel_error) < 1e-1
        # assert abs(avg_integrand - check_value) < 2.0 * sample_std
# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------
def main() :
    # -------------------------------------------------------------------------
    # wrok_dir
    work_dir = 'build/example'
    distutils.dir_util.mkpath(work_dir)
    os.chdir(work_dir)
    #
    # Create root_node.db
    root_node_database  = 'root_node.db'
    root_node_db(root_node_database)
    #
    # all_cov_reference
    all_cov_reference = dict()
    for node_name in [ 'n0', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6' ] :
        all_cov_reference[node_name] = {
            'income' : avg_income[node_name],
            'one':     1.0,
        }
    #
    # omega_grid
    omega_grid = dict()
    omega_grid['age']  = range( len(age_grid) )
    omega_grid['time'] = [ 0 ]
    #
    # mtall_data
    integrand_name = 'mtall'
    mtall_data     = dict()
    for node_name in [ 'n0', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6' ] :
        mtall_data[node_name] = list()
        income                = avg_income[node_name]
        for age_id in omega_grid['age'] :
            age  = age_grid[age_id]
            time = 2000.0
            mtall = average_integrand(integrand_name, age, node_name, income)
            mtall_data[node_name].append(mtall)
    #
    # mtspecific_data
    integrand_name  = 'mtspecific'
    mtspecific_data = dict()
    for node_name in [ 'n0', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6' ] :
        mtspecific_data[node_name] = list()
        income   = avg_income[node_name]
        for age_id in omega_grid['age'] :
            age  = age_grid[age_id]
            time = 2000.0
            mtspecific = \
                average_integrand(integrand_name, age, node_name, income)
            mtspecific_data[node_name].append(mtspecific)
    #
    #
    # Create all_node.db
    # We could get all_cov_reference from here, but we do not need to
    all_node_database = 'all_node.db'
    at_cascade.create_all_node_db(
        all_node_database   = all_node_database   ,
        root_node_database  = root_node_database  ,
        all_cov_reference   = all_cov_reference ,
        omega_grid          = omega_grid,
        mtall_data          = mtall_data,
        mtspecific_data     = mtspecific_data,
        fit_goal_set        = fit_goal_set,
    )
    #
    # node_table
    new        = False
    connection = dismod_at.create_connection(root_node_database, new)
    node_table = dismod_at.get_table_dict(connection, 'node')
    connection.close()
    #
    # fit_node_dir
    fit_node_dir = 'n0'
    if os.path.exists(fit_node_dir) :
        # rmtree is very dangerous so make sure fit_node_dir is as expected
        os.chdir('../..')
        assert work_dir == 'build/example'
        shutil.rmtree(work_dir + '/' + fit_node_dir)
        os.chdir(work_dir)
    os.makedirs(fit_node_dir )
    #
    # fit_node_database = root_node_database
    fit_node_database =  fit_node_dir + '/dismod.db'
    shutil.copyfile(root_node_database, fit_node_database)
    #
    # cascade starting at root node
    at_cascade.cascade_fit_node(
        all_node_database, fit_node_database, node_table
    )
    #
    # check results
    for goal_dir in [ 'n0/n1', 'n0/n2/n5', 'n0/n2/n6' ] :
        goal_database = goal_dir + '/dismod.db'
        check_fit(goal_database)
    #
    # check that fits were not run for n3 and n4
    for not_fit_dir in [ ] :
        assert not os.path.exists( not_fit_dir )

#
main()
print('iota_and_chi: OK')
sys.exit(0)
ncvome
# END iota_and_chi source code