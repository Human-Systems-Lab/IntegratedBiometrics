import ibs
from . import main


class TestComponent(ibs.IbsCmp):
    def startup_ref(self):
        return main.startup

    def shutdown_ref(self):
        return main.shutdown

    def get_widget(self):
        return main.Widget()


main.api = ibs.reg_ext(TestComponent())
