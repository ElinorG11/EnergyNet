from entities.device import Device
from typing import Any
from defs import ProducerState, ProduceAction
from gymnasium.spaces import Box
from env.config import MIN_POWER, MIN_PRODUCTION, MAX_ELECTRIC_POWER
import numpy as np

class PrivateProducer(Device):
    """Base producer class.

    Parameters
    ----------
    max_produce : float, default: 0.0
        producer output power in [kW]. Must be >= 0.
    efficiency : float, default: 1.0
    
    Other Parameters
    ----------------
    **kwargs : Any
        Other keyword arguments used to initialize super class.
    """
    
    def __init__(self, max_produce: float = None, efficiency: float = None, **kwargs: Any):
        super().__init__(efficiency, **kwargs)
        self.max_produce = max_produce
        self.init_max_produce = self.max_produce
        self.action_type = ProduceAction
        self.production = MIN_PRODUCTION

    @property
    def current_state(self) -> ProducerState:
        return ProducerState(max_produce=self.max_produce, production=self.production)

    @property
    def max_produce(self):
        return self._max_produce
    
    @max_produce.setter
    def max_produce(self, max_produce: float):
        assert max_produce >= MIN_POWER, 'max_produce must be >= MIN_POWER.'
        self._max_produce = max_produce



    @property
    def production(self):
        return self._production
    
    @production.setter
    def production(self, production: float):
        assert MIN_PRODUCTION <= production <= self.max_produce, 'production must be in [MIN_PRODUCTION, MAX_PRODUCTION].'
        self._production = production


    def get_current_state(self) -> ProducerState:
        return self.current_state
    
    def update_state(self, state: ProducerState):
        self.max_produce = state.max_produce
        self.production = state.production
        
    
    def get_reward(self):
        return 0
    
    def reset(self):
        super().reset()
        self.max_produce = self.init_max_produce
        return self.get_current_state()

    def get_action_space(self) -> Box:
        return Box(low=MIN_POWER, high=self.max_produce, shape=(1,), dtype=float)

    def get_observation_space(self) -> Box :
        # Define the lower and upper bounds for each dimension of the observation space
        low = np.array([MIN_POWER, MIN_POWER])  # Example lower bounds
        high = np.array([self.max_produce, MAX_ELECTRIC_POWER])  # Example upper bounds
        return Box(low=low, high=high, dtype=np.float32)


    
    


