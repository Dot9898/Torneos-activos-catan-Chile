

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import pandas as pd


#Written by AI

def convert_to_fig(dataframe, image_style, emoji_paths):

    padding_x = image_style['row_padding_x']
    row_height = image_style['row_height']
    corner_radius = image_style['corner_radius']
    emoji_text_spacing = image_style['emoji_text_spacing']

    def split_emoji(text):

        if pd.isna(text):
            text = "-"
        else:
            text = str(text)

        for emoji in emoji_paths:

            if text.startswith(emoji):
                return emoji, text[len(emoji):]

        return None, text


    # Temporary renderer for exact text measurement
    measure_fig = plt.figure(dpi=image_style['dpi'])
    measure_renderer = measure_fig.canvas.get_renderer()


    def get_text_width(text, font, size):

        text_artist = plt.Text(
            text=str(text),
            fontsize=size,
            fontproperties=font
        )

        text_artist.set_figure(measure_fig)

        bbox = text_artist.get_window_extent(
            renderer=measure_renderer
        )

        return bbox.width / measure_fig.dpi


    def get_cell_width(value):

        emoji, text = split_emoji(value)

        width = get_text_width(
            text,
            image_style['cell_font'],
            image_style['cell_font_size']
        )

        if emoji:

            width += (
                image_style['cell_font_size'] / 72
                + emoji_text_spacing
            )

        return width


    column_widths = []

    for column in dataframe.columns:

        header_width = get_text_width(
            column,
            image_style['header_font'],
            image_style['header_font_size']
        )

        cell_widths = [
            get_cell_width(value)
            for value in dataframe[column]
        ]

        column_widths.append(
            max([header_width] + cell_widths)
            + 2 * padding_x
        )


    plt.close(measure_fig)


    table_width = sum(column_widths)
    table_height = row_height * (len(dataframe) + 1)


    fig = plt.figure(
        figsize=(table_width, table_height),
        dpi=image_style['dpi']
    )


    ax = fig.add_axes([0, 0, 1, 1])

    ax.set_xlim(0, table_width)
    ax.set_ylim(0, table_height)

    ax.axis('off')


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
            font_color = image_style['header_font_color']

        else:

            background = image_style['cell_background_color']
            separator = image_style['cell_separator_color']
            font = image_style['cell_font']
            font_size = image_style['cell_font_size']
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


        if is_header:

            ax.text(
                x + width / 2,
                y + height / 2,
                str(text),
                fontproperties=font,
                fontsize=font_size,
                color=font_color,
                va='center',
                ha='center'
            )

            return


        emoji, text = split_emoji(text)


        text_width = get_text_width(
            text,
            font,
            font_size
        )


        emoji_width = 0

        if emoji:

            emoji_width = (
                font_size / 72
            )


        total_width = (
            text_width
            + emoji_width
            + (emoji_text_spacing if emoji else 0)
        )


        start_x = (
            x
            + (width - total_width) / 2
        )


        if emoji:

            image = plt.imread(
                emoji_paths[emoji]
            )

            emoji_artist = OffsetImage(
                image,
                zoom=font_size / 120
            )

            annotation = AnnotationBbox(
                emoji_artist,
                (
                    start_x + emoji_width / 2,
                    y + height / 2
                ),
                frameon=False
            )

            ax.add_artist(annotation)


            text_x = (
                start_x
                + emoji_width
                + emoji_text_spacing
            )

        else:

            text_x = start_x


        ax.text(
            text_x,
            y + height / 2,
            text,
            fontproperties=font,
            fontsize=font_size,
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

def fig_to_image_bytes(fig, dpi):

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format='png',
        bbox_inches='tight',
        pad_inches=0,
        transparent = True, 
        dpi = dpi
    )

    buffer.seek(0)

    return buffer.getvalue()

