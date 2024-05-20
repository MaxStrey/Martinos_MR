import sys
import numpy as np
from scipy.fft import fft2, fftshift
from skimage.transform import resize
from skimage.data import shepp_logan_phantom
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage

class FourierTransformGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(1000, 600)  # Adjusted window size

        # Main layout
        main_layout = QVBoxLayout()

        # Dropdown for image selection
        self.image_dropdown = QComboBox()
        self.image_dropdown.addItem("Shepp-Logan Phantom")
        self.image_dropdown.addItem("Undersampled Shepp-Logan Phantom")
        # Add more items if needed
        main_layout.addWidget(self.image_dropdown)

        # Horizontal layout for images
        image_layout = QHBoxLayout()

        # Labels for displaying images
        self.original_image_label = QLabel()
        self.original_image_label.setMinimumSize(300, 300)
        image_layout.addWidget(self.original_image_label)

        self.transformed_image_label = QLabel()
        self.transformed_image_label.setMinimumSize(300, 300)
        image_layout.addWidget(self.transformed_image_label)
        
        self.reconstructed_image_label = QLabel()
        self.reconstructed_image_label.setMinimumSize(300, 300)
        image_layout.addWidget(self.reconstructed_image_label)

        main_layout.addLayout(image_layout)

        # Process button
        process_button = QPushButton("Process Image")
        process_button.clicked.connect(self.process_image)
        main_layout.addWidget(process_button)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def process_image(self):
        # Load and resize image
        standardPhantom = resize(shepp_logan_phantom(), (256, 256), anti_aliasing=True)  # shepp_logan_phantom()
        undersampledPhantom = resize(standardPhantom, (256, 128), anti_aliasing=True)
        if self.image_dropdown.currentText() == "Shepp-Logan Phantom":
            image = standardPhantom
        elif self.image_dropdown.currentText() == "Undersampled Shepp-Logan Phantom":
            image = undersampledPhantom
            

        # Display original image
        original_qimage = self.numpy_to_qimage(image)
        self.original_image_label.setPixmap(QPixmap.fromImage(original_qimage))

        # Apply Fourier transform
        transformed_image = fftshift(fft2(image))

        # Resize the transformed image to fit the label
        transformed_image_resized = resize(np.abs(transformed_image), (256, 256), anti_aliasing=True)

        # Convert to displayable format and display
        transformed_qimage = self.numpy_to_qimage(transformed_image_resized)
        self.transformed_image_label.setPixmap(QPixmap.fromImage(transformed_qimage))
        
        # Transform back to spatial domain
        reconstructed_image = np.abs(np.fft.ifft2(np.fft.ifftshift(transformed_image)))
        reconstructed_image_resized = resize(reconstructed_image, (256, 256), anti_aliasing=True)
        

        # Display reconstructed image
        reconstructed_qimage = self.numpy_to_qimage(reconstructed_image_resized)
        self.reconstructed_image_label.setPixmap(QPixmap.fromImage(reconstructed_qimage))
        
        
        

    def numpy_to_qimage(self, array):
        array = np.uint8(array / np.max(array) * 255)  # Normalize and convert to 8-bit
        qimage = QImage(array, array.shape[1], array.shape[0], QImage.Format_Grayscale8)
        return qimage

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FourierTransformGUI()
    window.show()
    sys.exit(app.exec_())
