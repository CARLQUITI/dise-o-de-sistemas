# PSet 2: Patrones de Diseño en ReservaU

## Tabla de Patrones
| Patrón / Mecanismo | Requerimiento que lo justifica | Problema que resuelve | Clases y métodos |
| :--- | :--- | :--- | :--- |
| **Factory Method** | RF (Creación reservas) | Centraliza la creación de reservas según el tipo de solicitante, asignando automáticamente la política de cancelación correcta sin usar condicionales if-else. | `ReservaFactory`, `FabricaReservaEstudiante`, `FabricaReservaCapitan` |
| **Abstract Factory** | RF-14 (Sedes) | Evita que el código cliente mezcle un Validador de Horario del Campus Norte con un Canal de Notificación del Campus Sur. Agrupa familias de objetos. | `SedeNorteFactory`, `SedeSurFactory`, `ValidadorHorario`, `Notificador` |
| **Builder** | RF-09 (Res. Recurrente) | Separa la construcción de una solicitud compleja (con datos obligatorios y opcionales como equipo/notas) de su representación, permitiendo validar las semanas (2 a 8) antes de instanciar. | `BuilderReservaRecurrente`, `ReservaRecurrente` |
| **Prototype** | RF-13 (Bloqueos) | Permite definir la configuración de un bloqueo (motivo, equipo) una sola vez como plantilla, clonándola rápidamente para múltiples canchas y fechas. | `Bloqueo.clone()` |
| **Singleton** | RNF-02 (Centralización) | Garantiza que las reglas de negocio (tiempos de cancelación, límite de no-shows) vivan en una única instancia global accesible por todo el sistema, evitando valores hardcodeados. | `ConfiguracionReglas` |
| **Strategy** | RF-10, 11, 12 (Políticas) | Permite cambiar el algoritmo de cálculo de penalidad de cancelación dinámicamente. Evita que la clase `Reserva` tenga un switch gigante para saber cómo cancelarse. | `PoliticaCancelacion`, `CancelacionEstudiante`, `CancelacionCapitan`, `CancelacionAdmin` |
| **Facade** | RF (Operaciones core) | Provee una interfaz unificada y simplificada (`reservar`, `reservar_recurrente`, `cancelar`, `bloquear`) para que el cliente no interactúe directamente con subsistemas complejos. | `ReservaFacade` |
| **Concurrencia** | RNF-01 (Doble reserva) | Protege la sección crítica de validación y registro, evitando inconsistencias cuando dos usuarios intentan reservar la misma cancha al mismo milisegundo. | `threading.Lock()` en `ReservaFacade` |

## Justificaciones de Diseño

**1. Prototype: copy vs deepcopy**
Para la clase `Bloqueo` se utilizó `copy.copy()` (copia superficial). Dado que los atributos de la plantilla actual son tipos inmutables en Python (Strings para motivo, franja, equipo), una copia superficial es suficiente, eficiente y segura para reasignar la cancha y fecha del clon sin afectar a la plantilla original.

**2. Singleton: Beneficios y Costos**
*Beneficio:* Centraliza la "verdad" de las métricas del negocio. Si Tecnología necesita cambiar la suspensión a 14 días, se cambia en un solo lugar.
*Costo:* Introduce acoplamiento global. Las clases de dominio como `Solicitante` ahora dependen de un estado global, lo que puede dificultar ligeramente las pruebas unitarias aisladas en un futuro.

**3. Concurrencia: Elección de Locking**
Se utilizó Locking Pesimista (`threading.Lock()`). En el contexto de ReservaU, donde hay picos masivos de escritura al inicio del semestre (todos los estudiantes peleando por las canchas en la franja de la noche), los conflictos y "colisiones" son altamente probables. El bloqueo pesimista garantiza la exclusión mutua en la iteración de búsqueda de disponibilidad y escritura, asegurando consistencia absoluta (atomicidad) con bajo costo de implementación.

**4. Trazabilidad: Regla de los 3 No-Shows**
* **Requerimiento:** RF-12 (Nuevo). Tres no-shows en un mismo mes calendario derivan en 7 días de suspensión.
* **Caso de Uso y Diagrama:** Aparece en el flujo alterno del Caso de Uso de Cancelación, y gráficamente en el **Diagrama de Robustez** (paso 5).
* **Entidad y Método:** Entidad `Solicitante`, método `registrar_no_show()`.
* **Configuración:** Lee `limite_no_shows` (3) y `dias_suspension` (7 días) de la clase Singleton `ConfiguracionReglas`.
* **Línea de Simulación:** En el *Escenario 5* de `simulacion.py`, se observan las inserciones de no-shows con fechas del mismo mes, cambiando el estado de `esta_suspendido` a True, e impidiendo su reserva posterior.
