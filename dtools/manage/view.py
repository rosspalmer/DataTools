import pandas as pd
from prettytable import PrettyTable

def display_models(data, model_manager, model_list):

    model_df = model_manager.model_table
    if model_list <> 'ALL':
        model_df = model_df[model_df['model_id'].isin(model_list)]

    model_list = model_df['model_id'].unique()
    model_types = model_df['type'].unique()

    for model_type in model_types:

        summary_df = data.int_df['%s_summary' % model_type]
        summary_df = summary_df[summary_df['model_id'].isin(model_list)]

        summary_table = PrettyTable(summary_df.columns.tolist())

        for ll in summary_df.iloc[0].tolist():
            print type(ll)

        for i in range(len(summary_df.index)):
            summary_table.add_row(summary_df.iloc[i].tolist())

        coeff_df = data.int_df['%s_coeff' % model_type]
        coeff_df = coeff_df[coeff_df['model_id'].isin(model_list)]

        print
        print '>>>>>>>---- %s Models ----<<<<<<<' % model_type.capitalize()
        print
        print '----Summary----'
        print
        print  summary_table
        print
        print '----Coefficients----'
        print

        type_model_list = summary_df['model_id'].unique()

        for model_id in type_model_list:

            coeff_df_model = coeff_df[coeff_df['model_id']==model_id]
            coeff_table = PrettyTable(coeff_df_model.columns.tolist())

            for i in range(len(coeff_df_model.index)):
                coeff_table.add_row(coeff_df_model.iloc[i].tolist())

            print coeff_table
            print

