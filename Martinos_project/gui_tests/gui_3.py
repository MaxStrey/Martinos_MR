import sys
import numpy as np
from scipy.fft import ifft2, fft2, fftshift
from skimage.transform import resize
from skimage.data import shepp_logan_phantom
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtGui import QPixmap, QImage
import nibabel as nib
import pandas as pd
from tqdm import tqdm




class FourierTransformGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(1000, 600)  # Adjusted window size

        # Main layout
        main_layout = QVBoxLayout()

        # Dropdown for image selection
        self.image_dropdown = QComboBox()
        self.image_dropdown.addItem("Max's mprage nii file")
        self.image_dropdown.addItem("Shepp-Logan Phantom")
        # Add more items if needed
        main_layout.addWidget(self.image_dropdown)
        
        self.slice_number_input = QLineEdit()
        self.slice_number_input.setPlaceholderText("Enter slice number")
        main_layout.addWidget(self.slice_number_input)
        
        # Line edit for field_map_multiplier input
        self.field_map_multiplier_input = QLineEdit()
        self.field_map_multiplier_input.setPlaceholderText("Enter field map multiplier")
        main_layout.addWidget(self.field_map_multiplier_input)
        
        # Clear images button
        clear_button = QPushButton("Clear Images")
        clear_button.clicked.connect(self.clear_images)
        main_layout.addWidget(clear_button)

        # Horizontal layout for images
        image_layout = QHBoxLayout()
    

        # Labels for displaying images
        self.original_image_label = QLabel()
        self.original_image_label.setMinimumSize(300, 300)
        image_layout.addWidget(self.original_image_label)
        self.original_image_label.move(50, 0)

        self.transformed_image_label = QLabel()
        self.transformed_image_label.setMinimumSize(300, 300)
        image_layout.addWidget(self.transformed_image_label)
        self.transformed_image_label.move(100, 0)
        
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
        standardPhantom = resize(shepp_logan_phantom(), (256, 256), anti_aliasing=True)  # shepp_logan_phantom()

        if self.image_dropdown.currentText() == "Max's mprage nii file":
            img = nib.load('max_mprage.nii')
            mprage = img.get_fdata()
        elif self.image_dropdown.currentText() == "Shepp-Logan Phantom":
            img = standardPhantom
        
        


        # Get the data as a NumPy array
        
       

        gamma = 42.58e6  # Gyromagnetic ratio for hydrogen in Hz/T
        g_multx = 20 # Gradient multiplication factor in the x direction
        g_multy = 13.6 # Gradient multiplication factor in the y direction
        Gx = 0.004755753 * g_multx  # Gradient strength in T/m
        Gy = 0.004755753 * g_multy # Gradient strength in T/m
        Gz = 0.004755753 * g_multx # Gradient strength in T/m
        
            
        # Retrieve slice number from line edit
        try:
            slice_number = int(self.slice_number_input.text())
            if slice_number >= mprage.shape[2]:
                print("Slice number is out of bounds. Please enter a number less than {}.".format(mprage.shape[2]))
                return
        except ValueError:
            print("Invalid slice number. Please enter a valid integer.")
            return  # Exit the function if the input is not valid
        
        phantom = np.flipud(mprage[:, :, slice_number].T)
        phantom = phantom.astype(dtype=np.complex128) # Make the phantom complex


        B0_field_map = pd.read_csv('2Dslice.csv', header=None).values
        gamma = 42.58e6  # Gyromagnetic ratio for hydrogen in Hz/T
        B0_field_map  = (B0_field_map * gamma)/(2*np.pi * 10000)  # Convert to Hz/T
        B0_mean = np.mean(B0_field_map)  # Mean value of the B0 field map
        B0_field_map -= B0_mean # subtract by the mean value of the B0 field map
        B0_field_map *= 20 # B0 multiplier to see the distortion better
        B0_field_map = resize(B0_field_map, (256, 176))
        
        # Retrieve field_map_multiplier from line edit
        try:
            field_map_multiplier = float(self.field_map_multiplier_input.text())
        except ValueError:
            print("Invalid multiplier. Please enter a valid number.")
            return  # Exit the function if the input is not valid
        
        field_map_multiplier = 1
        B0_field_map = B0_field_map*field_map_multiplier
        
        # Time intervals for the gradients
        tau = 2e-3 # seconds

        timex = np.linspace(-tau/2,tau/2,256)
        timey = np.linspace(-tau/2,tau/2,176)

        # Gradient fields (assuming same for x and y directions)
        Gx_values = timex * Gx
        Gy_values = timey * Gy

        # k-space trajectory (assuming same for x and y directions)
        kx_values = gamma * Gx_values
        ky_values = gamma * Gy_values

        # Define field of view
        FOV = .2  # meters
        x_values = np.linspace(-FOV / 2, FOV / 2, 256)
        y_values = np.linspace(-FOV / 2, FOV / 2, 176)
        x_values, y_values = np.meshgrid(x_values, y_values, indexing='ij')  # Create 2D coordinate grid

        # Flatten the phantom
        phantom_flat = phantom.flatten()

        # Flatten the arrays to make them 1D
        x_values_flat = x_values.flatten()
        y_values_flat = y_values.flatten()
        B0_field_map_flat = B0_field_map.flatten()

        # Allocate memory for flattened k-space
        k_space_flat = np.zeros(176*256, dtype=np.complex128)



        # Iterate through the kx and ky values
        iterator = 0
        for i, kx in tqdm(enumerate(kx_values)):
            for j, ky in enumerate(ky_values):
                # Calculate the k-space value for this (kx, ky) point
                k_space_flat[iterator] = np.sum(phantom_flat * np.exp(-1j * (kx * x_values_flat + ky * y_values_flat + B0_field_map_flat * timey[j])))
                iterator += 1

        # Reshape the flattened k-space data back into 2D matrix form
        k_space = np.reshape(k_space_flat, (256, 176))
        
        # Display original image
        original_qimage = self.numpy_to_qimage(phantom)
        self.original_image_label.setPixmap(QPixmap.fromImage(original_qimage))

        # Convert to displayable format and display
        transformed_qimage = self.numpy_to_qimage(B0_field_map)
        self.transformed_image_label.setPixmap(QPixmap.fromImage(transformed_qimage))
        
        # display B0 map
        self.reconstructed_image_label.setPixmap(QPixmap.fromImage(original_qimage))
        
        # Apply inverse FFT
        reconstructed_image = ifft2(k_space)
        reconstructed_image_1 = fftshift(reconstructed_image)
        

        # Display reconstructed image
        reconstructed_qimage = self.numpy_to_qimage(reconstructed_image_1)
        self.reconstructed_image_label.setPixmap(QPixmap.fromImage(reconstructed_qimage))
        
    def clear_images(self):
        # Clear the pixmap of each label
        self.original_image_label.clear()
        self.transformed_image_label.clear()
        self.reconstructed_image_label.clear()
        self.original_image_label.setText("Original Image")
        self.transformed_image_label.setText("B0 Map")
        self.reconstructed_image_label.setText("Reconstructed Image")
        

    def numpy_to_qimage(self, array):
        # Handle complex arrays by taking the magnitude
        if np.iscomplexobj(array):
            array = np.abs(array)

        # Normalize the array to 0-255
        array = (array - np.min(array)) / (np.max(array) - np.min(array)) * 255

        # Convert array to uint8
        array = array.astype(np.uint8)

        # Create QImage from the array
        qimage = QImage(array.data, array.shape[1], array.shape[0], array.strides[0], QImage.Format_Grayscale8)
        return qimage


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FourierTransformGUI()
    window.show()
    sys.exit(app.exec_())
