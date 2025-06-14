import pydicom
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
from pydicom import dcmread

class Procesador:
    def cargar_serie_dicom(self, carpeta_dicom):
        # carga de archivos DICOM
        carpeta_dicom = "Datos"  

        # Obtener los nombres de todos los archivos .dcm
        archivos_dicom = [f for f in os.listdir(carpeta_dicom) if f.endswith('.dcm')]

        # Mostrar los nombres
        print("Archivos DICOM encontrados:")
        for nombre in archivos_dicom:
            print(nombre)
        
        slices = []
        for archivo in archivos_dicom:
            path = os.path.join(carpeta_dicom, archivo)
            ds = dcmread(path)
            slices.append(ds)

        return slices

    def reconstruir_3d(self, archivos_dicom):
        # reconstrucción 3D
        datasets_ordenados = sorted(archivos_dicom, key=lambda x: float(x.ImagePositionPatient[2]))
        volumen = np.stack([ds.pixel_array for ds in datasets_ordenados])
        print("Volumen reordenado:", volumen.shape)
        
        return volumen
    
    def mostrar_cortes(self, volumen):
        # Visualizar el corte medio en cada eje ortogonal
        mid_axial = volumen.shape[0] // 2
        mid_coronal = volumen.shape[1] // 2
        mid_sagital = volumen.shape[2] // 2

        corte_axial = volumen[mid_axial, :, :]     # plano XY
        corte_coronal = volumen[:, mid_coronal, :] # plano XZ
        corte_sagital = volumen[:, :, mid_sagital] # plano YZ

        # Crear subplots para visualizar cortes en Z, Y y X
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        axs[0].imshow(corte_axial, cmap='gray')  # Corte axial
        axs[0].set_title(f'Corte axial ')
        axs[0].axis('off')

        axs[1].imshow(corte_coronal, cmap='gray', aspect= 'auto')  # Corte coronal #aspect auto para arreglar achatamiento
        axs[1].set_title(f'Corte coronal ')
        axs[1].axis('off')

        axs[2].imshow(corte_sagital, cmap='gray', aspect= 'auto')  # Corte sagital
        axs[2].set_title(f'Corte sagital ')
        axs[2].axis('off')

        plt.tight_layout()
        plt.show()

class Paciente:
    def __init__(self, ds, im_3d):
        self.id_ = ds.PatientID
        self.nombre = ds.PatientName
        self.edad = ds.PatientAge
        self.imagen = im_3d #la anteriormente reconstruida

                


