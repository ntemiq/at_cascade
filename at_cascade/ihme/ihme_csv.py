# -----------------------------------------------------------------------------
# at_cascade: Cascading Dismod_at Analysis From Parent To Child Regions
#           Copyright (C) 2021-22 University of Washington
#              (Bradley M. Bell bradbell@uw.edu)
#
# This program is distributed under the terms of the
#     GNU Affero General Public License version 3.0 or later
# see http://www.gnu.org/licenses/agpl.txt
# ------------------------------------------------------------------------------
import os
import multiprocessing
import numpy
import dismod_at
import at_cascade.ihme
# -----------------------------------------------------------------------------
def ihme_csv_one_job(
    fit_node_database ,
    age_group_id_dict ,
    age_group_id_list ,
    one_age_group_dict ,
    interpolate_all_covariate ,
    max_plot ,
) :
    assert type(fit_node_database) == str
    assert type(age_group_id_dict) == dict
    assert type(age_group_id_list) == list
    assert type(one_age_group_dict) == dict
    assert type(interpolate_all_covariate) == dict
    assert type(max_plot) == int
    assert one_age_group_dict.keys() == interpolate_all_covariate.keys()
    #
    # all_node_database
    all_node_database = at_cascade.ihme.all_node_database
    #
    # integrand_name2measure_id
    integrand_name2measure_id = at_cascade.ihme.integrand_name2measure_id
    #
    # integrand_table, age_table, time_table
    new        = False
    connection      = dismod_at.create_connection(fit_node_database, new)
    integrand_table = dismod_at.get_table_dict(connection, 'integrand')
    age_table       = dismod_at.get_table_dict(connection, 'age')
    time_table      = dismod_at.get_table_dict(connection, 'time')
    covariate_table = dismod_at.get_table_dict(connection, 'covariate')
    connection.close()
    #
    # all_option_table, split_reference_table
    new               = False
    connection        = dismod_at.create_connection(all_node_database, new)
    all_option_table  = dismod_at.get_table_dict(connection, 'all_option')
    split_reference_table = \
        dismod_at.get_table_dict(connection, 'split_reference')
    connection.close()
    #
    # result_dir
    result_dir = None
    for row in all_option_table :
        if row['option_name'] == 'result_dir' :
            result_dir = row['option_value']
    assert result_dir is not None
    #
    # node_table
    # Note that this node table has map to location_id
    file_name  = at_cascade.ihme.csv_file['node']
    file_path  = f'{result_dir}/{file_name}'
    node_table = at_cascade.ihme.get_table_csv(file_path)
    #
    # fit_node_dir
    assert fit_node_database.endswith('/dismod.db')
    index        = fit_node_database.rfind('/')
    fit_node_dir = fit_node_database[0:index]
    #
    # fit_split_reference_id
    cov_info = at_cascade.get_cov_info(
        all_option_table, covariate_table, split_reference_table
    )
    fit_split_reference_id  = cov_info['split_reference_id']
    #
    # integrand_id_list
    integrand_id_list = list()
    for integrand_name in integrand_name2measure_id :
        integrand_id = at_cascade.table_name2id(
            integrand_table, 'integrand', integrand_name
        )
        integrand_id_list.append( integrand_id )
    #
    # year_grid
    # year_id in output file is in demographer notation
    year_grid = [ 1990.5, 1995.5, 2000.5, 2005.5, 2010.5, 2015.5, 2019.5 ]
    #
    # fit_node_name
    fit_node_name   = at_cascade.get_parent_node(fit_node_database)
    #
    # fit_node_id, location_id
    fit_node_id = None
    location_id = None
    for row in node_table :
        if row['node_name'] == fit_node_name :
            location_id = int( row['location_id'] )
            fit_node_id = int( row['node_id'] )
    index = fit_node_name.find('_')
    assert location_id == int( fit_node_name[0:index] )
    #
    # avgint_table
    avgint_table = list()
    #
    # sex, sex_name, sex_id
    row      = split_reference_table[fit_split_reference_id]
    sex      = row['split_reference_value']
    sex_name = row['split_reference_name']
    sex_id   = at_cascade.ihme.sex_info_dict[sex_name]['sex_id']
    #
    # list_str_x
    list_str_x = list()
    for j in range( len(covariate_table) ) :
        str_x = f'x_{j}'
        list_str_x.append( str_x )
    #
    #
    # age_index
    for age_index in range( len(age_group_id_list) ) :
        #
        # age_group_id
        age_group_id = age_group_id_list[age_index]
        #
        # age_lower, age_upper, age
        age_lower = age_group_id_dict[age_group_id]['age_lower']
        age_upper = age_group_id_dict[age_group_id]['age_upper']
        age       = (age_lower + age_upper) / 2.0
        #
        # time
        for time in year_grid :
            #
            # x
            x = list()
            for j in range( len(covariate_table) ) :
                #
                # covariate_name
                covariate_name = covariate_table[j]['covariate_name']
                #
                # value
                if covariate_name == 'one' :
                    value = 1.0
                elif covariate_name == 'sex' :
                    value = sex
                else :
                    # this is a relative covariate so interpolate its value
                    #
                    # covariate_by_sex
                    covariate_by_sex = \
                        interpolate_all_covariate[covariate_name][location_id]
                    #
                    if sex_name in covariate_by_sex  :
                        fun = covariate_by_sex[sex_name]
                        if one_age_group_dict[covariate_name] :
                            value = fun(time)
                        else :
                            value = fun(age, time, grid = False)
                    elif 'Both' in covariate_by_sex :
                        fun = covariate_by_sex['Both']
                        if one_age_group_dict[covariate_name] :
                            value = fun(time)
                        else :
                            value = fun(age, time, grid = False)
                    else :
                        # average Male and Female values to get value for Both
                        assert sex_name == 'Both'
                        assert 'Male' in covariate_by_sex
                        assert 'Female' in covariate_by_sex
                        #
                        # val_male
                        fun = covariate_by_sex['Male']
                        if one_age_group_dict[covariate_name] :
                            val_male = fun(time)
                        else :
                            val_male = fun(age, time, grid = False)
                        #
                        # val_female
                        fun = covariate_by_sex['Female']
                        if one_age_group_dict[covariate_name] :
                            val_female = fun(time)
                        else :
                            val_female = fun(age, time, grid = False)
                        #
                        # value
                        value = (val_male + val_female) / 2.0
                # x
                x.append(value)
            #
            for integrand_id in integrand_id_list :
                #
                # row
                # Covariates are in same order as covariate_table in the
                # create_root_node_database routine above.
                row = {
                    'integrand_id'    : integrand_id,
                    'node_id'         : fit_node_id,
                    'subgroup_id'     : 0,
                    'weight_id'       : None,
                    'age_lower'       : age_lower,
                    'age_upper'       : age_upper,
                    'time_lower'      : time,
                    'time_upper'      : time,
                    'c_age_group_id'  : age_group_id,
                }
                for j in range( len(x) ) :
                    row[ list_str_x[j] ] = x[j]
                avgint_table.append( row )
    #
    # avgint_table
    new        = False
    connection = dismod_at.create_connection(fit_node_database, new)
    dismod_at.replace_table(connection, 'avgint', avgint_table)
    connection.close()
    #
    # predict sample
    # print( 'sample' )
    command = [ 'dismod_at', fit_node_database, 'predict', 'sample' ]
    dismod_at.system_command_prc(command, print_command = False )
    #
    # db2csv
    # print( 'db2csv' )
    dismod_at.db2csv_command(fit_node_database)
    #
    # rate.pdf
    # print( 'rate.pdf' )
    pdf_file = f'{fit_node_dir}/rate.pdf'
    plot_title = f'{fit_node_name}.{sex_name}'
    rate_set   = { 'iota', 'chi', 'omega' }
    dismod_at.plot_rate_fit(
        fit_node_database, pdf_file, plot_title, rate_set
    )
    #
    # data.pdf
    # print( 'data.pdf' )
    pdf_file = f'{fit_node_dir}/data.pdf'
    plot_title = f'{fit_node_name}.{sex_name}'
    dismod_at.plot_data_fit(
        database   = fit_node_database,
        pdf_file   = pdf_file,
        plot_title = plot_title,
        max_plot   = max_plot,
    )
    #
    # predict_table
    new           = False
    connection    = dismod_at.create_connection(fit_node_database, new)
    predict_table = dismod_at.get_table_dict(connection, 'predict')
    connection.close()
    #
    # n_sample
    assert len(predict_table) % len(avgint_table) == 0
    n_sample = int( len(predict_table) / len(avgint_table) )
    #
    # n_avgint
    n_avgint = len( avgint_table )
    #
    # output_table
    output_table = list()
    #
    # plot_data
    plot_data = dict()
    #
    # avgint_row
    for (avgint_id, avgint_row) in enumerate( avgint_table ) :
        #
        # measure_id
        integrand_id    = avgint_row['integrand_id']
        integrand_name  = integrand_table[integrand_id]['integrand_name']
        measure_id      = integrand_name2measure_id[integrand_name]
        #
        # x
        x = list()
        for j in range( len(covariate_table) ) :
            x.append( avgint_row[ list_str_x[j] ] )
        #
        # plot_data[integrand_name]
        if integrand_name not in plot_data :
            plot_data[integrand_name] = list()
        #
        # age_group_id
        age_group_id  = avgint_row['c_age_group_id']
        #
        # year_id
        # convert from real to demographer notaiton by dropping .5
        assert avgint_row['time_lower'] == avgint_row['time_upper']
        year_id = int( avgint_row['time_lower'] )
        #
        # avg_integrand_list
        avg_integrand_list = list()
        #
        # sample_index
        for sample_index in range( n_sample ) :
            #
            # predict_row
            predict_id = sample_index * n_avgint + avgint_id
            predict_row = predict_table[predict_id]
            #
            # some checks
            assert sample_index  == predict_row['sample_index']
            assert avgint_id     == predict_row['avgint_id']
            #
            # avg_integrand
            avg_integrand = predict_row['avg_integrand']
            avg_integrand_list.append( avg_integrand )
        #
        # row
        row = {
            'location_id'    : location_id,
            'sex_id'         : sex_id,
            'age_group_id'   : age_group_id,
            'year_id'        : year_id,
            'measure_id'     : measure_id,
        }
        for j in range( len(covariate_table) ) :
            covariate_name        = covariate_table[j]['covariate_name']
            row[ covariate_name ] = x[j]
        for sample_index in range( n_sample ) :
            key = f'draw_{sample_index}'
            row[key] = avg_integrand_list[sample_index]
        #
        # output_table
        output_table.append(row)
        #
        # row
        mean      = numpy.mean( avg_integrand_list )
        std       = numpy.std( avg_integrand_list, ddof = 1 )
        age_lower = age_group_id_dict[age_group_id]['age_lower']
        age_upper = age_group_id_dict[age_group_id]['age_upper']
        age       = (age_lower + age_upper) / 2.0
        time      = avgint_row['time_lower']
        row = {
            'age'   : age,
            'time'  : time,
            'value' : mean,
            'std'   : std,
        }
        #
        # plot_data[integrand_name]
        plot_data[integrand_name].append( row )
    #
    # z_name
    z_list = list( plot_data.keys() )
    for z_name in z_list :
        #
        # max_std, max_value
        max_std   = 0.0
        max_value = 0.0
        for row in plot_data[z_name] :
            max_value = max(max_value, row['std'])
            max_std   = max(max_std, row['std'])
        #
        if max_value == 0.0 :
            # remove both plots for this integrand
            del plot_data[z_name]
        #
        elif max_std == 0.0 :
            # remove std plot for this integrand
            for row in plot_data[z_name] :
                del row['std']
    #
    # ihme.csv
    # print('ihme.csv')
    output_csv = f'{fit_node_dir}/ihme.csv'
    at_cascade.ihme.write_csv(output_csv, output_table)
    #
    # plot_limit
    age_min = min(  [ row['age']  for row in age_table  ] )
    age_max = max(  [ row['age']  for row in age_table  ] )
    time_min = min( [ row['time'] for row in time_table ] )
    time_max = max( [ row['time'] for row in time_table ] )
    plot_limit = {
        'age_min'  : age_min,
        'age_max'  : age_max,
        'time_min' : time_min,
        'time_max' : time_max,
    }
    #
    # ihme.pdf
    # print( 'ihme.pdf' )
    pdf_file = f'{fit_node_dir}/ihme.pdf'
    plot_title = f'{fit_node_name}.{sex_name}'
    dismod_at.plot_curve(
        pdf_file   = pdf_file      ,
        plot_limit = plot_limit      ,
        plot_title = plot_title      ,
        plot_data  = plot_data       ,
    )
