"""
Playback Controller Component
Handles multi-speed playback (play, pause, step, slow, fast)
"""

import streamlit as st
from typing import List, Callable
from enum import Enum
import time


class PlaybackSpeed(Enum):
    """Playback speed options"""
    SLOW_2X = 0.5  # 2x slower = 2x the delay
    NORMAL = 1.0
    FAST_2X = 2.0  # 2x faster = 0.5x the delay


class PlaybackController:
    """Control playback of step-by-step execution"""
    
    DEFAULT_STEP_DELAY_MS = 1500  # milliseconds per step
    
    def __init__(self, total_steps: int, on_step_change: Callable = None):
        """
        Initialize playback controller
        
        Args:
            total_steps: Total number of steps to play through
            on_step_change: Callback function when step changes
        """
        self.total_steps = total_steps
        self.on_step_change = on_step_change
        
        # Initialize session state
        if 'playback_step' not in st.session_state:
            st.session_state.playback_step = 0
        if 'playback_speed' not in st.session_state:
            st.session_state.playback_speed = PlaybackSpeed.NORMAL.value
        if 'playback_playing' not in st.session_state:
            st.session_state.playback_playing = False
        if 'playback_last_update' not in st.session_state:
            st.session_state.playback_last_update = 0
    
    def render_controls(self):
        """Render playback control buttons"""
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            if st.button("▶️ Play", use_container_width=True, key="playback_play"):
                st.session_state.playback_playing = True
                st.rerun()
        
        with col2:
            if st.button("⏸️ Pause", use_container_width=True, key="playback_pause"):
                st.session_state.playback_playing = False
        
        with col3:
            if st.button("⬅️ Prev", 
                        disabled=st.session_state.playback_step == 0, 
                        use_container_width=True, 
                        key="playback_prev"):
                st.session_state.playback_step = max(0, st.session_state.playback_step - 1)
                st.session_state.playback_playing = False
                if self.on_step_change:
                    self.on_step_change(st.session_state.playback_step)
                st.rerun()
        
        with col4:
            if st.button("Next ➡️", 
                        disabled=st.session_state.playback_step >= self.total_steps - 1, 
                        use_container_width=True, 
                        key="playback_next"):
                st.session_state.playback_step = min(self.total_steps - 1, st.session_state.playback_step + 1)
                st.session_state.playback_playing = False
                if self.on_step_change:
                    self.on_step_change(st.session_state.playback_step)
                st.rerun()
        
        with col5:
            speed = st.select_slider(
                "Speed",
                options=[PlaybackSpeed.SLOW_2X.value, PlaybackSpeed.NORMAL.value, PlaybackSpeed.FAST_2X.value],
                value=st.session_state.playback_speed,
                format_func=lambda x: {0.5: "Slow", 1.0: "Normal", 2.0: "Fast"}[x],
                key="playback_speed_slider"
            )
            st.session_state.playback_speed = speed
        
        with col6:
            if st.button("🔄 Reset", use_container_width=True, key="playback_reset"):
                st.session_state.playback_step = 0
                st.session_state.playback_playing = False
                if self.on_step_change:
                    self.on_step_change(0)
                st.rerun()
    
    def render_progress(self):
        """Render progress indicator"""
        if self.total_steps > 0:
            progress = (st.session_state.playback_step + 1) / self.total_steps
            st.progress(progress)
            st.caption(f"Step {st.session_state.playback_step + 1}/{self.total_steps} " + 
                      f"({int(progress * 100)}%)")
    
    def get_current_step(self) -> int:
        """Get current step number"""
        return st.session_state.playback_step
    
    def is_playing(self) -> bool:
        """Check if playback is active"""
        return st.session_state.playback_playing
    
    def next_step(self):
        """Advance to next step"""
        if st.session_state.playback_step < self.total_steps - 1:
            st.session_state.playback_step += 1
            if self.on_step_change:
                self.on_step_change(st.session_state.playback_step)
        else:
            # End of playback
            st.session_state.playback_playing = False
    
    def get_delay_seconds(self) -> float:
        """Get current step delay in seconds based on speed"""
        base_delay_seconds = self.DEFAULT_STEP_DELAY_MS / 1000.0
        return base_delay_seconds / st.session_state.playback_speed
