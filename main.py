from clases import Procesador, Paciente, ProcesadorPNG
import os
import cv2
import pydicom
# Diccionarios 
diccionario_pacientes = {}  # clave-id, valor-bjeto Paciente
diccionario_archivos = {} # clave-name, valor-dicom
imagenesNuevas= {}

if __name__ == "__main__":

    while True:
        menu = input('''
        1. Procesamiento de archivos DICOM
        2. Ingresar Paciente
        3. Ingresar imágenes jpg o png
        4. Transformación de imágenes
        5. Gestión y manipulación de imágenes 
        6. Salir
        ''')


        if menu == '1':
            procesador = Procesador()
            carpeta = input("Ruta de la carpeta DICOM: ")
            slices = procesador.cargar_serie_dicom(carpeta)
            volumen = procesador.reconstruir_3d(slices)
            clave = input("Ingrese clave con la que guardará estos datos: ")
            diccionario_archivos[clave] = {"slices": slices, "volumen": volumen}
            print(f"DICOM guardado con clave '{clave}'.")
            


        elif menu == '2':
            clave = input("Clave del DICOM ya procesado: ")
            if clave not in diccionario_archivos:
                print("No se encontró ese DICOM.")
                continue
            slices = diccionario_archivos[clave]["slices"]
            volumen = diccionario_archivos[clave]["volumen"]
            ds = slices[0]
            paciente = Paciente(ds, volumen)
            diccionario_pacientes[paciente.id_] = paciente
            print(f"Paciente '{paciente.nombre}' registrado con ID '{paciente.id_}'.")

   
        elif menu == '3':

            ruta = input('Ingrese la ruta de la imagen JPG o PNG:')

            if not os.path.exists(ruta):
                print('Ruta inválida.')

            nombre = input('Asignele un nombre: ')

            if ruta.lower().endswith('.dcm'):
                    try:
                        ds = pydicom.dcmread(ruta)
                        imagenesNuevas[nombre]= ds.pixel_array
                    except Exception as e:
                        print(f'Error')

            elif ruta.lower().endswith(('.jpg', '.png')):
                img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
                
            else:
                print('No se pudo cargar la imagen.')

                
            imagenesNuevas[nombre] = img
            print(f"Imagen cargada exitosamente.")


        elif menu == '4':
                procesador = ProcesadorPNG()
                #Mostrar imagen original
                imagen = procesador.im_original(diccionario_pacientes)
    
                procesador.traslación(imagen)

                

                procesador = ProcesadorPNG()
                corte = diccionario_pacientes[0].imagen 
                procesador.tranf(corte)

        elif menu == '5':
                procesador = ProcesadorPNG()
                corte = diccionario_pacientes[0].imagen 
                procesador.tranf(corte)
                

        elif menu == '6':
            print('cerrando menu...')
            break



    
