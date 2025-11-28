import os

print("📍 Diagnóstico del sistema de archivos:")
print(f"Directorio actual: {os.getcwd()}")
print(f"¿Existe instance/? {os.path.exists('instance')}")

if os.path.exists('instance'):
    print("Contenido de instance/:")
    for item in os.listdir('instance'):
        print(f"  - {item}")
else:
    print("Creando directorio instance...")
    os.makedirs('instance', exist_ok=True)