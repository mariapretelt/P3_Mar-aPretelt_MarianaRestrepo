import pydicom
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
from pydicom import dcmread

class Procesador:
    def cargar_serie_dicom(self, carpeta_dicom):

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

        # Crear subplots
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        axs[0].imshow(corte_axial, cmap='gray')  # Corte axial
        axs[0].set_title(f'Corte axial ')
        axs[0].axis('off')

        axs[1].imshow(corte_coronal, cmap='gray', aspect= 6)  # Corte coronal #aspect auto para arreglar achatamiento
        axs[1].set_title(f'Corte coronal ')
        axs[1].axis('off')

        axs[2].imshow(corte_sagital, cmap='gray', aspect= 6)  # Corte sagital
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
        indice = input("\nIngrese clave del paciente que desea usar: ") #esto es mas con la clave del paciente
        ima_original = pacientes[indice].imagen
        corte_axial = ima_original[ima_original.shape[0] // 2]  # Corte central (Z/2)
        return corte_axial
    
    def traslación(self, corte_axial):

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
        row, col = corte_axial.shape[:2] # img es la imagen DICOM 2D

        # Aplicar traslación
        tras = cv2.warpAffine(corte_axial, MT, (col, row))

        # Mostrar imágenes en subplots
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        axes[0].imshow(corte_axial, cmap='gray')
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

    def tranf(self, pacientes):
        print("Claves de pacientes disponibles:")
        for clave in pacientes:
            print("-", clave)
        clave = input("Ingrese la clave del paciente a procesar: ")
        if clave in pacientes:
            corte = pacientes[clave].imagen
            patient_id = pacientes[clave].id_
        else:
            print("Clave no válida.")
        
        # Se toma una imagen 2D 
        imagen_3d = pacientes[clave].imagen
        corte = imagen_3d[imagen_3d.shape[0] // 2]  # Corte axial
        corte = cv2.normalize(corte, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        opcion= input( '''Opciones de binarización:
            1. Binario
            2. Binario invertido
            3. Truncado
            4. Tozero
            5. Tozero invertido
            ''')
    

        kernel_size = int(input("Ingrese el tamaño del kernel morfológico (impar): "))
        umbral = 125  

        print("Seleccione la forma a dibujar:")
        print("1. Círculo")
        print("2. Cuadrado")
        shape_choice = int(input("Opción (1-2): "))


        # Binarización
        if opcion == '1':
                _, binaria_im = cv2.threshold(corte, 125, 255, cv2.THRESH_BINARY)
        elif opcion == '2':
                _, binaria_im = cv2.threshold(corte, 125, 255, cv2.THRESH_BINARY_INV)
        elif opcion == '3':
                _, binaria_im = cv2.threshold(corte, 125, 255, cv2.THRESH_TRUNC)
        elif opcion == '4':
                _, binaria_im = cv2.threshold(corte, 125, 255, cv2.THRESH_TOZERO)
        elif opcion == '5':
                _, binaria_im = cv2.threshold(corte, 125, 255, cv2.THRESH_TOZERO_INV)
        else:
                print(f"Opción no válida")


        # Crear kernel para transformacion morfologica
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        # Aplicar operación morfológica
        morphed_im = cv2.morphologyEx(binaria_im, cv2.MORPH_GRADIENT, kernel, iterations=1)

        # Convertir a GRB para dibujo de forma y texto en color blanco
        rgb_img = cv2.cvtColor(morphed_im, cv2.COLOR_GRAY2BGR)

        h, w = rgb_img.shape[:2]
        center = (w // 2, h // 2)

        # Dibujar forma y poner texto dentro
        if shape_choice == 1:
                # Círculo
                img = cv2.circle(rgb_img, center, 100, (0,0,255), -1)
                shape_height = 200  # Altura del círculo
        elif shape_choice == 2:
                # Cuadrado
                top_left = (center[0] - 100, center[1] - 100)
                bottom_right = (center[0] + 100, center[1] + 100)
                img = cv2.rectangle(rgb_img, top_left, bottom_right,(255,0,0), -1)
                
        else:
                print(f"Forma no válida")

        #Texto a dibujar
        text1 = "Imagen binarizada"
        text2 = "Umbral: 125 " #fijo
        text3 = f"Kernel: {kernel_size}X{kernel_size}"

        # Dibujar texto  encima de la imagen dentro de la forma
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_color = (0, 255, 255) #amarillo
        line_type = 2


        x_text = center[0] - 80
        y_text = center[1] - 10
        cv2.putText(img, text1 , (x_text, y_text), font, font_scale, font_color, line_type, cv2.LINE_AA)
        cv2.putText(img, text2, (x_text, y_text + 30), font, font_scale, font_color, line_type, cv2.LINE_AA)
        cv2.putText(img, text3 , (x_text, y_text + 60), font, font_scale, font_color, line_type, cv2.LINE_AA)

        # Guardar imagen resultante
        output_filename = f"_binarized.png"
        cv2.imwrite(output_filename, rgb_img)
        print(f"Imagen procesada y guardada: {output_filename}")

        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()