# -----------------------------------------------------------------------------
def ihme_csv(
    covariate_csv_file_dict, fit_goal_set, root_node_database, max_plot
) :
    #
    # all_node_database
    all_node_database = at_cascade.ihme.all_node_database
    #
    #
    # node_table, covariate_table
    new        = False
    connection      = dismod_at.create_connection(root_node_database, new)
    node_table      = dismod_at.get_table_dict(connection, 'node')
    covariate_table = dismod_at.get_table_dict(connection, 'covariate')
    connection.close()
    #
    # all_option_table, split_reference_table, node_split
    new              = False
    connection       = dismod_at.create_connection(all_node_database, new)
    all_option_table =  dismod_at.get_table_dict(connection, 'all_option')
    node_split_table =  dismod_at.get_table_dict(connection, 'node_split')
    split_reference_table = \
        dismod_at.get_table_dict(connection, 'split_reference')
    connection.close()
    #
    # result_dir
    result_dir = None
    for row in all_option_table :
        if row['option_name'] == 'result_dir' :
            result_dir = row['option_value']
    assert result_dir is not None
    #
    # node_split_set
    node_split_set = set()
    for row in node_split_table :
        node_split_set.add( row['node_id'] )
    #
    # root_node_id
    root_node_name = at_cascade.get_parent_node(root_node_database)
    root_node_id   = at_cascade.table_name2id(
            node_table, 'node', root_node_name
    )
    #
    # root_split_reference_id
    if len(split_reference_table) == 0 :
        root_split_refernence_id = None
    else :
        cov_info = at_cascade.get_cov_info(
            all_option_table      = all_option_table ,
            covariate_table       = covariate_table ,
            split_reference_table = split_reference_table,
        )
        root_split_reference_id = cov_info['split_reference_id']
    #
    # job_table
    job_table = at_cascade.create_job_table(
        all_node_database          = all_node_database       ,
        node_table                 = node_table              ,
        start_node_id              = root_node_id            ,
        start_split_reference_id   = root_split_reference_id ,
        fit_goal_set               = fit_goal_set            ,
    )
    #
    # age_group_id_dict, age_group_id_list
    age_group_id_table = at_cascade.ihme.get_age_group_id_table()
    age_group_id_dict   = dict()
    age_group_id_list   = list()
    for row in age_group_id_table :
        age_group_id = row['age_group_id']
        age_group_id_dict[age_group_id] = row
        age_group_id_list.append( age_group_id )
    #
    # one_age_group_dict, interpolate_all_covariate
    one_age_group_dict        = dict()
    interpolate_all_covariate = dict()
    covariate_list             = covariate_csv_file_dict.keys()
    for covariate_name in covariate_list :
        covariate_file_path = covariate_csv_file_dict[covariate_name]
        (one_age_group, interpolate_covariate) = \
            at_cascade.ihme.get_interpolate_covariate(
                covariate_file_path, age_group_id_dict
        )
        one_age_group_dict[covariate_name] = one_age_group
        interpolate_all_covariate[covariate_name] = interpolate_covariate
    #
    # error_message_dict
    error_message_dict = at_cascade.check_log(
        message_type = 'error',
        all_node_database = all_node_database,
        root_node_database = root_node_database,
        fit_goal_set       = fit_goal_set,
    )
    #
    # n_job
    n_job = len( job_table )
    #
    # job_row
    for (job_id, job_row) in enumerate(job_table) :
        #
        # job_name, fit_node_id, fit_split_reference_id
        job_name               = job_row['job_name']
        fit_node_id            = job_row['fit_node_id']
        fit_split_reference_id = job_row['split_reference_id']
        #
        # node_name, split_reference_name
        node_name = node_table[fit_node_id]['node_name']
        split_reference_name = \
        split_reference_table[fit_split_reference_id]['split_reference_name']
        #
        # database_dir
        database_dir           = at_cascade.get_database_dir(
            node_table              = node_table               ,
            split_reference_table   = split_reference_table    ,
            node_split_set          = node_split_set           ,
            root_node_id            = root_node_id             ,
            root_split_reference_id = root_split_reference_id  ,
            fit_node_id             = fit_node_id              ,
            fit_split_reference_id  = fit_split_reference_id   ,
        )
        #
        # file_in
        file_in = f'{result_dir}/{database_dir}/dismod.db'
        #
        # file_out
        file_out = f'{result_dir}/{database_dir}/ihme.csv'
        #
        # check for an error message in corresponding database
        if job_name in error_message_dict :
            if os.path.exists( file_out ) :
                os.path.remove( file_out )
            print( f'{job_id+1}/{n_job} Error in {job_name}' )
        elif not os.path.exists( file_in ) :
            print( f'{job_id+1}/{n_job} Missing dismod.db for {job_name}' )
        else :
            print( f'{job_id+1}/{n_job} Creating files for {job_name}' )
            #
            # fit_node_database
            fit_node_database = f'{result_dir}/{database_dir}/dismod.db'
            #
            if False :
                ihme_csv_one_job (
                    fit_node_database         ,
                    age_group_id_dict         ,
                    age_group_id_list         ,
                    one_age_group_dict        ,
                    interpolate_all_covariate ,
                    max_plot                  ,
                )
            else :
                # Matplotlib leaks memrory, so use a separate proccess
                # for this call to ihme_csv_one_job so the memory will be
                # freed when it is no longer needed
                #
                # args
                args = (
                    fit_node_database         ,
                    age_group_id_dict         ,
                    age_group_id_list         ,
                    one_age_group_dict        ,
                    interpolate_all_covariate ,
                    max_plot                  ,
                )
                #
                # target
                target = ihme_csv_one_job
                #
                # p
                p = multiprocessing.Process(target = target, args = args)
                #
                p.start()
                p.join()
