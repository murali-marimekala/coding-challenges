"""
Variable tracking for algorithm execution
Captures variable states at each step for visualization
"""

from typing import Any, Dict, List, Tuple
from dataclasses import dataclass, asdict
import copy


@dataclass
class VariableState:
    """Represents the state of all variables at a specific step"""
    step_number: int
    line_number: int
    variables: Dict[str, Any]
    timestamp: float = 0.0
    
    def to_dict(self):
        return asdict(self)


class VariableTracker:
    """Track variable states throughout algorithm execution"""
    
    def __init__(self):
        self.states: List[VariableState] = []
        self.current_step = 0
        self.variable_history = {}
    
    def record_state(self, step: int, line: int, variables: Dict[str, Any]):
        """Record variable state at current step"""
        # Deep copy to avoid reference issues
        var_copy = {}
        for key, value in variables.items():
            try:
                var_copy[key] = copy.deepcopy(value)
            except:
                var_copy[key] = str(value)
        
        state = VariableState(
            step_number=step,
            line_number=line,
            variables=var_copy
        )
        self.states.append(state)
        self.current_step = step
        self._update_history(key, value)
    
    def _update_history(self, var_name: str, value: Any):
        """Update variable history for tracking changes"""
        if var_name not in self.variable_history:
            self.variable_history[var_name] = []
        self.variable_history[var_name].append({
            'step': self.current_step,
            'value': copy.deepcopy(value) if hasattr(value, '__copy__') else value
        })
    
    def get_state(self, step: int = None) -> VariableState:
        """Get variable state at specific step"""
        if step is None:
            step = self.current_step
        
        for state in self.states:
            if state.step_number == step:
                return state
        return None
    
    def get_states(self) -> List[VariableState]:
        """Get all recorded states"""
        return self.states
    
    def get_variable_change(self, var_name: str, step: int) -> Tuple[Any, Any]:
        """Get variable value before and after a step"""
        if step == 0:
            return None, self._get_variable_at_step(var_name, 0)
        
        before = self._get_variable_at_step(var_name, step - 1)
        after = self._get_variable_at_step(var_name, step)
        return before, after
    
    def _get_variable_at_step(self, var_name: str, step: int) -> Any:
        """Get specific variable value at a step"""
        state = self.get_state(step)
        if state and var_name in state.variables:
            return state.variables[var_name]
        return None
    
    def get_variables_at_step(self, step: int) -> Dict[str, Any]:
        """Get all variables at specific step"""
        state = self.get_state(step)
        return state.variables if state else {}
    
    def clear(self):
        """Clear all recorded states"""
        self.states = []
        self.current_step = 0
        self.variable_history = {}
    
    def get_total_steps(self) -> int:
        """Get total number of steps recorded"""
        return len(self.states)
