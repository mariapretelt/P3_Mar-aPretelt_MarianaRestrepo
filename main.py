from clases import Procesador, Paciente

if __name__ == "__main__":
    procesador = Procesador()
    carpeta = "Datos"
    slices = procesador.cargar_serie_dicom(carpeta)

    volumen_3d = procesador.reconstruir_3d(slices)
    procesador.mostrar_cortes(volumen_3d)

    # Crear paciente usando el primer slice (ds) para extraer los datos
    paciente = Paciente(ds=slices[0], im_3d=volumen_3d)

    print("\nInformación del paciente:")
    print(f"ID: {paciente.id_}")
    print(f"Nombre: {paciente.nombre}")
    print(f"Edad: {paciente.edad}")
    print(f"Tamaño del volumen 3D: {paciente.imagen.shape}")

