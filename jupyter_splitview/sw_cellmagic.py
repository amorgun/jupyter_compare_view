import io
from base64 import b64decode

from IPython.core import magic_arguments
from IPython.core.display import HTML
from IPython.core.magic import Magics, cell_magic, magics_class
from IPython.display import display
from IPython.utils.capture import capture_output
from PIL import Image


@magics_class
class SplitViewMagic(Magics):
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "--position",
        "-p",
        default="50%",
        help=("The position where the slider starts"),
    )
    @magic_arguments.argument(
        "--height",
        "-h",
        default="300",
        help=(
            "The height that the widget has. The width will be adjusted automatically. \
             If height is choosen 'auto', the height will be defined by the resolution \
             in vertical direction of the first image."
        ),
    )
    @cell_magic
    def splity(self, line, cell):
        """Saves the png image and calls the splitview canvas"""

        with capture_output(stdout=False, stderr=False, display=True) as result:
            self.shell.run_cell(cell)

        # saves all jupyter output images into the out_images_base64 list
        out_images_base64 = []
        for output in result.outputs:
            data = output.data
            if "image/png" in data:
                png_bytes_data = data["image/png"]
                out_images_base64.append(png_bytes_data)

        # get the parameters the configure the widget
        args = magic_arguments.parse_argstring(SplitViewMagic.splity, line)

        slider_position = args.position
        widget_height = args.height

        if widget_height == "auto":
            imgdata = b64decode(out_images_base64[0])
            # maybe possible without the PIL dependency?
            im = Image.open(io.BytesIO(imgdata))
            width, height = im.size
            widget_height = height

        html_code = f"""
        <div class="outer_layer" style="position: relative; padding-top: {int(widget_height)+3}px;"> 
            <div class="juxtapose" data-startingposition="{slider_position}" style="height: {int(widget_height)}px;; width: auto; top: 1%; left: 1%; position: absolute;">
                <img src="data:image/jpeg;base64,{out_images_base64[0]}" />' <img src="data:image/jpeg;base64,{out_images_base64[1]}" />'
            </div>
        </div>
        <script src="https://cdn.knightlab.com/libs/juxtapose/latest/js/juxtapose.min.js"></script>
        <link rel="stylesheet" href="https://cdn.knightlab.com/libs/juxtapose/latest/css/juxtapose.css" />
        """
        display(HTML(html_code))
        