import numpy as np

def saturar_ram():
    # Intentar consumir memoria creando grandes matrices
    data = []
    try:
        while True:
            # Creamos matrices grandes llenas de números aleatorios
            data.append(np.random.rand(1000000))  # 1 millón de elementos por vez
            print(f"Memoria consumida: {len(data)} matrices")
    except MemoryError:
        print("Memoria agotada. El sistema está saturado.")

if __name__ == "__main__":
    saturar_ram()
