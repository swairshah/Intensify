from intensify import Intensify

def main():
    intensifier = Intensify(calibration_factor=1.0, colormap='inferno')

    data = {
        "text": ["This", "is", "an", "example", "sentence", "where", "words", "are", "colored", "using", "inferno"],
        "intensities": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.0]
    }
    intensifier.print(data, join_str=' ')

    data = {
        "text": ["This", "is", "an", "example", "sentence", "where", "words", "are", "colored", "using", "reds"],
        "intensities": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.0]
    }
    intensifier.set_colormap('reds')
    intensifier.print(data, join_str=' ')

    intensifier.set_colormap('reds')
    intensifier.print(data, join_str=' ')

    print("\nExample with close together values:")
    close_data = {
        "text": ["These", "words", "have", "very", "similar", "intensity", "values"],
        "intensities": [0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56]
    }
    
    print("Without contrast enhancement:")
    intensifier.print(close_data, enhance=False, join_str=' ')
    
    print("\nWith contrast enhancement:")
    intensifier.print(close_data, enhance=True, join_str=' ')

if __name__ == "__main__":
    main()
