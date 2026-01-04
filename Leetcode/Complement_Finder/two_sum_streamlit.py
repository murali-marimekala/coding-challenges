import streamlit as st
import pandas as pd
from typing import List, Tuple
import random
import plotly.graph_objects as go
import plotly.express as px
import time

st.set_page_config(page_title="Two Sum Solver - Step by Step", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for professional styling - minimize top spacing
st.markdown("""
<style>
    .stApp {
        margin-top: -6rem;
        padding-top: 0;
    }
    .stApp > header {
        display: none;
    }
    h1, h2, h3 {
        margin-top: -0.5rem !important;
        margin-bottom: 0.3rem !important;
    }
    .stContainer {
        padding-top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .code-container {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 20px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        line-height: 1.6;
        overflow-x: auto;
    }
    .scrollable-container {
        height: 700px;
        overflow-y: auto;
        padding: 0;
        border-radius: 8px;
    }
    .scrollable-container::-webkit-scrollbar {
        width: 8px;
    }
    .scrollable-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 8px;
    }
    .scrollable-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 8px;
    }
    .scrollable-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    .code-line {
        display: flex;
        padding: 4px 0;
    }
    .line-number {
        min-width: 40px;
        color: #858585;
        margin-right: 15px;
        text-align: right;
        user-select: none;
    }
    .code-content {
        flex: 1;
        color: #d4d4d4;
    }
    .cursor-line {
        background-color: #264f78;
        border-left: 3px solid #4fc3f7;
    }
    .cursor-indicator {
        color: #4fc3f7;
        font-weight: bold;
    }
    .keyword {
        color: #569cd6;
    }
    .string {
        color: #ce9178;
    }
    .function {
        color: #dcdcaa;
    }
    .number {
        color: #b5cea8;
    }
    .explanation-box {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 12px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 13px;
        line-height: 1.6;
    }
    .complexity-badge {
        display: inline-block;
        background-color: #fff3e0;
        border: 1px solid #ffb74d;
        padding: 4px 8px;
        border-radius: 4px;
        font-family: monospace;
        font-size: 11px;
        margin-left: 6px;
    }
    .formula-box {
        background-color: #f5f5f5;
        border: 1px solid #ddd;
        padding: 12px;
        border-radius: 4px;
        font-family: monospace;
        margin: 8px 0;
        text-align: center;
        font-size: 15px;
    }
    .value-highlight {
        font-weight: bold;
        padding: 2px 6px;
        border-radius: 3px;
        margin: 0 4px;
    }
    .target-color { background-color: #e8f5e9; color: #1b5e20; }
    .current-color { background-color: #fce4ec; color: #880e4f; }
    .complement-color { background-color: #e0f2f1; color: #004d40; }
    .flow-box {
        background-color: #f3e5f5;
        border: 1px solid #ce93d8;
        padding: 10px;
        border-radius: 4px;
        margin: 6px 0;
        font-size: 12px;
        line-height: 1.5;
    }
    .space-speed-box {
        display: flex;
        gap: 15px;
        padding: 10px;
        background-color: #f1f8e9;
        border: 1px solid #a1d82f;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 13px;
    }
    .space-speed-item {
        flex: 1;
        text-align: center;
    }
    .space-speed-item strong {
        display: block;
        color: #558b2f;
        margin-bottom: 4px;
    }
    /* Animation Styles */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    @keyframes highlight {
        0% { background-color: #ffeb3b; }
        50% { background-color: #ffeb3b; }
        100% { background-color: transparent; }
    }
    @keyframes matchFound {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    .variable-update {
        animation: highlight 1s ease-in-out;
        background-color: #fff9c4;
    }
    .array-item-current {
        animation: pulse 0.8s infinite;
    }
    .hashmap-item-new {
        animation: slideIn 0.6s ease-out;
    }
    .match-found-animation {
        animation: matchFound 0.6s ease-out;
        color: #4caf50;
        font-weight: bold;
    }
    .step-progress {
        animation: slideIn 0.4s ease-out;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🎯 Two Sum - Interactive Debugger")

def twoSum_with_steps(nums: List[int], target: int):
    """
    Generate step-by-step execution data with variable tracking
    Returns list of steps with detailed information including variable values
    """
    steps = []
    complement_map = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        found = complement in complement_map
        
        step_info = {
            'step_number': i + 1,
            'current_number': num,
            'current_index': i,
            'complement_needed': complement,
            'found': found,
            'found_at_index': complement_map.get(complement, None) if found else None,
            'map_before': complement_map.copy(),
            'map_after': complement_map.copy(),
            'code_line': 4,
            # Variable tracking
            'variables': {
                'i': i,
                'num': num,
                'target': target,
                'complement': complement,
                'complement_map': complement_map.copy(),
                'nums': nums
            }
        }
        
        if found:
            step_info['result'] = [complement_map[complement], i]
            step_info['result_values'] = [nums[complement_map[complement]], num]
            steps.append(step_info)
            break
        
        complement_map[num] = i
        step_info['map_after'] = complement_map.copy()
        step_info['variables']['complement_map'] = complement_map.copy()
        steps.append(step_info)
    
    return steps, complement_map if not steps or not steps[-1].get('found') else None

def get_step_explanation(step, depth="Simple"):
    """Generate explanation for current step based on depth setting"""
    if step.get('found'):
        if depth == "Simple":
            return "✅ Found! The complement exists in our hash map. Return the indices."
        else:
            return f"✅ **Found complement!** The value {step['complement_needed']} (complement of {step['current_number']}) exists at index {step['found_at_index']} in our hash map. Time: O(1). Return indices [{step['found_at_index']}, {step['current_index']}]."
    else:
        if depth == "Simple":
            return f"🔍 Complement not found. Add current number to hash map for future lookups."
        else:
            return f"🔍 **Searching...** Complement {step['complement_needed']} not found in map. Add {step['current_number']} at index {step['current_index']} to the hash map. Time: O(1) insertion. Continue to next iteration."

def get_flow_diagram(step):
    """Generate visual execution flow diagram"""
    found = "✅ YES" if step['found'] else "❌ NO"
    return f"""
    <div class="flow-box">
    <strong>Check: Is {step['complement_needed']} in hash map?</strong><br>
    ↓<br>
    {found}<br>
    {('→ Return [' + str(step['found_at_index']) + ', ' + str(step['current_index']) + ']') if step['found'] else ('→ Add ' + str(step['current_number']) + ' to map → Continue')}
    </div>
    """

def get_space_speed_info(step, total_elements):
    """Display space vs speed trade-off"""
    stored = len(step['map_after'])
    return f"""
    <div class="space-speed-box">
    <div class="space-speed-item">
        <strong>Elements Stored</strong>
        {stored}
    </div>
    <div class="space-speed-item">
        <strong>Iterations Done</strong>
        {step['current_index'] + 1}
    </div>
    <div class="space-speed-item">
        <strong>Space Used</strong>
        O(n)
    </div>
    <div class="space-speed-item">
        <strong>Time Saved</strong>
        O(1) lookups
    </div>
    </div>
    """

def format_variable_value(value):
    """Format variable values for display"""
    if isinstance(value, dict):
        if not value:
            return "{}"
        return str(value)
    elif isinstance(value, list):
        return str(value)
    else:
        return str(value)

def create_animated_hashmap(map_state: dict, step_number: int, found: bool = False):
    """Create animated Plotly visualization of hash map state"""
    if not map_state:
        fig = go.Figure()
        fig.add_annotation(text="Hash Map Empty", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=20))
        fig.update_layout(height=300, showlegend=False, margin=dict(l=0, r=0, t=20, b=0))
        return fig
    
    indices = list(map_state.keys())
    positions = list(map_state.values())
    colors = ['#2ecc71' if found and pos == positions[-1] else '#3498db' for pos in positions]
    
    fig = go.Figure(data=[
        go.Scatter(
            x=indices,
            y=positions,
            mode='markers+text',
            marker=dict(size=30, color=colors, line=dict(color='#2c3e50', width=2)),
            text=[f'Idx:{p}' for p in positions],
            textposition="top center",
            hovertemplate='<b>Number: %{x}</b><br>Index: %{y}<extra></extra>',
            showlegend=False
        )
    ])
    
    fig.update_layout(
        title=f"Hash Map State (Step {step_number})" + (" ✅ Match Found!" if found else ""),
        xaxis_title="Value",
        yaxis_title="Original Index",
        height=300,
        template="plotly_white",
        margin=dict(l=50, r=50, t=60, b=50),
        hovermode='closest'
    )
    
    return fig

def create_array_pointer_visualization(nums: List[int], current_index: int, complement: int = None):
    """Create visualization of array iteration with pointer"""
    colors = []
    for i, num in enumerate(nums):
        if i == current_index:
            colors.append('#e74c3c')  # Red for current
        elif complement is not None and num == complement:
            colors.append('#f39c12')  # Orange for complement
        else:
            colors.append('#95a5a6')  # Gray for others
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(range(len(nums))),
            y=nums,
            marker=dict(color=colors, line=dict(color='#2c3e50', width=2)),
            text=[f'{num}' for num in nums],
            textposition='outside',
            hovertemplate='Index: %{x}<br>Value: %{y}<extra></extra>',
            showlegend=False
        )
    ])
    
    fig.update_layout(
        title=f"Array Visualization (Processing Index {current_index})",
        xaxis_title="Index",
        yaxis_title="Value",
        height=300,
        template="plotly_white",
        margin=dict(l=50, r=50, t=60, b=50),
        showlegend=False,
        xaxis=dict(tickmode='linear', tick0=0, dtick=1)
    )
    
    return fig

def create_step_progress_animation(current_step: int, total_steps: int):
    """Create animated progress bar for step navigation"""
    progress = current_step / max(total_steps, 1)
    return progress

def animate_variable_change(old_value, new_value, var_name: str):
    """Return CSS class for animating variable changes"""
    if old_value != new_value:
        return "variable-update"
    return ""

def display_variables_watch(variables):
    """Display variables watch panel using Streamlit components"""
    # Create columns for the watch panel
    col1, col2, col3 = st.columns([40, 20, 40])
    
    with col1:
        st.markdown("**Variable Name**")
    with col2:
        st.markdown("**Type**")
    with col3:
        st.markdown("**Value**")
    
    st.divider()
    
    # Display each variable
    var_order = ['i', 'num', 'target', 'complement', 'complement_map', 'nums']
    
    for var_name in var_order:
        if var_name in variables:
            value = variables[var_name]
            
            col1, col2, col3 = st.columns([40, 20, 40])
            
            with col1:
                st.code(var_name, language="python")
            with col2:
                type_name = type(value).__name__
                st.caption(type_name)
            with col3:
                st.code(format_variable_value(value), language="python")

def get_algorithm_code(language="Python"):
    """Get algorithm code in different programming languages"""
    if language == "Python":
        return [
            "def twoSum(nums, target):",
            "    complement_map = {}",
            "    ",
            "    for i, num in enumerate(nums):",
            "        complement = target - num",
            "        if complement in complement_map:",
            "            return [complement_map[complement], i]",
            "        complement_map[num] = i",
            "    ",
            "    return []"
        ]
    elif language == "C":
        return [
            "int* twoSum(int* nums, int numsSize, int target, int* returnSize) {",
            "    int* result = (int*)malloc(2 * sizeof(int));",
            "    *returnSize = 0;",
            "    ",
            "    for (int i = 0; i < numsSize; i++) {",
            "        for (int j = i + 1; j < numsSize; j++) {",
            "            if (nums[i] + nums[j] == target) {",
            "                result[0] = i;",
            "                result[1] = j;",
            "                *returnSize = 2;",
            "                return result;",
            "            }",
            "        }",
            "    }",
            "    return result;",
            "}"
        ]
    elif language == "C++":
        return [
            "vector<int> twoSum(vector<int>& nums, int target) {",
            "    unordered_map<int, int> complement_map;",
            "    ",
            "    for (int i = 0; i < nums.size(); i++) {",
            "        int complement = target - nums[i];",
            "        if (complement_map.find(complement) != complement_map.end()) {",
            "            return {complement_map[complement], i};",
            "        }",
            "        complement_map[nums[i]] = i;",
            "    }",
            "    return {};",
            "}"
        ]
    return []

def display_algorithm_code(current_step=None, language="Python"):
    """Display the algorithm code with cursor highlighting"""
    code_lines = get_algorithm_code(language)
    
    html_code = '<div class="code-container">'
    
    for idx, line in enumerate(code_lines, 1):
        is_cursor_line = (current_step is not None and idx == current_step)
        line_class = "code-line cursor-line" if is_cursor_line else "code-line"
        
        cursor = '<span class="cursor-indicator">▶</span> ' if is_cursor_line else '  '
        
        html_code += f'<div class="{line_class}">'
        html_code += f'<span class="line-number">{idx}</span>'
        html_code += f'<span class="cursor-indicator">{cursor}</span>'
        
        # Syntax highlighting
        highlighted_line = line
        if language == "Python":
            highlighted_line = highlighted_line.replace('def', '<span class="keyword">def</span>')
            highlighted_line = highlighted_line.replace('in', '<span class="keyword">in</span>')
            highlighted_line = highlighted_line.replace('if', '<span class="keyword">if</span>')
            highlighted_line = highlighted_line.replace('for', '<span class="keyword">for</span>')
            highlighted_line = highlighted_line.replace('return', '<span class="keyword">return</span>')
            highlighted_line = highlighted_line.replace('enumerate', '<span class="function">enumerate</span>')
            highlighted_line = highlighted_line.replace('complement_map', '<span class="function">complement_map</span>')
        elif language == "C" or language == "C++":
            highlighted_line = highlighted_line.replace('int', '<span class="keyword">int</span>')
            highlighted_line = highlighted_line.replace('if', '<span class="keyword">if</span>')
            highlighted_line = highlighted_line.replace('for', '<span class="keyword">for</span>')
            highlighted_line = highlighted_line.replace('return', '<span class="keyword">return</span>')
            highlighted_line = highlighted_line.replace('void', '<span class="keyword">void</span>')
            if language == "C++":
                highlighted_line = highlighted_line.replace('vector', '<span class="keyword">vector</span>')
                highlighted_line = highlighted_line.replace('unordered_map', '<span class="keyword">unordered_map</span>')
        
        html_code += f'<span class="code-content">{highlighted_line}</span>'
        html_code += '</div>'
    
    html_code += '</div>'
    return html_code

import random

# ==================== TOP CONFIGURATION BAR ====================
config_col1, config_col2, config_col3, config_col4, config_col5 = st.columns([2, 2, 1.5, 1.5, 0.8], gap="small")

# Initialize auto-generated values if they exist
if 'auto_nums' not in st.session_state:
    st.session_state.auto_nums = None
if 'auto_target' not in st.session_state:
    st.session_state.auto_target = None
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Apply dark mode CSS directly based on session state
if st.session_state.dark_mode:
    dark_mode_css = """
    <style>
        body {
            background-color: #0e1117 !important;
            color: #e0e0e0 !important;
        }
        .stApp {
            background-color: #0e1117 !important;
            color: #e0e0e0 !important;
        }
        .code-container {
            background-color: #161b22 !important;
            color: #c9d1d9 !important;
        }
        .stExpander {
            background-color: #161b22 !important;
            border-color: #30363d !important;
        }
        .explanation-box {
            background-color: #1e3a5f !important;
            border-left-color: #58a6ff !important;
            color: #e0e0e0 !important;
        }
        .complexity-badge {
            background-color: #3d2817 !important;
            border-color: #d99e64 !important;
            color: #e0e0e0 !important;
        }
        .formula-box {
            background-color: #1c2128 !important;
            border-color: #30363d !important;
            color: #c9d1d9 !important;
        }
        .flow-box {
            background-color: #1c2128 !important;
            border-color: #30363d !important;
            color: #e0e0e0 !important;
        }
        .space-speed-box {
            background-color: #1c2128 !important;
            border-color: #30363d !important;
            color: #e0e0e0 !important;
        }
        .space-speed-item strong {
            color: #58a6ff !important;
        }
        .stMarkdown {
            color: #e0e0e0 !important;
        }
        input, select, textarea {
            background-color: #161b22 !important;
            color: #c9d1d9 !important;
            border-color: #30363d !important;
        }
        .stButton button {
            background-color: #161b22 !important;
            border-color: #30363d !important;
            color: #e0e0e0 !important;
        }
    </style>
    """
    st.markdown(dark_mode_css, unsafe_allow_html=True)

with config_col1:
    default_nums = "2, 7, 11, 15" if st.session_state.auto_nums is None else ", ".join(map(str, st.session_state.auto_nums))
    input_text = st.text_input("📝 Array:", value=default_nums, label_visibility="collapsed", placeholder="e.g., 2, 7, 11, 15")
    try:
        nums = [int(x.strip()) for x in input_text.split(",") if x.strip()]
    except ValueError:
        nums = []

with config_col2:
    default_target = 9 if st.session_state.auto_target is None else st.session_state.auto_target
    target = st.number_input("🎯 Target:", value=default_target, label_visibility="collapsed")

with config_col3:
    if st.button("🎲 Auto", use_container_width=True):
        # Generate random array and target
        st.session_state.auto_nums = [random.randint(1, 20) for _ in range(random.randint(3, 6))]
        st.session_state.auto_target = random.choice(st.session_state.auto_nums) + random.choice(st.session_state.auto_nums)
        st.session_state.current_step = 0
        st.rerun()

with config_col4:
    execution_mode = st.selectbox("Mode:", 
                                 ["Step by Step", "Show All Steps", "Skip to Result", "🎬 Auto-Play Animation"],
                                 label_visibility="collapsed")

with config_col5:
    theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    if st.button(theme_icon, help="Toggle dark/light mode", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==================== EXPLANATION & LEARNING CONTROLS ====================
st.markdown("---")

with st.expander("⚙️ Learning Settings", expanded=False):
    learn_col1, learn_col2, learn_col3 = st.columns(3, gap="large")
    
    with learn_col1:
        st.markdown("##### 📖 Explanation Depth")
        explanation_depth = st.radio("Explanation Depth", ["Simple", "Detailed"], horizontal=True, label_visibility="collapsed")
        if 'explanation_depth' not in st.session_state:
            st.session_state.explanation_depth = explanation_depth
        st.caption("Simple: 1-line summary | Detailed: Full analysis")
    
    with learn_col2:
        st.markdown("##### ⚡ Animation Speed")
        animation_speed = st.slider("Animation Speed", 500, 3000, 2000, 250, label_visibility="collapsed")
        if 'animation_speed' not in st.session_state:
            st.session_state.animation_speed = animation_speed
        st.caption(f"Current: {animation_speed}ms per frame")
    
    with learn_col3:
        st.markdown("##### 💻 Programming Language")
        language = st.radio("Language", ["Python", "C", "C++"], horizontal=True, label_visibility="collapsed")
        st.session_state.selected_language = language
        st.caption("View algorithm in different languages")
    
    st.markdown("---")
    st.markdown("##### 🧪 Edge Case Presets")
    edge_col1, edge_col2, edge_col3 = st.columns(3, gap="small")
    
    with edge_col1:
        if st.button("Duplicates", use_container_width=True, help="Test with duplicate numbers"):
            st.session_state.auto_nums = [1, 1, 2]
            st.session_state.auto_target = 2
            st.session_state.current_step = 0
            st.rerun()
    
    with edge_col2:
        if st.button("Negatives", use_container_width=True, help="Test with negative numbers"):
            st.session_state.auto_nums = [-2, 7, 11, 15]
            st.session_state.auto_target = 5
            st.session_state.current_step = 0
            st.rerun()
    
    with edge_col3:
        if st.button("Boundary", use_container_width=True, help="Test with target at edge"):
            st.session_state.auto_nums = [1, 2, 3]
            st.session_state.auto_target = 4
            st.session_state.current_step = 0
            st.rerun()

st.markdown("---")
# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'steps' not in st.session_state:
    st.session_state.steps = []
if 'last_nums' not in st.session_state:
    st.session_state.last_nums = None
if 'last_target' not in st.session_state:
    st.session_state.last_target = None
if 'explanation_depth' not in st.session_state:
    st.session_state.explanation_depth = "Simple"
if 'animation_speed' not in st.session_state:
    st.session_state.animation_speed = 2000
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "Python"

# Generate steps
if nums and target is not None:
    # Check if input changed by comparing current nums with last nums
    nums_changed = st.session_state.last_nums != nums or st.session_state.last_target != target
    
    if nums_changed:
        # Input changed - regenerate steps and reset
        st.session_state.steps, _ = twoSum_with_steps(nums, target)
        st.session_state.current_step = 0
        st.session_state.last_nums = nums
        st.session_state.last_target = target
    elif not st.session_state.steps:
        # First time - generate steps
        st.session_state.steps, _ = twoSum_with_steps(nums, target)
        st.session_state.last_nums = nums
        st.session_state.last_target = target
    
    total_steps = len(st.session_state.steps)
    
    # Ensure current_step is within bounds
    if st.session_state.current_step >= total_steps:
        st.session_state.current_step = max(0, total_steps - 1)
else:
    st.session_state.steps = []
    total_steps = 0
    st.session_state.current_step = 0

# Main content
if not nums:
    st.info("👈 Enter an array and target sum above!")
else:
    if execution_mode == "Step by Step":
        if st.session_state.steps and st.session_state.current_step < len(st.session_state.steps):
            step = st.session_state.steps[st.session_state.current_step]
            
            # Two Column Layout: Algorithm Code (Left/Wider) | Scrollable Execution State (Right/Narrower)
            col_code, col_state = st.columns([55, 45], gap="medium")
            
            # LEFT: Algorithm Code with cursor
            with col_code:
                # Algorithm Code - expandable
                with st.expander("📝 Algorithm Code", expanded=True):
                    # Determine which line is executing
                    # All iterations start at line 4 (for loop), then check line 6 (if), then line 7 (return) or line 8 (add to map)
                    cursor_line = step.get('code_line', 4)
                    st.markdown(display_algorithm_code(cursor_line, st.session_state.selected_language), unsafe_allow_html=True)
                
                # Navigation controls - compact and close to code
                nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([0.9, 0.9, 1.2, 0.9, 0.5], gap="small")
                with nav_col1:
                    if st.button("⬅️ Prev", disabled=st.session_state.current_step == 0, use_container_width=True):
                        st.session_state.current_step -= 1
                        st.rerun()
                with nav_col2:
                    if st.button("🔄 Reset", use_container_width=True):
                        st.session_state.current_step = 0
                        st.rerun()
                with nav_col3:
                    progress_percent = ((st.session_state.current_step + 1) / total_steps * 100) if total_steps > 0 else 0
                    st.caption(f"Step {st.session_state.current_step + 1}/{total_steps} ({progress_percent:.0f}%)")
                with nav_col4:
                    if st.button("Next ➡️", disabled=st.session_state.current_step >= total_steps - 1, use_container_width=True):
                        st.session_state.current_step += 1
                        st.rerun()
                with nav_col5:
                    st.empty()  # Spacer
                
                # Animated Visualizations
                st.markdown("**🎨 Live Visualization**")
                anim_col1, anim_col2 = st.columns(2, gap="large")
                
                with anim_col1:
                    st.markdown("**📊 Array Pointer**")
                    array_fig = create_array_pointer_visualization(nums, step['current_index'], step['complement_needed'])
                    st.plotly_chart(array_fig, use_container_width=True, config={'displayModeBar': False})
                
                with anim_col2:
                    st.markdown("**🗂️ Hash Map State**")
                    hashmap_fig = create_animated_hashmap(step['map_after'], step['step_number'], step['found'])
                    st.plotly_chart(hashmap_fig, use_container_width=True, config={'displayModeBar': False})
                
                # Step Analysis - collapsible
                with st.expander("📊 Step Analysis", expanded=True):
                    # Step Explanation
                    st.markdown("**📖 Explanation**")
                    explanation = get_step_explanation(step, st.session_state.explanation_depth)
                    st.markdown(f'<div class="explanation-box">{explanation}</div>', unsafe_allow_html=True)
                    
                    # Complement Calculation Visualization
                    st.markdown("**🔢 Complement Calculation**")
                    complement_html = f"""
                    <div class="formula-box">
                    target: <span class="value-highlight target-color">{step['variables']['target']}</span>
                    − 
                    current: <span class="value-highlight current-color">{step['current_number']}</span>
                    = 
                    complement: <span class="value-highlight complement-color">{step['complement_needed']}</span>
                    </div>
                    """
                    st.markdown(complement_html, unsafe_allow_html=True)
                    
                    # Execution Flow Diagram
                    st.markdown("**🔀 Execution Flow**")
                    st.markdown(get_flow_diagram(step), unsafe_allow_html=True)
                    
                    # Space vs Speed Visualization
                    st.markdown("**⚡ Space-Speed Trade-off**")
                    st.markdown(get_space_speed_info(step, len(nums)), unsafe_allow_html=True)
                
                # Memory allocation table - collapsible
                with st.expander("💾 Memory Allocation", expanded=False):
                    import sys
                    memory_data = []
                    for var_name in ['nums', 'complement_map', 'i', 'num', 'target', 'complement']:
                        if var_name in step['variables']:
                            value = step['variables'][var_name]
                            size_bytes = sys.getsizeof(value)
                            # Format size in bytes or KB
                            if size_bytes > 1024:
                                size_str = f"{size_bytes / 1024:.2f} KB"
                            else:
                                size_str = f"{size_bytes} B"
                            memory_data.append({
                                "Variable": var_name,
                                "Size": size_str,
                                "Type": type(value).__name__
                            })
                    
                    if memory_data:
                        st.dataframe(pd.DataFrame(memory_data), use_container_width=True, hide_index=True, height=120)
            
            # RIGHT: Scrollable Execution State + Variables using container
            with col_state:
                # Use a container that will scroll
                with st.container(border=False):
                    # Current iteration info - collapsible
                    with st.expander("🔍 Current Iteration", expanded=True):
                        st.markdown(f"**i:** `{step['current_index']}` | **num:** `{step['current_number']}` | **complement:** `{step['complement_needed']}`", help=None)
                    
                    # Hash Map Evolution - collapsible
                    with st.expander("🗺️ Hash Map", expanded=True):
                        map_col1, map_col2 = st.columns(2, gap="small")
                        with map_col1:
                            st.caption("Before:")
                            if step['map_before']:
                                before_df = pd.DataFrame([
                                    {"K": k, "V": v} for k, v in sorted(step['map_before'].items())
                                ])
                                st.dataframe(before_df, use_container_width=True, hide_index=True, height=80)
                            else:
                                st.caption("{ }")
                        
                        with map_col2:
                            st.caption("After:")
                            if step['map_after']:
                                after_df = pd.DataFrame([
                                    {"K": k, "V": v} for k, v in sorted(step['map_after'].items())
                                ])
                                st.dataframe(after_df, use_container_width=True, hide_index=True, height=80)
                            else:
                                st.caption("{ }")
                    
                    # Variables Watch - collapsible
                    with st.expander("👁️ Variables", expanded=True):
                        var_order = ['i', 'num', 'target', 'complement', 'complement_map', 'nums']
                        
                        # Determine which variables are active in this step
                        active_vars = {'i', 'num', 'target', 'complement', 'complement_map', 'nums'}
                        if step['found']:
                            active_vars = {'i', 'complement', 'complement_map'}  # Focus on the found variables
                        
                        var_data = []
                        for var_name in var_order:
                            if var_name in step['variables']:
                                value = step['variables'][var_name]
                                is_active = var_name in active_vars
                                highlight = "✓" if is_active else " "
                                var_data.append({
                                    "": highlight,
                                    "Var": var_name,
                                    "Value": str(value),
                                    "_active": is_active
                                })
                        
                        if var_data:
                            df = pd.DataFrame(var_data)
                            # Create HTML with highlighting for active variables
                            html_table = "<table style='width:100%; border-collapse: collapse;'><tr style='background-color: #f0f0f0; border-bottom: 1px solid #ddd;'>"
                            html_table += "<th style='padding: 8px; text-align: left; width: 5%;'></th>"
                            html_table += "<th style='padding: 8px; text-align: left; width: 30%;'>Var</th>"
                            html_table += "<th style='padding: 8px; text-align: left; width: 65%;'>Value</th>"
                            html_table += "</tr>"
                            
                            for _, row in df.iterrows():
                                bg_color = "#ffffff" if row["_active"] else "#f5f5f5"
                                border_left = "4px solid #28a745" if row["_active"] else "4px solid transparent"
                                html_table += f"<tr style='background-color: {bg_color}; border-bottom: 1px solid #ddd; border-left: {border_left};'>"
                                html_table += f"<td style='padding: 8px; text-align: center;'>{row['']}</td>"
                                html_table += f"<td style='padding: 8px; font-weight: bold;'><code>{row['Var']}</code></td>"
                                html_table += f"<td style='padding: 8px;'><code>{row['Value']}</code></td>"
                                html_table += "</tr>"
                            
                            html_table += "</table>"
                            st.markdown(html_table, unsafe_allow_html=True)
                        
                        # Status & Result
                        if step['found']:
                            st.success(f"✅ **Solution Found!** Indices: [{step['found_at_index']}, {step['current_index']}] = {step['result_values'][0]} + {step['result_values'][1]}")
                        else:
                            st.info(f"➕ **Added:** {step['current_number']} at index {step['current_index']}")
    
    elif execution_mode == "Show All Steps":
        st.subheader("📋 All Steps Summary")
        
        all_steps_data = []
        for step in st.session_state.steps:
            all_steps_data.append({
                "Step": step['step_number'],
                "Number": step['current_number'],
                "Index": step['current_index'],
                "Complement": step['complement_needed'],
                "Found?": "✅" if step['found'] else "❌",
                "Map": str(step['map_after'])
            })
        
        st.dataframe(pd.DataFrame(all_steps_data), use_container_width=True, hide_index=True)
        
        # Final result
        if st.session_state.steps and st.session_state.steps[-1].get('found'):
            st.success("✅ Solution Found!")
            final_step = st.session_state.steps[-1]
            st.markdown(f"**Result:** `{final_step['result']}` → {final_step['result_values']}")
        else:
            st.error("❌ No solution found!")
    
    elif execution_mode == "🎬 Auto-Play Animation":
        st.subheader("🎬 Animated Step-by-Step Execution")
        
        # Animation controls
        anim_col1, anim_col2, anim_col3 = st.columns([2, 1, 1])
        
        with anim_col1:
            play_speed = st.slider(
                "Animation Speed", 
                min_value=500, 
                max_value=3000, 
                value=st.session_state.animation_speed,
                step=100,
                label_visibility="collapsed"
            )
            st.session_state.animation_speed = play_speed
        
        with anim_col2:
            if st.button("▶️ Play All", use_container_width=True):
                st.session_state.auto_play = True
        
        with anim_col3:
            if st.button("⏸️ Stop", use_container_width=True):
                st.session_state.auto_play = False
        
        # Initialize auto_play state if needed
        if 'auto_play' not in st.session_state:
            st.session_state.auto_play = False
        
        # Auto-play animation loop
        if st.session_state.auto_play and st.session_state.steps:
            placeholder_steps = st.empty()
            placeholder_anim = st.empty()
            
            for idx in range(len(st.session_state.steps)):
                if not st.session_state.auto_play:
                    break
                    
                step = st.session_state.steps[idx]
                
                with placeholder_steps.container():
                    # Show current step info with animation
                    st.markdown(f"<div class='step-progress'><h3>Step {idx + 1} of {len(st.session_state.steps)}</h3></div>", 
                               unsafe_allow_html=True)
                    
                    # Three column layout for animation
                    col1, col2, col3 = st.columns(3, gap="medium")
                    
                    with col1:
                        st.markdown("**📊 Array Visualization**")
                        array_fig = create_array_pointer_visualization(nums, step['current_index'], step['complement_needed'])
                        st.plotly_chart(array_fig, use_container_width=True, config={'displayModeBar': False})
                    
                    with col2:
                        st.markdown("**🗂️ Hash Map State**")
                        hashmap_fig = create_animated_hashmap(step['map_after'], idx + 1, step['found'])
                        st.plotly_chart(hashmap_fig, use_container_width=True, config={'displayModeBar': False})
                    
                    with col3:
                        st.markdown("**📖 Step Details**")
                        st.info(f"""
                        **Current Number:** {step['current_number']}  
                        **Looking for:** {step['complement_needed']}  
                        **Found:** {'✅ YES' if step['found'] else '❌ NO'}
                        """)
                    
                    # Step explanation
                    explanation = get_step_explanation(step, st.session_state.explanation_depth)
                    st.markdown(f'<div class="explanation-box">{explanation}</div>', unsafe_allow_html=True)
                
                # Progress bar animation
                progress = (idx + 1) / len(st.session_state.steps)
                st.progress(progress)
                
                # Wait based on animation speed
                time.sleep(play_speed / 1000)
            
            # Final result
            st.markdown("---")
            if st.session_state.steps[-1].get('found'):
                final_step = st.session_state.steps[-1]
                st.success(f"✅ **Solution Found!** Indices: [{final_step['result'][0]}, {final_step['result'][1]}]")
                st.metric("Values", f"{final_step['result_values'][0]} + {final_step['result_values'][1]} = {target}")
            else:
                st.error("❌ No solution found!")
            
            st.session_state.auto_play = False
        else:
            st.info("👆 Click 'Play All' to start the animated walkthrough")
    
    else:  # Skip to Result
        st.subheader("🏁 Final Result")
        
        if st.session_state.steps and st.session_state.steps[-1].get('found'):
            step = st.session_state.steps[-1]
            st.success("✅ Solution Found!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Indices", f"[{step['result'][0]}, {step['result'][1]}]")
            with col2:
                st.metric("Sum", f"{step['result_values'][0]} + {step['result_values'][1]} = {target}")
            
            # Visualization
            st.markdown("**Array with Solution:**")
            result_df = pd.DataFrame({
                "Index": range(len(nums)),
                "Value": nums,
                "Solution": ["✅" if i in step['result'] else "" for i in range(len(nums))]
            })
            st.dataframe(result_df, use_container_width=True, hide_index=True)
            
            st.metric("Steps Executed", total_steps)
        else:
            st.error("❌ No solution exists for this input!")
            st.info(f"No two numbers in {nums} add up to {target}")

st.caption("Algorithm: Hash Map based Two-Sum | Time: O(n) | Space: O(n)")

