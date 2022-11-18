import io
import base64
import enum
import os
import uuid
from pathlib import Path
from jinja2 import Template, StrictUndefined
import IPython


def img2base64(img):
    import matplotlib.pyplot as plt
    
    im_file = io.BytesIO()
    plt.imsave(im_file, img, format='jpeg')
    im_bytes = im_file.getvalue()
    return base64.b64encode(im_bytes)


def img2url(img):
    if not isinstance(img, str):
        return f"data:image/jpeg;base64,{str(img2base64(img).strip(), 'utf8')}"
    return img.strip()


def compile_template(in_file: str, **variables) -> str:
    with open(in_file, "r", encoding="utf-8") as file:
        template = Template(file.read(), undefined=StrictUndefined)
    return template.render(**variables)


def prepare_html(image_urls: typing.List[str], height: str, add_controls: bool, config: dict) -> str:
    uid=uuid.uuid1()
    config['key'] = str(uid)
    if add_controls:
        config["controls_id"] = f"controls_{uid}"
    root = Path(__file__).parent
    js_path = root / "../vendor/compare_view/browser_compare_view.js"
    js = js_path.read_text()
    return compile_template(
        root / "template.html",
        uid=uid,
        image_urls=image_urls,
        height=height,
        js=js,
        add_controls=add_controls,
        config=json.dumps(config),
    )


@enum.unique
class StartMode(str, enum.Enum):
    CIRCLE = "circle"
    HORIZONTAL = "horizonal"
    VERTICAL = "vertical"


def compare(
    images: typing.List[str],
    height: typing.Union[str|int] ='auto',
    add_controls: bool = True,
    # // either "circle", "horizonal" or "vertical"
    start_mode: StartMode = StartMode.CIRCLE,
    # // size of circle outline as fraction of image width or height (whatever is bigger)
    circumference_fraction: float = 0.005,
    # // overwrite circle size
    circle_size: typing.Optional[float] = None,
    circle_fraction: float = 0.2,
    # // draw line around circle
    show_circle: bool = True,
    revolve_imgs_on_click: bool = True,
    slider_fraction: float = 0.01,
    # // time slider takes to reach clicked location
    slider_time: float = 400,
    # // apply when moving slider
    # // see: https://easings.net
    # rate_function: str = 'ease_in_out_cubic',
    # // 0.0 -> left; 1.0 -> right
    start_slider_pos: float = 0.5,
    # // draw line at slider
    show_slider: bool = True,
):
    image_urls = [
        img2url(img) for img in images
    ]
    _locals = locals()
    config = {k: _locals[k] for k in [
            'start_mode',
            'circumference_fraction',
            'circle_fraction',
            'show_circle',
            'revolve_imgs_on_click',
            'slider_fraction',
            'slider_time',
            # 'rate_function',
            'start_slider_pos',
            'show_slider',
        ]
        + ['circle_size'] * (circle_size is not None)
    }
    html = prepare_html(
        image_urls=image_urls,
        height=f'{height}px' if not isinstance(height, str) else height,
        add_controls=add_controls,
        config=config,
    )
    return IPython.display.HTML(html)
