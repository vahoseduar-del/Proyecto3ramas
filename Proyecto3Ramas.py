import json
import os
from datetime import datetime


ARCHIVO_DATOS = "datos_ventas.json"
IVA = 0.19


class SistemaVentas:
    def __init__(self):
        self.productos = {}
        self.ventas = []
        self.cargar_datos()

    # ---------------------------------------------------------
    # GUARDAR Y CARGAR INFORMACIÓN
    # ---------------------------------------------------------

    def cargar_datos(self):
        if os.path.exists(ARCHIVO_DATOS):
            try:
                with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
                    datos = json.load(archivo)

                self.productos = datos.get("productos", {})
                self.ventas = datos.get("ventas", [])

            except (json.JSONDecodeError, OSError):
                print("\nNo fue posible cargar los datos.")
                print("El sistema comenzará con información vacía.\n")

    def guardar_datos(self):
        datos = {
            "productos": self.productos,
            "ventas": self.ventas
        }

        try:
            with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)

        except OSError:
            print("\nNo fue posible guardar la información.")

    # ---------------------------------------------------------
    # FUNCIONES DE ENTRADA
    # ---------------------------------------------------------

    def leer_entero(self, mensaje, minimo=0):
        while True:
            try:
                valor = int(input(mensaje))

                if valor < minimo:
                    print(f"Debe ingresar un número mayor o igual a {minimo}.")
                    continue

                return valor

            except ValueError:
                print("Entrada no válida. Por favor escriba un número entero.")

    def leer_decimal(self, mensaje, minimo=0):
        while True:
            try:
                valor = float(input(mensaje))

                if valor < minimo:
                    print(f"El valor debe ser mayor o igual a {minimo}.")
                    continue

                return valor

            except ValueError:
                print("Entrada no válida. Por favor escriba un número.")

    # ---------------------------------------------------------
    # PRODUCTOS
    # ---------------------------------------------------------

    def agregar_producto(self):
        print("\n========== AGREGAR PRODUCTO ==========")

        nombre = input("Nombre del producto: ").strip()

        if not nombre:
            print("El nombre no puede estar vacío.")
            return

        nombre = nombre.title()

        if nombre in self.productos:
            print("Ese producto ya existe.")
            return

        precio = self.leer_decimal("Precio: $")
        cantidad = self.leer_entero("Cantidad disponible: ", 0)

        self.productos[nombre] = {
            "precio": precio,
            "cantidad": cantidad
        }

        self.guardar_datos()

        print("\nProducto registrado correctamente.")
        print(f"Producto: {nombre}")
        print(f"Precio: ${precio:,.2f}")
        print(f"Cantidad: {cantidad}")

    def listar_productos(self):
        print("\n========== PRODUCTOS DISPONIBLES ==========")

        if not self.productos:
            print("No hay productos registrados.")
            return

        print("\nProducto                 Precio        Cantidad")
        print("-" * 55)

        for nombre, datos in self.productos.items():
            print(
                f"{nombre:<24} "
                f"${datos['precio']:>10,.2f} "
                f"{datos['cantidad']:>10}"
            )

    def buscar_producto(self):
        print("\n========== BUSCAR PRODUCTO ==========")

        palabra = input("Escriba el nombre o parte del nombre: ").strip().lower()

        encontrados = []

        for nombre, datos in self.productos.items():
            if palabra in nombre.lower():
                encontrados.append((nombre, datos))

        if not encontrados:
            print("No se encontraron productos.")
            return

        print("\nResultados:")

        for nombre, datos in encontrados:
            print(
                f"- {nombre}: ${datos['precio']:,.2f} "
                f"| Disponible: {datos['cantidad']}"
            )

    def modificar_producto(self):
        print("\n========== MODIFICAR PRODUCTO ==========")

        if not self.productos:
            print("No hay productos registrados.")
            return

        self.listar_productos()

        nombre = input("\nProducto que desea modificar: ").strip().title()

        if nombre not in self.productos:
            print("Producto no encontrado.")
            return

        nuevo_precio = self.leer_decimal("Nuevo precio: $")
        nueva_cantidad = self.leer_entero("Nueva cantidad: ", 0)

        self.productos[nombre]["precio"] = nuevo_precio
        self.productos[nombre]["cantidad"] = nueva_cantidad

        self.guardar_datos()

        print("\nProducto actualizado correctamente.")

    def eliminar_producto(self):
        print("\n========== ELIMINAR PRODUCTO ==========")

        if not self.productos:
            print("No hay productos registrados.")
            return

        self.listar_productos()

        nombre = input("\nProducto que desea eliminar: ").strip().title()

        if nombre not in self.productos:
            print("Producto no encontrado.")
            return

        confirmar = input(
            f"¿Está seguro de eliminar '{nombre}'? (S/N): "
        ).strip().upper()

        if confirmar == "S":
            del self.productos[nombre]
            self.guardar_datos()
            print("Producto eliminado correctamente.")
        else:
            print("Operación cancelada.")

    # ---------------------------------------------------------
    # VENTAS
    # ---------------------------------------------------------

    def realizar_venta(self):
        print("\n========== NUEVA VENTA ==========")

        if not self.productos:
            print("No existen productos registrados.")
            return

        carrito = {}

        while True:

            self.listar_productos()

            nombre = input(
                "\nProducto a vender (ENTER para finalizar): "
            ).strip().title()

            if not nombre:
                break

            if nombre not in self.productos:
                print("Producto no encontrado.")
                continue

            disponible = self.productos[nombre]["cantidad"]

            if disponible <= 0:
                print("Este producto está agotado.")
                continue

            cantidad = self.leer_entero(
                f"Cantidad (disponible {disponible}): ",
                1
            )

            if cantidad > disponible:
                print("No hay suficiente inventario.")
                continue

            carrito[nombre] = carrito.get(nombre, 0) + cantidad

            print(f"{cantidad} unidad(es) agregada(s).")

        if not carrito:
            print("\nNo se agregó ningún producto.")
            return

        subtotal = 0

        print("\n========== RESUMEN DE VENTA ==========")

        for nombre, cantidad in carrito.items():

            precio = self.productos[nombre]["precio"]
            total_producto = precio * cantidad

            subtotal += total_producto

            print(
                f"{nombre}: {cantidad} x ${precio:,.2f} "
                f"= ${total_producto:,.2f}"
            )

        impuesto = subtotal * IVA
        total = subtotal + impuesto

        print("-" * 50)
        print(f"Subtotal:       ${subtotal:,.2f}")
        print(f"IVA (19%):      ${impuesto:,.2f}")
        print(f"TOTAL:          ${total:,.2f}")

        confirmar = input(
            "\n¿Confirmar venta? (S/N): "
        ).strip().upper()

        if confirmar != "S":
            print("Venta cancelada.")
            return

        dinero_recibido = self.leer_decimal(
            "Dinero recibido: $",
            total
        )

        cambio = dinero_recibido - total

        for nombre, cantidad in carrito.items():
            self.productos[nombre]["cantidad"] -= cantidad

        venta = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "productos": carrito,
            "subtotal": round(subtotal, 2),
            "iva": round(impuesto, 2),
            "total": round(total, 2),
            "recibido": round(dinero_recibido, 2),
            "cambio": round(cambio, 2)
        }

        self.ventas.append(venta)

        self.guardar_datos()

        print("\n======================================")
        print("       VENTA REALIZADA")
        print("======================================")
        print(f"Total:     ${total:,.2f}")
        print(f"Recibido:  ${dinero_recibido:,.2f}")
        print(f"Cambio:    ${cambio:,.2f}")
        print("======================================")

    # ---------------------------------------------------------
    # HISTORIAL
    # ---------------------------------------------------------

    def historial_ventas(self):
        print("\n========== HISTORIAL DE VENTAS ==========")

        if not self.ventas:
            print("Todavía no existen ventas registradas.")
            return

        for numero, venta in enumerate(self.ventas, start=1):

            print(f"\nVenta #{numero}")
            print(f"Fecha: {venta['fecha']}")

            for producto, cantidad in venta["productos"].items():
                print(f"  - {producto}: {cantidad}")

            print(f"Total: ${venta['total']:,.2f}")

    # ---------------------------------------------------------
    # RESUMEN DEL NEGOCIO
    # ---------------------------------------------------------

    def resumen(self):
        print("\n========== RESUMEN DEL NEGOCIO ==========")

        cantidad_productos = len(self.productos)
        unidades = sum(
            datos["cantidad"]
            for datos in self.productos.values()
        )

        total_ventas = sum(
            venta["total"]
            for venta in self.ventas
        )

        print(f"Productos registrados: {cantidad_productos}")
        print(f"Unidades disponibles:  {unidades}")
        print(f"Ventas realizadas:     {len(self.ventas)}")
        print(f"Ingresos acumulados:   ${total_ventas:,.2f}")

    # ---------------------------------------------------------
    # ALERTAS
    # ---------------------------------------------------------

    def alertas_inventario(self):
        print("\n========== ALERTAS DE INVENTARIO ==========")

        encontrados = False

        for nombre, datos in self.productos.items():

            if datos["cantidad"] <= 5:

                encontrados = True

                print(
                    f"⚠ {nombre}: quedan "
                    f"{datos['cantidad']} unidad(es)"
                )

        if not encontrados:
            print("No existen productos con inventario bajo.")

    # ---------------------------------------------------------
    # MENÚ PRINCIPAL
    # ---------------------------------------------------------

    def ejecutar(self):

        while True:

            print("\n")
            print("=" * 60)
            print("        CONECTACAPAZ - SISTEMA DE VENTAS")
            print("=" * 60)
            print("Una herramienta para apoyar la autonomía económica")
            print("de personas con discapacidad.")
            print("=" * 60)

            print("\n1. Agregar producto")
            print("2. Ver productos")
            print("3. Buscar producto")
            print("4. Modificar producto")
            print("5. Eliminar producto")
            print("6. Realizar venta")
            print("7. Historial de ventas")
            print("8. Resumen del negocio")
            print("9. Alertas de inventario")
            print("0. Salir")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.agregar_producto()

            elif opcion == "2":
                self.listar_productos()

            elif opcion == "3":
                self.buscar_producto()

            elif opcion == "4":
                self.modificar_producto()

            elif opcion == "5":
                self.eliminar_producto()

            elif opcion == "6":
                self.realizar_venta()

            elif opcion == "7":
                self.historial_ventas()

            elif opcion == "8":
                self.resumen()

            elif opcion == "9":
                self.alertas_inventario()

            elif opcion == "0":
                print("\nGracias por utilizar ConectaCapaz.")
                print("Seguimos construyendo oportunidades.")
                break

            else:
                print("\nOpción no válida.")

            input("\nPresione ENTER para continuar...")


# ---------------------------------------------------------
# INICIO DEL PROGRAMA
# ---------------------------------------------------------

if __name__ == "__main__":
    sistema = SistemaVentas()
    sistema.ejecutar()
