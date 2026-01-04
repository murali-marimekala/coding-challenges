# 🎯 Algorithm Mastery Platform

Interactive learning platform for mastering difficult algorithms through worked examples, step-by-step visualization, and cognitive science-backed techniques.

## Quick Start

### Option 1: One-Command Run (Recommended)

**macOS/Linux:**
```bash
cd Leetcode/AlgorithmMastery
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
cd Leetcode\AlgorithmMastery
run.bat
```

### Option 2: Manual Run

```bash
cd Leetcode/AlgorithmMastery
pip install streamlit plotly pandas pyyaml
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Features

### Tier 1 Foundation
- ✅ **Worked Examples** - Multiple examples per difficulty level (Easy/Medium/Hard)
- ✅ **Step-by-Step Playback** - Navigate through algorithm execution with multi-speed controls
- ✅ **Hash Map Visualization** - See how the algorithm evolves in real-time
- ✅ **Code Display** - View the algorithm implementation with syntax highlighting
- ✅ **Variable Tracking** - Monitor variable values at each step
- ✅ **Collapsible Sections** - Clean, organized interface

### Learning Theory
Built on cognitive science principles:
- **Worked Examples Effect** - Step-by-step solutions reduce cognitive load
- **Cognitive Load Theory** - Minimize extraneous, maximize germane load
- **Spacing Effect** - Foundation for spaced practice (coming soon)
- **Retrieval Practice** - Foundation for quiz integration (coming soon)

## Architecture

### Config-Driven Design
Algorithms are defined in `algorithms/<algorithm>/config.yaml`:
- Metadata (name, difficulty, patterns, learning objectives)
- Test cases for each difficulty level
- Complexity analysis (time/space)
- Pseudocode and learning objectives

### Reusable Components
- `ConfigLoader` - Load algorithm metadata from YAML
- `VariableTracker` - Track variable states across execution
- `WorkedExamplePlayer` - Render step-by-step explanations
- `PlaybackController` - Multi-speed playback controls
- `VariableTrackerUI` - Visualize variable evolution

### Easy to Extend
Adding a new algorithm requires only:
1. Create `algorithms/<name>/config.yaml`
2. Create `algorithms/<name>/solution.py` with execution logic
3. All components automatically work with the new algorithm

## File Structure

```
AlgorithmMastery/
├── app.py                          # Main Streamlit application
├── run.sh / run.bat               # Quick start scripts
├── README.md                       # This file
├── algorithms/
│   └── two_sum/
│       ├── config.yaml            # Algorithm metadata
│       ├── solution.py            # Implementation + examples
│       └── __init__.py
├── components/
│   ├── playback_controller.py     # Multi-speed playback controls
│   ├── worked_example_player.py   # Step-by-step visualization
│   ├── variable_tracker_ui.py     # Variable state visualization
│   └── __init__.py
├── utils/
│   ├── config_loader.py           # YAML config management
│   ├── variable_tracker.py        # Execution state tracking
│   └── __init__.py
└── data/                          # User progress/achievements (future)
```

## Usage

### Starting the App
```bash
./run.sh              # macOS/Linux
run.bat              # Windows
```

### Using the App
1. **Select Difficulty** - Choose Easy, Medium, or Hard
2. **View Problem** - Expand "Problem Overview" to see input/output
3. **Study Code** - "Algorithm Code" shows implementation with controls underneath
4. **Run Playback** - Use play/pause/next/prev buttons to step through
5. **Analyze State** - Expand sections to see hash map, variables, arrays
6. **Read Explanation** - Step explanation helps understand each iteration

## Requirements

- Python 3.8+
- Streamlit
- Plotly
- Pandas
- PyYAML

The `run.sh` and `run.bat` scripts will automatically install dependencies if needed.

## Next Steps (Tier 2+)

- 🔄 Comparison view (optimal vs brute force)
- 🎯 Interactive quiz mode
- 📊 Progress tracking & achievements
- 🎨 Custom input testing
- 🧬 Algorithm comparison patterns
- 📚 Curriculum builder
- 🌍 Spaced review scheduler

## Contributing

To add a new algorithm:

1. Create directory: `algorithms/<algorithm_name>/`
2. Add `config.yaml` with metadata and test cases
3. Add `solution.py` with `TwoSumSolver`-style class
4. App automatically discovers and loads it

## License

MIT

## Support

For issues or suggestions, open an issue on GitHub.

---

**Happy Learning! 🚀**
