
from datetime import datetime
origen = "prestamos.lfa"
destino = "reportes.html"


class Prestamos:
    #clase prestamos
    def __init__(self, id_usuario, nombre_usuario, id_libro, titulo_libro, fecha_prestamo, fecha_devolucion):
        self.id_usuario = id_usuario
        self.nombre_usuario =  nombre_usuario
        self.id_libro=id_libro
        self.titulo_libro=titulo_libro
        self.fecha_prestamo=fecha_prestamo
        self.fecha_devolucion=fecha_devolucion
    
#alfabeto que va a aceptar
Alfabeto = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"abcdefghijklmnopqrstuvwxyz"
"0123456789"
"ÁÉÍÓÚáéíóúÑñÜü"
" ,.-@()"
)



Alfabeto_permitido = set(Alfabeto)

#metodo que devuelve si es valido o no
def Validar_Alfabeto(linea:str, linea_error:int ):
    valido = True
    for i, x in enumerate(linea, start=1):
        #si no esta en el alfabeto y este no es un salto devuelve el error
        if x in ("\n","\r"):
            continue #continua al siguiente bloque
        if x not in Alfabeto_permitido:
            #si no esta en el alfabeto tira el error
            print(f"Error en linea {linea_error}, indice: {i} caracter no permitido {x}")
            valido=False

    return valido

#metodo que valida la estructura de la fecha
def ValidarFecha(fecha: str) -> bool:
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

prestamos = []

def cargar_prestamos(archivo):
    with open(archivo,"r", encoding="utf-8") as f:
        linea_num = 0;
        for linea in f:
            linea_num+=1
            linea = linea.strip()

            if not Validar_Alfabeto(linea, linea_num):
                continue #continua a la siguiente linea

            partes = linea.split(",") #separa id, nombre, idlibro etc

            if len(partes)!=6: #verifica que haya los 6 datos esperados
                print(f"Error en la linea {linea_num}, cantidad de campos incorrectos")
                continue #si es incorrecto solo tira el error y sigue a el siguiente bloque

            #asignamos las partes
            id_usuario, nombre_usuario, id_libro, titulo_libro, fecha_prestamo, fecha_devolucion = partes

            if not ValidarFecha(fecha_prestamo) or not ValidarFecha(fecha_devolucion):
                print(f"Error en la linea {linea_num}, formato de fecha incorrecto")
                continue

            p = Prestamos(id_usuario.strip(), nombre_usuario.strip(), id_libro.strip(), titulo_libro.strip(), 
                          fecha_prestamo.strip(), fecha_devolucion.strip())

  
            prestamos.append(p)

def historial_prestamos():
    html = "<h2>Historial de Prestamos</h2><pre>"
    html += "ID Usuario | Nombre | ID Libro | Titulo | Fecha Prestamo | Fecha Devolucion\n"
    html += "-"*70 + "\n"
    for p in prestamos:
        html += f"{p.id_usuario} | {p.nombre_usuario} | {p.id_libro} | {p.titulo_libro} | {p.fecha_prestamo} | {p.fecha_devolucion}\n"
    html += "</pre>\n"
    return html

def listado_usuario():
    #guardamos los usuarios por su clave y valor (id y nombre)
    usuarios = {}
    for elemento in prestamos:
        usuarios[elemento.id_usuario] = elemento.nombre_usuario
    html = "<h2>Listado de Usuarios</h2><pre>"
    html += "ID Usuario | Nombre\n"
    html += "-"*30 + "\n"
    for uid, nombre in usuarios.items():
        html += f"{uid} | {nombre}\n"
    html += "</pre>\n"
    return html

def listado_libros():
    #guardamos los libros por su clave y valor (id y titulo)
    libros = {}
    for elemento in prestamos:
        libros[elemento.id_libro] = elemento.titulo_libro
    html = "<h2>Listado de Libros Prestados</h2><pre>"
    html += "ID Libro | Titulo\n"
    html += "-"*30 + "\n"
    for lid, titulo in libros.items():
        html += f"{lid} | {titulo}\n"
    html += "</pre>\n"
    return html

