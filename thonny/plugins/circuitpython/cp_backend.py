import logging
import time

from thonny.plugins.micropython.backend import INTERRUPT_CMD
from thonny.plugins.micropython.bare_metal_backend import (
    BareMetalMicroPythonBackend,
    SOFT_REBOOT_CMD,
)

logger = logging.getLogger(__name__)


class CircuitPythonBackend(BareMetalMicroPythonBackend):
    def _extra_interrupts_after_soft_reboot(self):
        logger.debug("Extra interrupts for CP")
        # CP runs code.py after soft-reboot even in raw repl, so I'll send some Ctrl-C to intervene
        # # (they don't do anything when already in raw repl)
        self._write(INTERRUPT_CMD)
        time.sleep(0.05)
        self._write(INTERRUPT_CMD)
        time.sleep(0.3)
        self._write(INTERRUPT_CMD)
        time.sleep(0.05)
        self._write(INTERRUPT_CMD)

    def _soft_reboot_without_running_main(self):
        logger.debug("_soft_reboot_in_normal_mode_without_running_main")
        # no point in going to raw mode at all
        self._write(SOFT_REBOOT_CMD + INTERRUPT_CMD)
        self._extra_interrupts_after_soft_reboot()

        def ignore_output(data, stream):
            pass

        self._forward_output_until_active_prompt(ignore_output)
