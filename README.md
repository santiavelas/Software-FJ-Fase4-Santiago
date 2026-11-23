# Software FJ - Gestión de clientes, servicios y reservas

Proyecto académico en Python para el componente práctico del curso Programación (213023). La solución está organizada en módulos y demuestra programación orientada a objetos y manejo avanzado de excepciones.

## Enfoque de la solución

La aplicación funciona desde la terminal y utiliza únicamente la biblioteca estándar de Python. No incorpora una interfaz gráfica ni una base de datos. La información de clientes, servicios y reservas se conserva en listas internas mientras el programa está en ejecución. El único archivo que se escribe es el registro de eventos y errores: `logs/software_fj.log`.

El sistema simula tres servicios especializados:

- **Reserva de salas:** valida la capacidad máxima de asistentes.
- **Alquiler de equipos:** controla existencias y las devuelve al cancelar o procesar una reserva.
- **Asesoría especializada:** valida el tema de la consulta y calcula el costo por hora.

## Requisitos

- Python 3.10 o superior.
- No requiere instalar paquetes externos.

## Estructura modular

```text
Software_FJ_Entrega_Individual/
├── main.py
├── software_fj/
│   ├── __init__.py
│   ├── entidades.py
│   ├── excepciones.py
│   ├── logging_config.py
│   ├── reservas.py
│   ├── servicios.py
│   ├── sistema.py
│   └── validaciones.py
├── tests/
│   └── test_software_fj.py
├── logs/
│   ├── .gitkeep
│   └── software_fj.log
├── README.md
├── Resultado_Pruebas.txt
└── Ejecucion_Demostracion.txt
```

## Ejecutar el sistema

Abre una terminal en la carpeta principal y ejecuta:

```bash
python main.py
```

El programa presenta la fecha y hora de ejecución y realiza una demostración de 23 operaciones válidas e inválidas. Cada operación tiene su propio control de errores; al finalizar se muestra el resumen y se conserva el registro en `logs/software_fj.log`.

## Ejecutar las pruebas automatizadas

```bash
python -m unittest discover -s tests -v
```

La batería incluida contiene 13 pruebas de validación de clientes, capacidad de salas, inventario, estados de reserva, cálculo de tarifas y encadenamiento de excepciones.

## Relación con los requisitos del Anexo 3

| Requisito | Implementación |
|---|---|
| Clase abstracta de entidades | `Entidad`, en `software_fj/entidades.py` |
| Cliente con encapsulación y validaciones | `Cliente`, en `software_fj/entidades.py` |
| Servicio abstracto y tres derivados | `Servicio`, `ServicioSala`, `ServicioEquipo`, `ServicioAsesoria`, en `servicios.py` |
| Reserva con cliente, servicio, duración y estado | `Reserva`, en `reservas.py` |
| Métodos con variantes de cálculo | `calcular_total()` y `calcular_costo()` aceptan impuesto y descuento opcionales |
| Excepciones personalizadas | `software_fj/excepciones.py` |
| `try/except`, `else` y `finally` | `ejecutar_operacion()` en `main.py` |
| Encadenamiento de excepciones | `validar_numero_positivo()` y `validar_porcentaje()` |
| Registro de eventos y errores | `software_fj/logging_config.py` y `logs/software_fj.log` |
| Diez o más operaciones | 23 operaciones de demostración |

### Nota sobre la sobrecarga en Python

Python no permite definir varias implementaciones de un método con el mismo nombre y diferentes firmas de forma idéntica a Java o C++. Para cubrir la variante indicada en el enunciado, el cálculo utiliza parámetros opcionales: costo base, costo con impuesto y costo con impuesto y descuento. Por ejemplo:

```python
reserva.calcular_total()
reserva.calcular_total(impuesto=0.19)
reserva.calcular_total(impuesto=0.19, descuento=0.10)
```

## Tarifas de demostración

Los valores monetarios del ejemplo son ilustrativos y se utilizan únicamente para comprobar las operaciones. No corresponden a tarifas oficiales de Software FJ.

## Publicación en GitHub

La guía de la actividad solicita trabajar en el repositorio del grupo. No se incluye una URL inventada: antes de entregar, se debe utilizar el repositorio autorizado por el tutor o confirmar si se permite una copia individual. Revisa `INSTRUCCIONES_GITHUB.md` antes de publicar el proyecto.
