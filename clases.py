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

class ProcesadorPNG:
    def im_original(self, pacientes):
        indice = int(input("\nIngrese el número del paciente que desea usar: ")) #esto es mas con la clave del paciente
        ima_original = pacientes[indice].imagen
        return ima_original
    
    def traslación(self, ima_original):

        opciones = {
            1: (13, 120),   # Derecha, abajo
            2: (100, -50),  # Derecha, arriba
            3: (70, -100)   # Derecha, más arriba
        }

        # Pedir selección
        opcion = int(input("Elige número de 1 a 3: "))
        dx, dy = opciones.get(opcion, (0, 0))  # Si no es válido, no se mueve
        print(f"Traslación aplicada: dx={dx}, dy={dy}")

        # Crear la matriz de transformación
        MT = np.float32([[1, 0, dx], [0, 1, dy]])

        # Obtener tamaño de la imagen original
        row, col = ima_original.shape  # img es la imagen DICOM 2D

        # Aplicar traslación
        tras = cv2.warpAffine(ima_original, MT, (col, row))

        # Mostrar imágenes en subplots
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        axes[0].imshow(ima_original, cmap='gray')
        axes[0].set_title("Imagen original")
        axes[0].axis('off')

        axes[1].imshow(tras, cmap='gray')
        axes[1].set_title(f"Imagen trasladada\n(dx={dx}, dy={dy})")
        axes[1].axis('off')
        plt.tight_layout()
        plt.show()

        # Guardar imagen
        tras_uint8 = cv2.normalize(tras, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        cv2.imwrite("imagen_trasladada.png", tras_uint8)
        print("Imagen trasladada guardada como 'imagen_trasladada.png")

#Función para ingresar imágenes
imagenesNuevas= {}

def IngresarImagen():
  ruta = input('Ingrese la ruta de la imagen JPG o PNG:')

  if not os.path.exists(ruta):
      print('Ruta inválida.')
      return

  nombre = input('Asignele un nombre: ')

  if not ruta.lower().endswith(('.jpg', '.png')):
      print("Formato no válido.")

  elif ruta.lower().endswith('.dcm'):
        try:
            ds = pydicom.dcmread(ruta)
            imagenesNuevas[nombre]= ds.pixel_array
        except Exception as e:
            print(f'Error')
            return
  else:
      print('No se pudo cargar la imagen.')
      return
      
  imagenesNuevas[nombre] = img
  print(f"Imagen cargada exitosamente.")
                


