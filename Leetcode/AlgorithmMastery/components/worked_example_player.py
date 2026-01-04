"""
Worked Example Player Component
Guides learners through step-by-step algorithm execution with narration
"""

import streamlit as st
from typing import List, Dict, Any, Callable
from dataclasses import dataclass


@dataclass
class WorkedExample:
    """Represents a worked example for an algorithm"""
    title: str
    input_array: list
    target: int
    expected_output: list
    explanation: str
    steps_explanation: List[str]  # Explanation for each step


class WorkedExamplePlayer:
    """Interactive player for worked examples"""
    
    def __init__(self, example: WorkedExample, execution_func: Callable):
        """
        Initialize player
        
        Args:
            example: WorkedExample object
            execution_func: Function that generates step-by-step execution data
        """
        self.example = example
        self.execution_func = execution_func
        self.steps = []
        self.total_steps = 0
        
        # Generate steps
        self._generate_steps()
    
    def _generate_steps(self):
        """Generate step-by-step execution"""
        self.steps, _ = self.execution_func(self.example.input_array, self.example.target)
        self.total_steps = len(self.steps)
    
    def render(self, allow_user_control: bool = False):
        """
        Render the worked example player
        
        Args:
            allow_user_control: Whether to show play/pause controls
        """
        # Title and explanation
        st.markdown(f"### 📚 {self.example.title}")
        st.markdown(f"**Problem:** Find two numbers in `{self.example.input_array}` that sum to `{self.example.target}`")
        st.markdown(f"**Expected Output:** `{self.example.expected_output}`")
        st.info(self.example.explanation)
        
        # Initialize session state for playback
        if 'example_step' not in st.session_state:
            st.session_state.example_step = 0
        if 'example_playing' not in st.session_state:
            st.session_state.example_playing = False
        
        # Controls
        if allow_user_control:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("▶️ Play", use_container_width=True):
                    st.session_state.example_playing = True
            
            with col2:
                if st.button("⏸️ Pause", use_container_width=True):
                    st.session_state.example_playing = False
            
            with col3:
                if st.button("⬅️ Prev", disabled=st.session_state.example_step == 0, use_container_width=True):
                    st.session_state.example_step -= 1
            
            with col4:
                if st.button("Next ➡️", disabled=st.session_state.example_step >= self.total_steps - 1, use_container_width=True):
                    st.session_state.example_step += 1
        
        # Progress indicator
        if self.total_steps > 0:
            progress = (st.session_state.example_step + 1) / self.total_steps
            st.progress(progress)
            st.caption(f"Step {st.session_state.example_step + 1}/{self.total_steps}")
        
        # Display current step
        if st.session_state.example_step < self.total_steps:
            self._render_step(st.session_state.example_step)
    
    def _render_step(self, step_index: int):
        """Render specific step"""
        if step_index >= len(self.steps):
            return
        
        step = self.steps[step_index]
        
        # Step explanation
        if step_index < len(self.example.steps_explanation):
            st.markdown(f"**Step {step_index + 1}:** {self.example.steps_explanation[step_index]}")
        
        # Key information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Number", step.get('current_number', 'N/A'))
        
        with col2:
            st.metric("Index", step.get('current_index', 'N/A'))
        
        with col3:
            st.metric("Complement Needed", step.get('complement_needed', 'N/A'))
        
        # Hash map state
        st.markdown("**Hash Map State:**")
        map_state = step.get('map_after', {})
        if map_state:
            st.code(str(map_state), language='python')
        else:
            st.code("{}", language='python')
        
        # Result if found
        if step.get('found'):
            st.success(f"✅ **Found!** Indices: {step.get('result')}")


class WorkedExampleBuilder:
    """Helper to build worked examples from test cases"""
    
    @staticmethod
    def from_config(test_case: Dict[str, Any], difficulty: str = "easy") -> WorkedExample:
        """Create worked example from config test case"""
        
        explanations = {
            'easy': {
                [2, 7, 11, 15]: "This is a straightforward case where we look for two numbers summing to the target.",
                [3, 2, 4]: "This demonstrates the algorithm finding a solution in the middle of the array.",
            }
        }
        
        step_explanations = [
            "Initialize empty hash map",
            "Look at first number, calculate complement, not found → add to map",
            "Look at second number, calculate complement, found in map! Return indices.",
        ]
        
        return WorkedExample(
            title=f"Example: {test_case['array']} → target {test_case['target']}",
            input_array=test_case['array'],
            target=test_case['target'],
            expected_output=test_case.get('expected', []),
            explanation=test_case.get('explanation', ''),
            steps_explanation=step_explanations
        )
