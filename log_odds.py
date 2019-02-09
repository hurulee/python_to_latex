import pandas as pd

# config

model_name = 'Option ARM C to D30'
model_label = 'po_c_30'
results_out = 'unit_model_material'
transition = 'p' # p = prepay, c = cure, d = delinquency

#create test dataframes
arm_Margin = {
     'variable': [1, 24, 48, 72],
     'contrib': [0.0616, 1.4784, 0.8160, -0.1416]}

arm_Margin_df = pd.DataFrame(data=arm_Margin)

mfico = {
     'variable': [600, 700, 725, 750, 775, 800],
     'contrib': [0.6060, 0.7070, 0.7590, 0.7988, 0.8708, 0.96225]}

mfico_df = pd.DataFrame(data=mfico)

mcltv = {
     'variable': [30, 50, 70, 90, 110, 130],
     'contrib': [-0.3120, -0.52, -0.6894, -1.2314, -2.5094, -3.3054]}

mcltv_df = pd.DataFrame(data=mcltv)

upb = {
     'variable': [4.6, 4.8, 5, 5.2, 5.4, 5.6],
     'contrib': [-12.2871, -12.8213, -12.4610, -12.2968, -12.1289, -12.03904]}

upb_df = pd.DataFrame(data=upb)

uer = {
     'variable': [4.6, 4.8],
     'contrib': [-12.2871, -12.8213]}

uer_df = pd.DataFrame(data=uer)

hpi = {
     'variable': [2.6, 4.5],
     'contrib': [10.2871, 12.8213]}

hpi_df = pd.DataFrame(data=hpi)


age = {
     'variable': [1, 24, 48, 72, 96, 108, 132],
     'contrib': [0.0616, 1.4784, 1.4784, -0.1416, 0.567, 0.89, 0.324]}

age_df = pd.DataFrame(data=age)


def slope_change(df):

    # get floor and cap of variable
    knot_list = df['variable'].tolist()
    floor = knot_list.pop(0)
    cap = knot_list.pop()

    # determine if line segment is positively or negatively sloped
    contrib_list = df['contrib'].tolist()

    slope_list = []
    for i in range(0, len(df)-1):

        diff = contrib_list[i+1] - contrib_list[i]
        if diff > 0:
            slope = 1
        elif diff < 0:
            slope = -1
        else:
            slope = 0
        slope_list.append(slope)

    # identify the knot where sign change occurs
    slope_list = [0] + slope_list
    temp = pd.Series(slope_list)
    df_copy = df.copy()
    df_copy['change'] = temp.values
    df_copy['change_1'] = df_copy['change'].shift(-1)
    df_copy['change_1'].fillna(df_copy['change'], inplace=True)
    df_copy = df_copy.drop(df_copy[df_copy['change'] == 0].index)
    df_copy = df_copy.drop(df_copy[df_copy['change'] == df_copy['change_1']].index)
    slope_knot_change_list = df_copy['variable'].tolist()
    slope_list = [x for x in slope_list if x != 0]


    slope_change = []

    for i in range(0, len(slope_list)-1):
        if slope_list[i+1] == slope_list[i]:
            change = 0
        else:
            change = 1
        slope_change.append(change)

    num_changes = sum(slope_change)
    slope = slope_list[0]

    return slope_knot_change_list, num_changes, slope, floor, cap


macro_list = [arm_Margin_df, mfico_df, mcltv_df, upb_df, uer_df, hpi_df, age_df]

macro_name_list = ['arm_Margin', 'mfico', 'mcltv', 'upb', 'uer', 'hpi', 'age']

macro_name_latex = [w.replace('_', '\\_') for w in macro_name_list]


macro_name_list = [x.lower() for x in macro_name_list]

LO_figure_header = r'''

\begin{figure}[H]
\centering
\def\HideLegend{true}
\def\CustomLines{contrib/contrib/mark=*}
\def\ChartWidth{0.6\textwidth}
\def\ChartHeight{0.44\textwidth}
'''

