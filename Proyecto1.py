def mostrar_menu():
    print("\nMenú de opciones:")
    print("1. Cargar Archivo")
    print("2. Procesar Archivo")
    print("3. Escribir Archivo de Salida")
    print("4. Mostrar datos del Estiudiante")
    print("5. Generar Graficas")  # También corregí el typo: "Genarar" → "Generar"
    print("6. Salir")


def main():
    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ")

        if opcion == '1':
            print("Cargar Archivo")
            # Lógica para cargar archivo
        elif opcion == '2':
            print("Procesar Archivo")
            # Lógica para procesar archivo 
        elif opcion == '3':
            print("Escribir Archivo de Salida")
            # Lógica para escribir archivo de salida
        elif opcion == '4':    
            print("Mostrar datos del Estudiante")
            # Lógica para mostrar datos del estudiante
        elif opcion == '5':
            print("Generar Graficas")
            # Lógica para generar gráficas
        elif opcion == '6':
            print("Saliendo del programa...")
            break 
        else:
            print("Opción no válida. Por favor, intente de nuevo.")


# Esta parte debe estar al final y fuera de cualquier función
if __name__ == "__main__":
    main()