

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO


#Original source before styling: https://github.com/imaadmkhan1/dataframe_to_image


def convert_to_fig(dataframe, image_style):

    col_width=2.0
    row_height = image_style['row_height']

    ax=None



    if ax is None:
        size = (np.array(dataframe.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig = plt.figure(figsize=size)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')

    mpl_table = ax.table(cellText=dataframe.values, colLabels=dataframe.columns)
    mpl_table.auto_set_font_size(False)

    for k, cell in mpl_table._cells.items():
        cell.set_linewidth(image_style['separator_width'])

        if k[0] == 0:
            cell.set_facecolor(image_style['header_background_color'])
            cell.set_edgecolor(image_style['header_separator_color'])
            cell.set_text_props(font = image_style['header_font'], 
                                size = image_style['header_font_size'], 
                                weight = image_style['header_font_weight'], 
                                color = image_style['header_font_color'])
        
        else:
            cell.set_facecolor(image_style['cell_background_color'])
            cell.set_edgecolor(image_style['cell_separator_color'])
            cell.set_text_props(font = image_style['cell_font'], 
                                size = image_style['cell_font_size'], 
                                weight = image_style['cell_font_weight'], 
                                color = image_style['cell_font_color'])
    
    mpl_table.auto_set_column_width(range(len(dataframe.columns)))

    return(fig)

def fig_to_image_bytes(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format = 'png', bbox_inches = 'tight', pad_inches = 0)
    return(buffer.getvalue())

def convert_to_image_bytes(dataframe, image_style):
    fig = convert_to_fig(dataframe, image_style)
    bytes_ = fig_to_image_bytes(fig)
    return(bytes_)






from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle


def convert_to_fig(dataframe, image_style):

    padding_x = image_style.get('cell_padding_x', 0.15)
    row_height = image_style['row_height']
    corner_radius = image_style.get('corner_radius', 0.05)

    def estimate_text_width(text, font_size):
        return len(str(text)) * font_size * 0.012

    # Column widths
    column_widths = []

    for column in dataframe.columns:
        values = [column] + dataframe[column].astype(str).tolist()

        width = max(
            estimate_text_width(
                value,
                max(
                    image_style['header_font_size'],
                    image_style['cell_font_size']
                )
            )
            for value in values
        )

        column_widths.append(width + 2 * padding_x)

    table_width = sum(column_widths)
    table_height = row_height * (len(dataframe) + 1)

    fig = plt.figure(
        figsize=(table_width, table_height),
        dpi=100
    )

    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, table_width)
    ax.set_ylim(0, table_height)
    ax.axis('off')

    # Outer rounded table background
    table_shape = FancyBboxPatch(
        (0, 0),
        table_width,
        table_height,
        boxstyle=f"round,pad=0,rounding_size={corner_radius}",
        linewidth=image_style['separator_width'],
        edgecolor=image_style['cell_separator_color'],
        facecolor=image_style['cell_background_color']
    )

    ax.add_patch(table_shape)

    def draw_cell(x, y, width, height, text, is_header):

        if is_header:
            background = image_style['header_background_color']
            separator = image_style['header_separator_color']
            font = image_style['header_font']
            font_size = image_style['header_font_size']
            font_weight = image_style['header_font_weight']
            font_color = image_style['header_font_color']

        else:
            background = image_style['cell_background_color']
            separator = image_style['cell_separator_color']
            font = image_style['cell_font']
            font_size = image_style['cell_font_size']
            font_weight = image_style['cell_font_weight']
            font_color = image_style['cell_font_color']

        cell = Rectangle(
            (x, y),
            width,
            height,
            linewidth=image_style['separator_width'],
            edgecolor=separator,
            facecolor=background
        )

        cell.set_clip_path(table_shape)
        ax.add_patch(cell)

        ax.text(
            x + padding_x,
            y + height / 2,
            str(text),
            fontname=font,
            fontsize=font_size,
            fontweight=font_weight,
            color=font_color,
            va='center',
            ha='left'
        )

    # Header
    y = table_height - row_height
    x = 0

    for column, width in zip(dataframe.columns, column_widths):
        draw_cell(
            x,
            y,
            width,
            row_height,
            column,
            True
        )

        x += width

    # Body
    for _, row in dataframe.iterrows():

        y -= row_height
        x = 0

        for value, width in zip(row, column_widths):

            draw_cell(
                x,
                y,
                width,
                row_height,
                value,
                False
            )

            x += width

    return fig


def fig_to_image_bytes(fig):

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format='png',
        bbox_inches='tight',
        pad_inches=0
    )

    buffer.seek(0)

    return buffer.getvalue()


def convert_to_image_bytess(dataframe, image_style):

    fig = convert_to_fig(
        dataframe,
        image_style
    )

    image_bytes = fig_to_image_bytes(fig)

    plt.close(fig)

    return image_bytes