LO_figure_csv_path_start = r'''\PlotScatterLines{'''

LO_figure_yaxis_start = r'''
{'''

LO_figure_xaxis = r'''
{Logodds Contribution}'''

LO_figure_legend_info = r'''
{}
'''

LO_figure_caption_start = r'''\caption{'''

LO_figure_ref_start = r'''\ref{fig:'''

LO_figure_label_start = r'''\label{fig:'''

LO_figure_brace_end = r'''}'''

LO_figure_footer = r'''
\end{figure}
'''

paragraph_break = r'''

'''


script_dict = {
    'log_odds_intro_1': 'The effect of ',
    'log_odds_intro_2': 'is estimated via a linear spline function, ',
    'log_odds_intro_3': 'which is floored at ',
    'log_odds_intro_4': 'and capped at ',
    'log_odds_intro_5': "The estimated log odds contribution for the variable's effect is presented in Figure ",
    'log_odds_analysis_1': ' shows, the log odds contribution curve is monotonically increasing. ',
    'log_odds_analysis_2': ' shows, the log odds contribution curve is monotonically decreasing. ',
    'log_odds_analysis_3': ' shows, the log odds contribution curve exhibits an inverted U-shape,',
    'log_odds_analysis_4': ' shows, the log odds contribution curve exhibits a U-shape,',
    'log_odds_analysis_5': ' shows, the log odds contribution curve changes slope in multiple locations,'
                           ' where the slope changes when ',
    'log_odds_analysis_6': ' where a change in slope occurs when ',
    'log_odds_analysis_7': 'This result is consistent with economic intuition. ',
    'log_odds_analysis_8': 'This implies that the likelihood of prepayment increases as ',
    'log_odds_analysis_9': 'This implies that the likelihood of prepayment decreases as ',
    'log_odds_analysis_10': 'This implies that the likelihood of delinquency increases as ',
    'log_odds_analysis_11': 'This implies that the likelihood of delinquency decreases as ',
    'log_odds_analysis_12': 'This implies that the likelihood of curing increases as ',
    'log_odds_analysis_13': 'This implies that the likelihood of curing decreases as ',
    'log_odds_analysis_14': ' and then increases thereafter. ',
    'log_odds_analysis_15': ' and then decreases thereafter. ',
    'arm_margin': 'ARM margin ',
    'mfico': 'FICO at origination ',
    'mcltv': 'current LTV ',
    'upb': 'unpaid principal balance ',
    'uer': 'unemployment rate ',
    'hpi': 'housing price index ',
    'age': 'loan age ',
}


