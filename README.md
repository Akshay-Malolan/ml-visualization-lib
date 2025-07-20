# Machine Learning Visualization Library

This project is a library for visualizing machine learning concepts, particularly focusing on cost functions and data plotting. It provides various functions to help users understand the behavior of their models through visual representation.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the library, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/ml-visualization-lib.git
cd ml-visualization-lib
pip install -r requirements.txt
```

## Usage

After installation, you can use the library in your Python scripts as follows:

```python
from ml_visualization.plotting import plt_house_x, plt_intuition
from ml_visualization.cost_functions import compute_cost

# Example usage of plotting functions
plt_house_x(X, y)
plt_intuition(x_train, y_train)

# Example usage of cost function
cost = compute_cost(x, y, w, b)
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.