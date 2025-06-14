from clases import Procesador, Paciente, ProcesadorPNG

if __name__ == "__main__":
    # Instanciar el procesador de DICOM
    procesador = Procesador()

    # Cargar los archivos desde la carpeta "Datos"
    carpeta = "Datos"
    slices = procesador.cargar_serie_dicom(carpeta)

    # Reconstruir el volumen 3D
    volumen_3d = procesador.reconstruir_3d(slices)

    # Mostrar cortes axiales/coronales/sagitales
    procesador.mostrar_cortes(volumen_3d)

    # Crear lista de pacientes (por ahora uno solo)
    pacientes = []
    paciente = Paciente(ds=slices[0], im_3d=volumen_3d)
    pacientes.append(paciente)

    # Mostrar datos del paciente
    print("\nDatos del paciente cargado:")
    print(f"ID: {paciente.id_}")
    print(f"Nombre: {paciente.nombre}")
    print(f"Edad: {paciente.edad}")
    print(f"Volumen 3D shape: {paciente.imagen.shape}")

    # ProcesadorPNG: seleccionar y mostrar la imagen del paciente
    procesador_png = ProcesadorPNG()
    imagen = procesador_png.im_original(pacientes)

    # Mostrar un corte axial del volumen 3D
    import matplotlib.pyplot as plt
    corte_axial = imagen[imagen.shape[0] // 2]  # Corte medio
    plt.imshow(corte_axial, cmap='gray')
    plt.title("Corte axial del paciente seleccionado")
    plt.axis('off')
    plt.show()

    procesador_png.traslación(corte_axial)