def estadisticas():
    total_prestado = len(prestamos)

    conteo_libros = {}
    for elemento in prestamos:
        conteo_libros[elemento.titulo_libro]=conteo_libros.get(elemento.titulo_libro, 0)+1
        #busca la clave mas grande dentro del conteo de libros y retorna el valor si esta vacio solo devuelve N/A
    libro_mas_prestado = max(conteo_libros, key=conteo_libros.get) if conteo_libros else "N/A"

    conteo_usuarios = {}
    for elemento in prestamos:
        conteo_usuarios[elemento.nombre_usuario] = conteo_usuarios.get(elemento.nombre_usuario,0)+1
    usuario_mas_activo = max(conteo_usuarios, key=conteo_usuarios.get) if conteo_usuarios else "N/A"

    total = len(conteo_usuarios)

    html = "<h2>Estadisticas de Prestamos</h2><pre>"
    html += f"Total de Prestamos: {total_prestado}\n"
    html += f"Libro mas Prestado: {libro_mas_prestado}\n"
    html += f"Usuario mas Activo: {usuario_mas_activo}\n"
    html += f"Total de Usuarios Unicos: {total}\n"
    html += "</pre>\n"
    return html

def prestamos_vencidos():
    hoy = datetime.today()
    html = "<h2>Prestamos Vencidos</h2><pre>"
    html += "ID Usuario | Nombre | ID Libro | Titulo | Fecha Prestamo | Fecha Devolucion\n"
    html += "-"*70 + "\n"
    for elemento in prestamos:
        if elemento.fecha_devolucion.strip() == "":
            continue
        fecha_dev = datetime.strptime(elemento.fecha_devolucion, "%Y-%m-%d")
        if fecha_dev < hoy:
            html += f"{elemento.id_usuario} | {elemento.nombre_usuario} | {elemento.id_libro} | {elemento.titulo_libro} | {elemento.fecha_prestamo} | {elemento.fecha_devolucion}\n"
    html += "</pre>\n"
    return html

opc = 1
ArchivoSeCargo = False #El archivo inicia el programa sin cargarse
if __name__ == "__main__":
    with open(destino,"w+", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Reporte de Prestamos</title></head><body>")
        f.write("<h1>Reporte de Biblioteca</h1>")
        while(opc!=7):
            print("Ingrese la opcion que desea realizar:\n1.Cargar Archivo\n2.General Historial\n3.Listado de usuarios\n4.Listado de libros\n5.Estadisticas\n6.Generar Prestamos vencidos\n7.Salir")
            try:
                opc = int(input("Eleccion: "))
            except ValueError:
                print("Error intento ingresar un simbolo invalido\n")
            if opc == 1:
                cargar_prestamos(origen)
                ArchivoSeCargo = True
                print("Archivo cargado correctamente.\n")
            elif opc ==2:
                if ArchivoSeCargo == True:
                    f.write(historial_prestamos())
                    print("Historial de reportes guardado correctamente.\n")
                else:
                    print("No se ha inicializado aun el archivo\n")
            elif opc==3:
                if ArchivoSeCargo == True:
                    f.write(listado_usuario())
                    print("Lista de usuarios guardado correctamente.\n")
                else:
                    print("No se ha inicializado aun el archivo\n")
            elif opc==4:
                if ArchivoSeCargo == True:
                    f.write(listado_libros())
                    print("Lista de Libros guardado correctamente.\n")
                else:
                    print("No se ha inicializado aun el archivo\n")
            elif opc==5:
                if ArchivoSeCargo == True:
                    f.write(estadisticas())
                    print("Estadisticas guardadas correctamente.\n")
                else:
                    print("No se ha inicializado aun el archivo\n")
            elif opc==6:
                if ArchivoSeCargo == True:
                    f.write(prestamos_vencidos())
                    print("Lista de prestamos vencidos correctamente.\n")
                else:
                    print("No se ha inicializado aun el archivo\n")
            elif opc==7:
                print("Saliendo...")
            else:
                print("Error opcion invalida\n")

        f.write("</body></html>")


