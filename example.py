from intensify import Intensify

def main():
    intesifier = Intensify(calibration_factor=1.0, colormap='inferno')

    data = {
        "text": ["This", "is", "an", "example", "sentence", "where", "words", "are", "colored", "using", "inferno"],
        "intensities": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.0]
    }
    intesifier.print(data)

    data = {
        "text": ["This", "is", "an", "example", "sentence", "where", "words", "are", "colored", "using", "reds"],
        "intensities": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.0]
    }
    intesifier.set_colormap('reds')
    intesifier.print(data)

    intesifier.set_colormap('reds')
    intesifier.print(data)

if __name__ == "__main__":
    main()