def convert_to_image_bytes(dataframe, image_style, emoji_paths):

    fig = convert_to_fig(
        dataframe,
        image_style, 
        emoji_paths, 
    )

    image_bytes = fig_to_image_bytes(fig, image_style['dpi'])

    plt.close(fig)

    return image_bytes

def crop_background(
    background,
    required_height,
    center_y):

    bg_width, bg_height = background.size


    # If content is larger than background, use the full background
    if required_height >= bg_height:
        return background


    half = required_height // 2

    crop_top = int(center_y - half)
    crop_bottom = crop_top + required_height


    # Keep crop inside image bounds
    if crop_top < 0:
        crop_top = 0
        crop_bottom = required_height


    if crop_bottom > bg_height:
        crop_bottom = bg_height
        crop_top = bg_height - required_height


    return background.crop(
        (
            0,
            crop_top,
            bg_width,
            crop_bottom
        )
    )

def add_background_and_title(
    table_bytes,
    background_bytes,
    font_bytes,
    title,
    subtitle,
    background_center_y
):

    background = Image.open(
        BytesIO(background_bytes)
    ).convert("RGBA")

    table = Image.open(
        BytesIO(table_bytes)
    ).convert("RGBA")

    # Resize table if needed
    max_width = background.width - 200

    if table.width > max_width:

        ratio = max_width / table.width

        table = table.resize(
            (
                round(table.width * ratio),
                round(table.height * ratio)
            ),
            Image.Resampling.LANCZOS
        )

    # Layout spacing
    extra_background = 80

    top_margin = 40 + extra_background
    title_margin = 15
    subtitle_margin = 40
    bottom_margin = 50 + extra_background

    # Fonts
    title_font_size = 80
    subtitle_font_size = 35

    title_font = ImageFont.truetype(
        BytesIO(font_bytes),
        title_font_size
    )

    subtitle_font = ImageFont.truetype(
        BytesIO(font_bytes),
        subtitle_font_size
    )

    draw = ImageDraw.Draw(background)

    # Shrink title until it fits
    while draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )[2] > background.width - 100:

        title_font_size -= 5

        title_font = ImageFont.truetype(
            BytesIO(font_bytes),
            title_font_size
        )

    # Shrink subtitle until it fits
    while draw.textbbox(
        (0, 0),
        subtitle,
        font=subtitle_font
    )[2] > background.width - 100:

        subtitle_font_size -= 5

        subtitle_font = ImageFont.truetype(
            BytesIO(font_bytes),
            subtitle_font_size
        )

    title_height = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )[3]

    subtitle_height = draw.textbbox(
        (0, 0),
        subtitle,
        font=subtitle_font
    )[3]

    # Infer final required height from table size
    required_height = (
        top_margin
        + title_height
        + title_margin
        + subtitle_height
        + subtitle_margin
        + table.height
        + bottom_margin
    )

    # Crop background around chosen center
    background = crop_background(
        background,
        required_height,
        background_center_y
    )

    draw = ImageDraw.Draw(background)

    # Draw title
    title_width = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )[2]

    draw.text(
        (
            (background.width - title_width) // 2,
            top_margin
        ),
        title,
        font=title_font,
        fill=(50, 40, 20, 255)
    )

    # Draw subtitle
    subtitle_width = draw.textbbox(
        (0, 0),
        subtitle,
        font=subtitle_font
    )[2]

    draw.text(
        (
            (background.width - subtitle_width) // 2,
            top_margin + title_height + title_margin
        ),
        subtitle,
        font=subtitle_font,
        fill=(50, 40, 20, 255)
    )

    # Paste table
    table_y = (
        top_margin
        + title_height
        + title_margin
        + subtitle_height
        + subtitle_margin
    )

    table_x = (
        background.width - table.width
    ) // 2

    background.alpha_composite(
        table,
        (
            table_x,
            table_y
        )
    )

    output = BytesIO()

    background.save(
        output,
        format="PNG",
        optimize=True
    )

    return output.getvalue()



