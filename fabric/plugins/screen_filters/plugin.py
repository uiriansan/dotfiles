from utils.plugins import ToolbarPlugin
from widgets.common_button import CommonButton
from .service import FilterService
from .popover import ScreenFiltersPopover

class ScreenFilters(ToolbarPlugin):
    def __init__(self):
        self._name = "screen_filters"
        self._description = "Show screen filters button."

        self.shell_context = None

        self._filters_enabled = True
        self._min_brightness = 0.5
        self._max_brightness = 1.0
        self._min_blf = 2000.0
        self._max_blf = 25000.0
        self._filter_service = FilterService.get_instance()

    def get_popover_content(self):
        return ScreenFiltersPopover(self._filter_service)

    def initialize(self, shell_context):
        self.shell_context = shell_context
        self._filter_service.shader_on()

    def register_toolbar_widget(self):
        return CommonButton(
            name="screen-filters-button", icon="brightness", title="Screen filters", l_popover_factory=self.get_popover_content
        )
