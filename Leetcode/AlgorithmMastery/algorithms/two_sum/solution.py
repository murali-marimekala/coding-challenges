"""
Two Sum Solution - With step-by-step tracking for visualization
"""

from typing import List, Tuple, Dict, Any
from utils.variable_tracker import VariableTracker


class TwoSumSolver:
    """Two Sum algorithm with detailed execution tracking"""
    
    @staticmethod
    def solve_with_steps(nums: List[int], target: int) -> Tuple[List[Dict[str, Any]], Dict]:
        """
        Solve Two Sum and return step-by-step execution data
        
        Returns:
            Tuple of (steps list, final state)
        """
        steps = []
        complement_map = {}
        tracker = VariableTracker()
        
        if not nums or len(nums) < 2:
            return steps, complement_map
        
        for i, num in enumerate(nums):
            complement = target - num
            found = complement in complement_map
            
            # Determine which line of code is being executed
            if i == 0:
                code_line = 4  # First iteration, entering for loop
            elif found:
                code_line = 7  # Found match, returning result
            else:
                code_line = 8  # Adding to hash map
            
            step_info = {
                'step_number': i + 1,
                'current_number': num,
                'current_index': i,
                'complement_needed': complement,
                'found': found,
                'found_at_index': complement_map.get(complement, None) if found else None,
                'map_before': dict(complement_map),
                'map_after': dict(complement_map),
                'code_line': code_line,
                'variables': {
                    'i': i,
                    'num': num,
                    'target': target,
                    'complement': complement,
                    'complement_map': dict(complement_map),
                    'nums': nums
                }
            }
            
            # Record state before adding to map
            tracker.record_state(i, code_line, step_info['variables'])
            
            if found:
                step_info['result'] = [complement_map[complement], i]
                step_info['result_values'] = [nums[complement_map[complement]], num]
                steps.append(step_info)
                break
            
            # Add current number to map
            complement_map[num] = i
            step_info['map_after'] = dict(complement_map)
            step_info['variables']['complement_map'] = dict(complement_map)
            steps.append(step_info)
        
        return steps, complement_map
    
    @staticmethod
    def solve_brute_force(nums: List[int], target: int) -> List[int]:
        """Brute force O(n²) solution for comparison"""
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []
    
    @staticmethod
    def solve_optimal(nums: List[int], target: int) -> List[int]:
        """Optimal O(n) solution (hash map approach)"""
        complement_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in complement_map:
                return [complement_map[complement], i]
            complement_map[num] = i
        return []


# Pre-built examples for each difficulty
EASY_EXAMPLES = [
    {
        'array': [2, 7, 11, 15],
        'target': 9,
        'expected': [0, 1],
        'explanation': '2 + 7 = 9. This is a straightforward case where the solution appears early in the array.',
        'step_explanations': [
            '📍 Step 1: Start with empty hash map. Process number 2 (index 0).',
            '   Need complement: 9 - 2 = 7',
            '   Hash map is empty, so 7 not found.',
            '   ➕ Add 2 → index 0 to map',
            '',
            '📍 Step 2: Process number 7 (index 1).',
            '   Need complement: 9 - 7 = 2',
            '   ✅ Found 2 in map at index 0!',
            '   🎉 Return indices [0, 1]',
        ]
    }
]

MEDIUM_EXAMPLES = [
    {
        'array': [3, 2, 4],
        'target': 6,
        'expected': [1, 2],
        'explanation': 'Demonstrates finding a solution in the middle/end of array. Shows that order matters.',
        'step_explanations': [
            '📍 Step 1: Process 3, need complement 3, not found, add to map',
            '📍 Step 2: Process 2, need complement 4, not found, add to map',
            '📍 Step 3: Process 4, need complement 2, FOUND at index 1!',
            '🎉 Return [1, 2]'
        ]
    },
    {
        'array': [3, 3],
        'target': 6,
        'expected': [0, 1],
        'explanation': 'Demonstrates using the same number twice (duplicates). Important edge case.',
        'step_explanations': [
            '📍 Step 1: Process first 3, need 3, not found, add to map',
            '📍 Step 2: Process second 3, need 3, FOUND at index 0!',
            '🎉 Return [0, 1]'
        ]
    }
]

HARD_EXAMPLES = [
    {
        'array': [-1, -2, -3, 5, 10],
        'target': 7,
        'expected': [-2, 9],
        'explanation': 'Works with negative numbers. Shows algorithm flexibility.',
        'step_explanations': [
            '📍 Step 1-4: Process negative numbers and 5, no matches',
            '📍 Step 5: Process 10, need -3, found at index 2!',
            '🎉 Return [2, 4] → [-3, 10] = 7'
        ]
    },
    {
        'array': [-10, -1, 0, 5, 9],
        'target': -1,
        'expected': [-10, 9],
        'explanation': 'Negative target value. Shows algorithm handles any target.',
        'step_explanations': [
            '📍 Step 1: Process -10, need 9, not found, add to map',
            '📍 Steps 2-4: Process other numbers, no matches',
            '📍 Step 5: Process 9, need -10, FOUND at index 0!',
            '🎉 Return [0, 4] → [-10, 9] = -1'
        ]
    }
]
