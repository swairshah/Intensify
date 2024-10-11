import math
from .colormaps import COLORMAPS

def match_arrays(a, b):
    return b[:len(a)] if len(b) > len(a) else b + [0]*(len(a)-len(b))

class Intensify:
    ANSI_RESET = "\033[0m"

    COLORMAPS = {}

    def __init__(self, calibration_factor=1.0, log_scale=False, min_intensity=0.0001, colormap='reds'):
        """
        Initialize the Intensify instance with calibration options and colormap.

        :param calibration_factor: Factor to calibrate intensity (default is 1.0)
        :param log_scale: Whether to use logarithmic scaling for intensities (default is False)
        :param min_intensity: Minimum intensity value to consider (default is 0.0001)
        :param colormap: Name of the colormap to use (default is 'reds')
        """
        self.calibration_factor = calibration_factor
        self.log_scale = log_scale
        self.min_intensity = min_intensity
        self.add_predefined_colormaps()
        self.set_colormap(colormap)

    def add_predefined_colormaps(self):
        """
        Add predefined colormaps, including those from Matplotlib.
        """
        self.COLORMAPS = COLORMAPS

    def set_colormap(self, colormap):
        """
        Set the current colormap.

        :param colormap: Name of the colormap to use
        """
        if colormap not in self.COLORMAPS:
            raise ValueError(f"Unsupported colormap '{colormap}'. Supported colormaps are: {', '.join(self.COLORMAPS.keys())}")
        self.colormap = self.COLORMAPS[colormap]
        self.colormap_length = len(self.colormap)

    def calibrate_intensity(self, value):
        """
        Apply a non-linear transformation to the intensity value.

        :param value: Original intensity value (0 to 1)
        :return: Calibrated intensity value
        """
        # Ensure the value is not smaller than min_intensity
        value = max(value, self.min_intensity)
        
        if self.log_scale:
            # Apply logarithmic scaling
            value = math.log(value) / math.log(self.min_intensity)
        
        # Apply calibration factor
        value = math.pow(value, self.calibration_factor)
        
        # Ensure the result is between 0 and 1
        return max(0, min(value, 1))

    def map_intensity_to_color(self, intensity):
        """
        Map a calibrated intensity value to a color in the colormap.

        :param intensity: Calibrated intensity value (0 to 1)
        :return: Tuple of (R, G, B)
        """
        # Ensure intensity is within [0, 1]
        intensity = max(0, min(intensity, 1))
        # Scale intensity to colormap index
        index = int(intensity * (self.colormap_length - 1))
        return self.colormap[index]

    def get_ansi_color_code(self, color, background=False):
        """
        Generate ANSI escape code for a given RGB color.

        :param color: Tuple of (R, G, B)
        :param background: If True, generate background color code
        :return: ANSI escape code string
        """
        r, g, b = color
        if background:
            return f"\033[48;2;{r};{g};{b}m"
        else:
            return f"\033[38;2;{r};{g};{b}m"

    def enhance_contrast(self, intensities):
        """
        Enhance contrast of intensities using a simplified histogram equalization.

        :param intensities: List of intensity values
        :return: List of enhanced intensity values
        """
        # Sort intensities and get their ranks
        sorted_intensities = sorted(enumerate(intensities), key=lambda x: x[1])
        ranks = [0] * len(intensities)
        for i, (index, _) in enumerate(sorted_intensities):
            ranks[index] = i

        # Map ranks to new intensity values
        enhanced = [rank / (len(intensities) - 1) for rank in ranks]
        return enhanced

    def print(self, data, background=False, print_output=True, enhance=True):
        """
        Apply color to each text element based on corresponding intensity.

        :param data: Dictionary with 'text' and 'intensities' lists
        :param background: If True, apply background colors instead of text colors
        :param print_output: If True, prints the colored text. Otherwise, returns the string.
        :param enhance: If True, applies contrast enhancement to intensities
        :return: Colored string if print_output is False
        """
        texts = data.get("text", [])
        intensities = data.get("intensities", [])

        if len(texts) != len(intensities):
            intensities = match_arrays(texts, intensities)

        # normalize intensities 
        if any(i < 0 or i > 1 for i in intensities):
            min_intensity = min(intensities)
            max_intensity = max(intensities)
            if min_intensity != max_intensity:
                intensities = [(i - min_intensity) / (max_intensity - min_intensity) for i in intensities]
            else:
                intensities = [1.0] * len(intensities)

        # Apply contrast enhancement if enabled
        if enhance:
            intensities = self.enhance_contrast(intensities)

        colored_texts = []
        for word, intensity in zip(texts, intensities):
            calibrated_intensity = self.calibrate_intensity(intensity)
            color = self.map_intensity_to_color(calibrated_intensity)
            color_code = self.get_ansi_color_code(color, background)
            colored_word = f"{color_code}{word}{self.ANSI_RESET}"
            colored_texts.append(colored_word)

        result = ' '.join(colored_texts)

        if print_output:
            print(result)
        else:
            return result

    def print_sentence(self, sentence, intensities, background=False, print_output=True, enhance=True):
        """
        Helper method to colorize a sentence based on word intensities.

        :param sentence: The sentence string
        :param intensities: List of intensity values for each word
        :param background: If True, apply background colors instead of text colors
        :param print_output: If True, prints the colored text. Otherwise, returns the string.
        :param enhance: If True, applies contrast enhancement to intensities
        :return: Colored string if print_output is False
        """
        words = sentence.split()
        data = {"text": words, "intensities": intensities}
        return self.print(data, background, print_output, enhance)

    def add_custom_colormap(self, name, colors):
        """
        Add a custom colormap.

        :param name: Name of the custom colormap
        :param colors: List of (R, G, B) tuples
        """
        if name in self.COLORMAPS:
            raise ValueError(f"Colormap '{name}' already exists.")
        self.COLORMAPS[name] = colors
