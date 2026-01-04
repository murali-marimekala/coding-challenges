"""
Algorithm Mastery Platform - Main Streamlit Application
Tier 1: Core Learning Foundation with Worked Examples
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from algorithms.two_sum.solution import TwoSumSolver, EASY_EXAMPLES, MEDIUM_EXAMPLES, HARD_EXAMPLES
from utils.config_loader import get_config_loader
from utils.variable_tracker import VariableTracker
from components.worked_example_player import WorkedExamplePlayer, WorkedExample
from components.playback_controller import PlaybackController
from components.variable_tracker_ui import VariableTrackerUI, HashMapVisualizer


# Page configuration
st.set_page_config(
    page_title="Algorithm Mastery - Two Sum",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'current_difficulty' not in st.session_state:
        st.session_state.current_difficulty = 'Easy'
    if 'current_example_idx' not in st.session_state:
        st.session_state.current_example_idx = 0
    if 'playback_step' not in st.session_state:
        st.session_state.playback_step = 0
    if 'playback_playing' not in st.session_state:
        st.session_state.playback_playing = False
    if 'playback_speed' not in st.session_state:
        st.session_state.playback_speed = 1.0


def get_examples_for_difficulty(difficulty: str):
    """Get examples for selected difficulty"""
    examples_map = {
        'Easy': EASY_EXAMPLES,
        'Medium': MEDIUM_EXAMPLES,
        'Hard': HARD_EXAMPLES
    }
    return examples_map.get(difficulty, EASY_EXAMPLES)


def render_difficulty_tabs():
    """Render difficulty selection tabs"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟢 Easy", use_container_width=True, 
                    key="btn_easy",
                    type="primary" if st.session_state.current_difficulty == 'Easy' else "secondary"):
            st.session_state.current_difficulty = 'Easy'
            st.session_state.current_example_idx = 0
            st.rerun()
    
    with col2:
        if st.button("🟡 Medium", use_container_width=True,
                    key="btn_medium",
                    type="primary" if st.session_state.current_difficulty == 'Medium' else "secondary"):
            st.session_state.current_difficulty = 'Medium'
            st.session_state.current_example_idx = 0
            st.rerun()
    
    with col3:
        if st.button("🔴 Hard", use_container_width=True,
                    key="btn_hard",
                    type="primary" if st.session_state.current_difficulty == 'Hard' else "secondary"):
            st.session_state.current_difficulty = 'Hard'
            st.session_state.current_example_idx = 0
            st.rerun()


def render_worked_example(example_data: dict, difficulty: str):
    """Render a single worked example with full interactivity"""
    
    st.subheader(f"📚 Worked Example - {difficulty} Level")
    st.divider()
    
    # Execute algorithm with step tracking
    steps, final_map = TwoSumSolver.solve_with_steps(
        example_data['array'],
        example_data['target']
    )
    
    if not steps:
        st.error("No solution found!")
        return
    
    # Problem Overview (Expandable)
    with st.expander("📋 Problem Overview", expanded=True):
        st.markdown(f"**Scenario:** {example_data['explanation']}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Input Array", str(example_data['array']))
        with col2:
            st.metric("Target Sum", example_data['target'])
        with col3:
            st.metric("Expected Output", str(example_data['expected']))
    
    # Algorithm Code with Controls (Expandable)
    with st.expander("💻 Algorithm Code", expanded=True):
        st.subheader("Python Implementation")
        code = '''def twoSum(nums: List[int], target: int) -> List[int]:
    """
    Find two numbers that add up to target
    Time: O(n) | Space: O(n)
    """
    complement_map = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in complement_map:
            return [complement_map[complement], i]
        
        complement_map[num] = i
    
    return []'''
        st.code(code, language="python")
        
        # Playback controls under code
        st.markdown("**Playback Controls:**")
        playback = PlaybackController(total_steps=len(steps))
        playback.render_controls()
    
    # Current Step Analysis (Expandable)
    with st.expander("📍 Current Step Analysis", expanded=True):
        current_step_idx = min(st.session_state.playback_step, len(steps) - 1)
        current_step = steps[current_step_idx]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Step", f"{current_step_idx + 1}/{len(steps)}")
        with col2:
            st.metric("Current Number", current_step['current_number'])
        with col3:
            st.metric("Complement Needed", current_step['complement_needed'])
        with col4:
            status = "✅ FOUND!" if current_step['found'] else "❌ Not found"
            st.write(f"**Status:** {status}")
    
    # Hash Map Evolution (Expandable)
    with st.expander("🗺️ Hash Map Evolution", expanded=True):
        current_step_idx = min(st.session_state.playback_step, len(steps) - 1)
        current_step = steps[current_step_idx]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Before this step:**")
            HashMapVisualizer.render_hash_map(current_step['map_before'], None, None)
        
        with col2:
            st.write("**After this step:**")
            HashMapVisualizer.render_hash_map(
                current_step['map_after'],
                current_step['current_number'] if not current_step['found'] else None,
                current_step['complement_needed'] if current_step['found'] else None
            )
    
    # Array Visualization (Expandable)
    with st.expander("📊 Array Pointer", expanded=True):
        current_step_idx = min(st.session_state.playback_step, len(steps) - 1)
        current_step = steps[current_step_idx]
        HashMapVisualizer.render_array_with_pointer(example_data['array'], current_step['current_index'])
    
    # Step Explanation (Expandable)
    with st.expander("📖 Step Explanation", expanded=True):
        current_step_idx = min(st.session_state.playback_step, len(steps) - 1)
        current_step = steps[current_step_idx]
        for line in example_data['step_explanations']:
            st.write(line)
        
        # Solution found
        if current_step['found']:
            st.divider()
            st.success(f"✅ Solution Found! Indices: {current_step['result']}")


