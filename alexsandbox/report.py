import plotly.graph_objects as go
from plotly.subplots import make_subplots
import csv
from gp_framework.FitnessCalculator import *


def generate_csv(csv_name: str, header: List[any], rows: List[List[any]]) -> None:
    with open("csvs/{}".format(csv_name), 'w') as csv_file:
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(header)
        csv_writer.writerows(rows)


def _average(floats: List[float]) -> float:
    total = 0
    for i in floats:
        total += i
    return total/len(floats)


def _combine_list_elements(list_: List[float], group_size: int) -> List[float]:
    combined_list = []
    starting_indices = [i for i in range(0, len(list_), group_size)]
    end_index = len(list_) + 1
    for index in starting_indices:
        combined_list.append(_average(list_[index:min(index+group_size, end_index)]))
    return combined_list


def _transpose_list_of_lists(list_of_lists: List[List[any]]) -> List[List[any]]:
    """
    This assumes that all inner_lists have the same length
    :param list_of_lists: the list to transpose
    :return: the transposed list
    """
    new_list = []
    for i in range(len(list_of_lists[0])):
        new_list.append([])
        for j in range(len(list_of_lists)):
            new_list[i].append(list_of_lists[j][i])
    return new_list


def generate_plot_from_csv(csv_name: str, elements_per_point: int, output_name: str,
                           show_plot: bool = True, save_plot: bool = False) -> None:
    """
    Makes nice plots to help visualize data
    :param csv_name: Name of csv file to draw data from
    :param elements_per_point: How many data points to average into one point on the plot
    :param output_name: Name of the plot (appears at the top)
    :param show_plot: Whether or not to display the graph upon creation
    :param save_plot: Whether or not to save the plot
    :return:
    """

    labels: List[str]
    data: List[List[float]] = []

    # read the csv file into a list of lists
    with open("csvs/{}".format(csv_name), 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
        labels = next(reader)
        for row in reader:
            data.append(row)
    data = _transpose_list_of_lists(data)

    # combine the elements of data
    for i in range(len(data)):
        data[i] = _combine_list_elements(data[i], elements_per_point)

    fig = make_subplots(rows=len(data), cols=1, subplot_titles=labels)
    for i in range(len(data)):
        fig.add_trace(go.Scatter(x=[j for j in range(len(data[i]))], y=data[i]), row=i+1, col=1)
    fig.update_layout(height=3000, width=1000*len(data), title_text=output_name)

    if save_plot:
        fig.write_html("plots/{}.html".format(output_name))
    if show_plot:
        fig.show()
