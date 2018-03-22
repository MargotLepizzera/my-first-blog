from functools import partial

from pyexcel._compact import PY2


class Plotter(object):
    def __init__(self, instance):
        self._ref = instance
        try:
            from pyexcel_echarts.options import CHART_TYPES

            for key in CHART_TYPES.keys():
                setattr(self.__class__, key, make_echarts_presenter(key))
        except ImportError:
            pass

        # to detect svg, jpeg, png
        for file_type in ['svg', 'jpeg', 'png']:
            setattr(self.__class__, file_type, make_graphics(file_type))

    def _repr_svg_(self):
        return self.svg()


def make_graphics(file_type):
    def draw_chart_in_file(self, **keywords):
        # make the signature for jypter notebook
        memory_content = self._ref.save_to_memory(
            file_type, **keywords)

        setattr(memory_content,
                '_repr_%s_' % file_type,
                partial(get_content, memory_content))
        return memory_content
    draw_chart_in_file.__doc__ = "Draw charts in %s format" % file_type
    return draw_chart_in_file


def get_content(class_instance):
    content = class_instance.getvalue()
    if PY2:
        content = content.decode('utf-8')
    return content


def make_echarts_presenter(chart_type):
    def draw_chart(self, **keywords):
        file_type = 'echarts.html'
        memory_content = self._ref.save_to_memory(
            file_type, title=self._ref.name, chart_type=chart_type,
            mode='notebook', **keywords)

        setattr(memory_content,
                '_repr_html_',
                partial(get_content, memory_content))
        return memory_content
    draw_chart.__doc__ = "Draw %s chart" % chart_type
    return draw_chart