def render_sidebar():
    """Render sidebar with navigation and learning resources"""
    st.sidebar.title("🎯 Algorithm Mastery")
    
    st.sidebar.divider()
    
    # Learning objectives
    st.sidebar.subheader("📚 Learning Objectives")
    objectives = [
        "Understand hash table usage",
        "Master complement pattern",
        "Optimize from O(n²) to O(n)",
        "Recognize similar problems"
    ]
    for obj in objectives:
        st.sidebar.write(f"• {obj}")
    
    st.sidebar.divider()
    
    # Complexity info
    st.sidebar.subheader("⚡ Complexity Analysis")
    st.sidebar.info("""
    **Optimal Solution (Hash Map):**
    - Time: O(n)
    - Space: O(n)
    
    **Brute Force:**
    - Time: O(n²)
    - Space: O(1)
    """)
    
    st.sidebar.divider()
    
    # Resources
    st.sidebar.subheader("🔗 Resources")
    st.sidebar.markdown("""
    - [LeetCode Problem](https://leetcode.com/problems/two-sum/)
    - [Hash Table Concepts](https://en.wikipedia.org/wiki/Hash_table)
    - [Algorithm Patterns](https://github.com/)
    """)


def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.title("🎯 Algorithm Mastery Platform")
    st.markdown("**Learn difficult algorithms through interactive worked examples**")
    st.divider()
    
    # Main content
    col_main, col_sidebar = st.columns([4, 1])
    
    with col_main:
        # Algorithm selection
        st.subheader("Two Sum")
        st.markdown("""
        **Problem:** Given an array of integers `nums` and an integer `target`, return the **indices** 
        of the two numbers that add up to target. You may assume each input has exactly one solution, 
        and you cannot use the same element twice.
        """)
        
        st.divider()
        
        # Difficulty selection
        st.subheader("🎚️ Select Difficulty Level")
        render_difficulty_tabs()
        
        st.divider()
        
        # Get examples for current difficulty
        examples = get_examples_for_difficulty(st.session_state.current_difficulty)
        
        # Example navigation
        if len(examples) > 1:
            st.subheader(f"📂 Examples ({st.session_state.current_example_idx + 1}/{len(examples)})")
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.session_state.current_example_idx > 0:
                    if st.button("⬅️ Previous", use_container_width=True):
                        st.session_state.current_example_idx -= 1
                        st.rerun()
            
            with col3:
                if st.session_state.current_example_idx < len(examples) - 1:
                    if st.button("Next ➡️", use_container_width=True):
                        st.session_state.current_example_idx += 1
                        st.rerun()
            
            st.divider()
        
        # Render current example
        current_example = examples[st.session_state.current_example_idx]
        render_worked_example(
            current_example,
            st.session_state.current_difficulty
        )
    
    with col_sidebar:
        render_sidebar()


if __name__ == "__main__":
    main()
