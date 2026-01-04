"""
Variable Tracker UI Component - Visualizes variable states and changes
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List
from utils.variable_tracker import VariableTracker


class VariableTrackerUI:
    """Renders variable state visualization in Streamlit"""
    
    def __init__(self, tracker: VariableTracker):
        self.tracker = tracker
    
    def render_variable_panel(self, current_step: int = None):
        """Render current variable states"""
        if self.tracker.get_total_steps() == 0:
            st.info("No execution data yet")
            return
        
        if current_step is None:
            current_step = self.tracker.get_total_steps() - 1
        
        current_state = self.tracker.get_state(current_step)
        
        if current_state is None:
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📍 Current State")
            for var_name, var_value in current_state.variables.items():
                if isinstance(var_value, dict):
                    st.write(f"**{var_name}:** `{var_value}`")
                elif isinstance(var_value, list):
                    st.write(f"**{var_name}:** `{var_value}`")
                else:
                    st.write(f"**{var_name}:** `{var_value}`")
        
        with col2:
            st.subheader("🔄 Variable History")
            # Show history of key variables
            for var_name in ['complement_map', 'complement', 'num']:
                if var_name in current_state.variables:
                    try:
                        history = self._get_variable_history(var_name)
                        with st.expander(f"History of {var_name}"):
                            st.text("\n".join(history))
                    except:
                        pass
    
    def _get_variable_history(self, var_name: str) -> List[str]:
        """Get history of a variable across all steps"""
        history = []
        for step in range(self.tracker.get_total_steps()):
            state = self.tracker.get_state(step)
            if state and var_name in state.variables:
                value = state.variables[var_name]
                history.append(f"Step {step + 1}: {value}")
        return history
    
    def render_comparison_table(self):
        """Render before/after comparison for current and next step"""
        if self.tracker.get_total_steps() < 2:
            return
        
        st.subheader("📊 Step Comparison")
        
        # Create comparison data
        steps_data = []
        for step in range(self.tracker.get_total_steps()):
            state = self.tracker.get_state(step)
            if state:
                steps_data.append({
                    'Step': step + 1,
                    'Line': state.line_number,
                    **{f"{k}": str(v) for k, v in state.variables.items() if k not in ['nums', 'array']}
                })
        
        if steps_data:
            df = pd.DataFrame(steps_data)
            st.dataframe(df, use_container_width=True)
    
    def render_variable_timeline(self):
        """Render timeline of variable changes"""
        st.subheader("⏱️ Variable Timeline")
        
        # Track specific variables we care about
        tracked_vars = ['i', 'num', 'complement', 'complement_map']
        
        timeline_data = []
        for step in range(self.tracker.get_total_steps()):
            state = self.tracker.get_state(step)
            if state:
                row = {'Step': step + 1}
                for var_name in tracked_vars:
                    if var_name in state.variables:
                        value = state.variables[var_name]
                        # Format for readability
                        if isinstance(value, dict):
                            row[var_name] = f"size={len(value)}"
                        elif isinstance(value, list):
                            row[var_name] = f"len={len(value)}"
                        else:
                            row[var_name] = value
                timeline_data.append(row)
        
        if timeline_data:
            df = pd.DataFrame(timeline_data)
            st.dataframe(df, use_container_width=True)


class HashMapVisualizer:
    """Specialized visualizer for hash map (complement_map)"""
    
    @staticmethod
    def render_hash_map(hash_map: Dict[int, int], current_number: int = None, complement: int = None):
        """Render visual representation of hash map"""
        st.subheader("🗺️ Hash Map State")
        
        if not hash_map:
            st.info("Hash map is empty")
            return
        
        # Create two-column layout for key-value pairs
        col1, col2 = st.columns(2)
        
        for i, (key, value) in enumerate(hash_map.items()):
            with (col1 if i % 2 == 0 else col2):
                # Highlight current items
                highlight = ""
                if key == current_number:
                    highlight = " 👈 current"
                elif key == complement:
                    highlight = " ✅ target found!"
                
                st.write(f"**{key}** → index `{value}`{highlight}")
    
    @staticmethod
    def render_array_with_pointer(array: List[int], current_index: int = None):
        """Render array with position pointer"""
        st.subheader("📋 Input Array")
        
        # Create visual representation
        visual = ""
        for i, num in enumerate(array):
            if i == current_index:
                visual += f"👉 **{num}** | "
            else:
                visual += f"{num} | "
        
        st.code(f"[{visual.rstrip('| ')}]", language="")
