import os

# config

model_name = 'Option ARM C to D30'
model_label = 'po_c_30'
results_out = 'unit_model_material'
data_in = 'unit_model_material'
sample = 'is'


bt_figure_header = r'''
\begin{figure}[H]
\centering
\def\ChartWidth{0.39\textwidth}
\def\ChartHeight{0.35\textwidth}
\def\LegendColumns{4}
\def\SubChart{}
\begin{tabular}{rr}'''

bt_subfigure_header = r'''\def\YAxisModL{*100}
\def\DateFormat{\Mon\year}'''

bt_subtitle = r'''\def\SubTitle{'''

bt_figure_csv_path_start = r'''
\PlotScatterLinesAndArea{'''

bt_figure_brace_end = r'''}'''

bt_subfigure_footer = r'''{dates}
{Monthly rate}
{Loan count}
{}
{}'''

bt_hspace = r'''&\hspace{0.5cm}'''

line_break = r'''\\'''

bt_end_tabular = r'''\end{tabular}
\caption{'''

bt_figure_ref_start = r'''\ref{fig:'''

bt_figure_label_start = r'''\label{fig:'''


bt_figure_footer = r'''
\end{figure}
'''

bt_dict = {
    'is': 'in-sample ',
    'oos': 'out-of-sample ',
    'oot': 'out-of-time ',
}

knots = [600, 650, 700, 750, 800]
# variable_list = ['meanfico', 'lmcltv']

variable_list = ['meanfico']

bt_tex_path = os.path.join(results_out + '/' + sample + '_' + variable_list[0] + '.tex')

with open(bt_tex_path, "w") as text_file:

    print(bt_figure_header, file=text_file)

    for j in range(0, len(knots)):

        print(bt_subfigure_header, file=text_file)

        if j == 0:
            print(bt_subtitle + r'''\textless ''' + str(knots[j]) + bt_figure_brace_end +
                  bt_figure_csv_path_start + data_in + '/' + variable_list[0] + '_' + str(j) +
                  '.csv' + bt_figure_brace_end, file=text_file)
        else:
            print(bt_subtitle + str(knots[j-1]) + ' - ' + str(knots[j]) + bt_figure_brace_end +
                  bt_figure_csv_path_start + data_in + '/' + variable_list[0] + '_' + str(j) +
                  '.csv' + bt_figure_brace_end, file=text_file)

        print(bt_subfigure_footer, file=text_file)

        if j in (0, 2, 4):
            print(bt_hspace, file=text_file)
        else:
            print(line_break, file=text_file)

    print(bt_subfigure_header, file=text_file)
    print(bt_subtitle + r'''\textgreater ''' + str(knots[-1]) + bt_figure_brace_end +
          bt_figure_csv_path_start + data_in + '/' + variable_list[0] + '_' + str(len(knots)) +
          '.csv' + bt_figure_brace_end, file=text_file)
    print(bt_subfigure_footer, file=text_file)

    print(bt_end_tabular + model_name + ' transition state regression ' + bt_dict[sample] +
          'performance by time according to ' + variable_list[0] + ' bucket' +
          bt_figure_label_start + '_' + sample + '_' + model_label + '_' + variable_list[0] +
          bt_figure_brace_end + bt_figure_brace_end + bt_figure_footer, file=text_file)
