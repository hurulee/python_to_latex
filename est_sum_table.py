import pandas as pd
import numpy as np
import os
from collections import OrderedDict

# config

model_name = r'''Option ARM C to D30'''
model_label = 'po_c_30'
results_out = 'unit_model_material'


#create test dataframe
d = {'var_name': ['intercept', 'meanfico', 'meanfico', 'meanfico', 'meanfico', 'doctype'],
     'sas_variable': ['intercept', 'LS_meanfico_1', 'LS_meanfico_2', 'LS_meanfico_3', 'LS_meanfico_4', 'doctype_full'],
     'value': ['','[600, 650)','[650, 700)','[700, 750)','[750, 800)', ''],
     'estimate': [0.1243, 0.00875, 0.0153, 0.0334, 0.5227, -1.554],
     'std_err': [0.586, 0.1124, 0.655, 0.324, 0.653, 0.567],
     'chi_sq': [155.47, 6765.24, 323.53, 78.99, 656.89, 23.77],
     'p_value': [0.98, 0.048, 0.02, 0.03, 0.033, 0.074]}

df = pd.DataFrame(data=d)


# convert dataframe to latex-friendly csv file
df_csv = df.copy()
df_csv['var_name'] = df_csv['var_name'].str.replace('_','\\_')
df_csv['sas_variable'] = df_csv['sas_variable'].str.replace('_','\\_')
df_csv['value'] = df_csv['value'].str.replace(',','\quotesinglbase\\thinspace ')
csv_path = os.path.join(results_out + '/finalSpec.csv')
df_csv.to_csv(csv_path, index=False)

# determine if there are insignificant variables (ex-intercept)
df_x_int = df.copy()
df_x_int = df_x_int[(df_x_int['var_name'] != 'intercept')]

df_x_int['key_1'] = np.where(df_x_int['p_value']>0.05, 1, 0)

total = df_x_int['key_1'].sum()

if total >= 1:
    insig_vars = []
    for i in range(0, len(df_x_int)):
        if df_x_int.iloc[i]['key_1'] == 1:
            var = df_x_int.iloc[i]['sas_variable']
            insig_vars.append(var)
        else:
            pass

else:
    pass


est_summary_header = r'''
\begin{landscape}
{
\scriptsize
\pgfplotstabletypeset[
every even row/.style={before row=\hline},
every odd row/.style={before row=\hline},
columns/var_name/.style={column type=|p{0.28\textwidth}},
columns/sas_variable/.style={column type=|>{\centering\arraybackslash}m{1.6in}},
columns/value/.style={column type=|>{\centering\arraybackslash}m{1.5in}},
columns/estimate/.style={column type=|>{\centering\arraybackslash}m{0.5in}},
columns/std_err/.style={column type=|>{\centering\arraybackslash}m{0.4in}},
columns/chi_sq/.style={column type=|>{\centering\arraybackslash}m{0.4in}},
columns/p_value/.style={column type=|>{\centering\arraybackslash}m{0.4in}|},
empty header,
begin table=\begin{longtable},
every first row/.append style={before row={
'''

est_summary_config = r'''
\\
\bottomrule
\cellcolor{gray!25}\textbf{Variable} & \cellcolor{gray!25}\textbf{SAS Variable} & \cellcolor{gray!25}\textbf{Value} & \cellcolor{gray!25}\textbf{Estimate} & \cellcolor{gray!25}\textbf{Std. Error} & \cellcolor{gray!25}\textbf{Wald Chi-Square} & \cellcolor{gray!25}\textbf{Pr \textgreater Chi Sq} \\ \hline
\endfirsthead
\multicolumn{7}{c}
{{Table \thetable\ - \textit{Continued from previous page}}} \\
\bottomrule
\cellcolor{gray!25}\textbf{Variable} & \cellcolor{gray!25}\textbf{SAS Variable} & \cellcolor{gray!25}\textbf{Value} & \cellcolor{gray!25}\textbf{Estimate} & \cellcolor{gray!25}\textbf{Std. Error} & \cellcolor{gray!25}\textbf{Wald Chi-Square} & \cellcolor{gray!25}\textbf{Pr \textgreater Chi Sq} \\ 
\endhead
\multicolumn{7}{r}{{\textit{Continued on next page}}} \\
\endfoot
\hline
\multicolumn{7}{r}{} \\
\endlastfoot
}},
end table=\end{longtable},
col sep=comma,
string type,
]
'''

est_summary_footer = r'''}\end{landscape}'''

est_summary_caption_start = r'''\caption{Estimation summary for '''

est_summary_csv_path_start = r'''{'''

est_summary_ref_end = r'''_finalSpec}'''

est_summary_label_end = r'''_finalSpec}'''

est_summary_csv_path_end = r'''/finalSpec.csv}'''

est_summary_caption_end = r''' model}'''

table_ref_start = r'''\ref{tab:'''

table_label_start = r'''\label{tab:'''





script_dict = {
    'finalSpec_intro_1': 'A more detailed description of the variables included in the final specification is '
                         'provided in the Appendix. ',
    'finalSpec_analysis_1': 'the signs of the coefficients for the key variables included in the final specification '
                            'are consistent with economic intuition. ',
    'finalSpec_analysis_2': 'Furthermore, the Wald statistic shows that all of the variables are statistically '
                            'significant at the 5\% level.',
}




if total >= 1:
    insig_vars_latex = [w.replace('_', '\\_') for w in insig_vars]
    d = OrderedDict()
    for idx, value in enumerate(insig_vars_latex):
        key = 'var' + str(idx)
        d[key] = value
else:
    pass

with open("unit_model_material/finalSpec.tex", "w") as text_file:

    print('Table ' + table_ref_start + model_label + est_summary_label_end +
          ' presents the final specification of the ' +
          model_name +
          ' transition state regression model, along with the estimated coefficients. ' +
          script_dict['finalSpec_intro_1']
          , file=text_file)

    print(est_summary_header +
          est_summary_caption_start + model_name + est_summary_caption_end +
          table_label_start + model_label + est_summary_label_end +
          est_summary_config +
          est_summary_csv_path_start + results_out + est_summary_csv_path_end +
          est_summary_footer
          , file=text_file)



    if total >= 1:
        if total == 1:
            print('Table ' + table_ref_start + model_label + est_summary_label_end +
                  ' shows that ' + script_dict['finalSpec_analysis_1'] + ' However, ' +
                  d['var0'] + ' is not statistically significant at the 5\% level.'
                  , file=text_file)
        if total > 1:
            print('Table ' + table_ref_start + model_label + est_summary_label_end +
                  ' shows that ' + script_dict['finalSpec_analysis_1'] +
                  'However, the following variables are not statistically significant at the 5\% level:'
                  , file=text_file)
            print(r'''\begin{itemize}''', file=text_file)
            for i in range(0, len(insig_vars_latex)):
                print(r'''\item ''' + insig_vars_latex[i], file=text_file)
            print(r'''\end{itemize}''', file=text_file)
    else:
        print('Table ' + table_ref_start + model_label + est_summary_label_end +
              ' shows that ' + script_dict['finalSpec_analysis_1'] +
              script_dict['finalSpec_analysis_2']
              , file=text_file)