with open("unit_model_material/log_odds.tex", "w") as text_file:

    for i in range(0, len(macro_name_list)):

        slope_knot_change_list, num_changes, slope, floor, cap = slope_change(macro_list[i])

        print(script_dict['log_odds_intro_1'] + script_dict[macro_name_list[i]] + script_dict['log_odds_intro_2'] +
              script_dict['log_odds_intro_3'] + str(floor) + ' ' + script_dict['log_odds_intro_4'] + str(cap) + '. ' +
              script_dict['log_odds_intro_5'] + LO_figure_ref_start + model_label + '_logodds_' +
              macro_name_list[i] + LO_figure_brace_end + '.', file=text_file)

        print(LO_figure_header +
              LO_figure_csv_path_start + results_out + r'''/''' + macro_name_list[i] + r'''.csv''' +
              LO_figure_brace_end + LO_figure_yaxis_start + macro_name_latex[i] + LO_figure_brace_end +
              LO_figure_xaxis +
              LO_figure_legend_info +
              LO_figure_caption_start + model_name + r''' transition state regression log odds contribution of ''' +
              script_dict[macro_name_list[i]] +
              LO_figure_label_start + model_label + '_logodds_' + macro_name_list[i] + LO_figure_brace_end +
              LO_figure_brace_end +
              LO_figure_footer, file=text_file)

        print('As Figure ' + LO_figure_ref_start + model_label + '_logodds_' + macro_name_list[i] +
              LO_figure_brace_end, file=text_file)

        if num_changes == 0:

            if (slope == 1) and (transition == 'p'):
                print(script_dict['log_odds_analysis_1'] + script_dict['log_odds_analysis_8'], file=text_file)
            elif (slope == 1) and (transition == 'c'):
                print(script_dict['log_odds_analysis_1'] + script_dict['log_odds_analysis_12'], file=text_file)
            elif (slope == 1) and (transition == 'd'):
                print(script_dict['log_odds_analysis_1'] + script_dict['log_odds_analysis_10'], file=text_file)
            elif (slope == -1) and (transition == 'p'):
                print(script_dict['log_odds_analysis_2'] + script_dict['log_odds_analysis_9'], file=text_file)
            elif (slope == -1) and (transition == 'c'):
                print(script_dict['log_odds_analysis_2'] + script_dict['log_odds_analysis_13'], file=text_file)
            else:
                # (slope == -1) and (transition == 'd')
                print(script_dict['log_odds_analysis_2'] + script_dict['log_odds_analysis_11'], file=text_file)

            print(script_dict[macro_name_list[i]] + 'increases. ' + script_dict['log_odds_analysis_7'] +
                  paragraph_break, file=text_file)

        elif (num_changes == 1) and (slope == 1):

            print(script_dict['log_odds_analysis_3'] + script_dict['log_odds_analysis_6'] +
                  script_dict[macro_name_list[i]] + 'equals ' + str(slope_knot_change_list[0]) + '. ', file=text_file)

            if transition == 'p':
                print(script_dict['log_odds_analysis_8'] + script_dict[macro_name_list[i]] + 'increases to ',
                      file=text_file)
            elif transition == 'c':
                print(script_dict['log_odds_analysis_10'] + script_dict[macro_name_list[i]] + 'increases to ',
                      file=text_file)
            else:
                print(script_dict['log_odds_analysis_12'] + script_dict[macro_name_list[i]] + 'increases to ',
                      file=text_file)

            print(str(slope_knot_change_list[0]) + script_dict['log_odds_analysis_15'] +
                  script_dict['log_odds_analysis_7'] +
                  paragraph_break, file=text_file)

        elif (num_changes == 1) and (slope == -1):

            print(script_dict['log_odds_analysis_4'] + script_dict['log_odds_analysis_6'] +
                  script_dict[macro_name_list[i]] + 'equals ' + str(slope_knot_change_list[0]) + '. ', file=text_file)

            if transition == 'p':
                print(script_dict['log_odds_analysis_9'] + script_dict[macro_name_list[i]] + 'increases to ',
                      file=text_file)
            elif transition == 'c':
                print(script_dict['log_odds_analysis_11'] + script_dict[macro_name_list[i]] + 'increases to ',
                      file=text_file)
            else:
                # (slope == -1) and (transition == 'd')
                print(script_dict['log_odds_analysis_13'] + script_dict[macro_name_list[i]] + 'increases to ',
                      file=text_file)

            print(str(slope_knot_change_list[0]) + script_dict['log_odds_analysis_14'] +
                  script_dict['log_odds_analysis_7'] +
                  paragraph_break, file=text_file)

        else:
            print(script_dict['log_odds_analysis_5'] + script_dict[macro_name_list[i]] + 'equals '
                  , file=text_file)
            for j in range(0, len(slope_knot_change_list) - 1):
                print(str(slope_knot_change_list[j]) + ', ', file=text_file)
            print('and ', file=text_file)
            last_knot = slope_knot_change_list.pop()
            print(str(last_knot) + '. ' + script_dict['log_odds_analysis_7'] +
                  paragraph_break, file=text_file)

