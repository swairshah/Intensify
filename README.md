# Intensify

Intensify is a Python package that allows you to colorize text based on intensity values. It provides an easy-to-use interface for applying color gradients to text or background colors in the terminal.

## Installation

You can install Intensify using pip:

```bash
pip install git+https://github.com/swairshah/Intensify
```

example usage::

```python
from intensify import Intensify

intesifier = Intensify(calibration_factor=1.0, colormap='inferno')

data = {
    "text": ["This", "is", "an", "example", "sentence", "where", "words", "are", "colored", "using", "inferno"],
    "intensities": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.0]
}
intesifier.print(data)
```

## Features

- Multiple predefined colormaps
- Custom colormap support
- Intensity calibration options
- Background coloring support
- Logarithmic scaling for intensities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.