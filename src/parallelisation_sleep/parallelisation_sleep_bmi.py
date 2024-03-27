from typing import Any, Tuple
import time
import numpy as np
from parallelisation_sleep import utils
from parallelisation_sleep.lumped_bmi import LumpedBmi


class ParallelisationSleep(LumpedBmi):
    """Used to test parallelisation"""

    def initialize(self, config_file: str) -> None:
        # The model config contains the precipitation file, and the model parameter.
        self.config: dict[str, Any] = utils.read_config(config_file)

        self.start_time = 0
        self.current_timestep = self.start_time

        self.end_timestep = 20_000_000

        # The one model parameter is the 'sleepiness' of the model:
        self.sleepiness = self.config["sleepiness"]

    def update(self) -> None:

        if self.current_timestep < self.end_timestep:
            # Do calculations for current timestep

            time.sleep(self.sleepiness)

            # Advance the model time by one step
            self.current_timestep += self.sleepiness


    def get_component_name(self) -> str:
        return "Parallelisation Sleep"

    def get_value(self, var_name: str, dest: np.ndarray) -> np.ndarray:
        match var_name:
            case "sleep":
                dest[:] = np.array(self.sleepiness)
                return dest
            case _:
                raise ValueError(f"Unknown variable {var_name}")

    def get_var_units(self, var_name: str) -> str:
        match var_name:
            case "sleep":
                return "s"
            case _:
                raise ValueError(f"Unknown variable {var_name}")

    def set_value(self, var_name: str, src: np.ndarray) -> None:
        match var_name:
            case "sleep":
                self.sleepiness = src[0]
            case _:
                raise ValueError(f"Cannot set value of var {var_name}")

    def get_output_var_names(self) -> Tuple[str]:
        return ("discharge",)

    def get_start_time(self) -> float:
        """Return end time in seconds since 1 january 1970."""
        return get_unixtime(self.start_time) # type: ignore

    def get_end_time(self) -> float:
        """Return end time in seconds since 1 january 1970."""
        return get_unixtime(self.end_timestep) # type: ignore
