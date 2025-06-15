from clases import Procesador, Paciente, ProcesadorPNG
import os
import cv2
import pydicom
# Diccionarios 
diccionario_pacientes = {} 
diccionario_dicom = {} 
imagenesNuevas= {}

if __name__ == "__main__":

    while True:
        menu = input('''
        1. Procesamiento de archivos DICOM
        2. Ingresar Paciente
        3. Ingresar imágenes jpg o png
        4. Translación de imágenes
        5. Binarización, Tranformación morfologíca y dibujo de figuras 
        6. Salir
        ''')


        if menu == '1':
            procesador = Procesador()
            ruta = input('Escriba ruta:')
            archivos = procesador.cargar_serie_dicom(ruta)
            volumen_3d = procesador.reconstruir_3d(archivos)
            procesador.mostrar_cortes(volumen_3d)

            clave = input("Ingrese un nombre clave para guardar esta serie DICOM: ")
            diccionario_dicom[clave] = {
                "slices": archivos,
                "volumen": volumen_3d
}


        elif menu == '2':
            clave = input("Clave del DICOM ya procesado: ")
            if clave not in diccionario_dicom:
                print("No se encontró ese DICOM.")
                continue
            slices = diccionario_dicom[clave]["slices"]
            volumen = diccionario_dicom[clave]["volumen"]
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
                imagen = procesador.im_original(diccionario_pacientes)

                if imagen is not None:
                    procesador.traslación(imagen)

                


        elif menu == '5':
                procesador = ProcesadorPNG()
                procesador.tranf(diccionario_pacientes)
         

        elif menu == '6':
            print('cerrando menú...')
            break



    
