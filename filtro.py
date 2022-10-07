import sys
import csv
from datetime import datetime
import os

persona=[]
personacsv=[]
ccsv=[]
cont=0
indi=0

print("")
print("_______________LISTADO DE CHEQUES_______________")
print("")

#validacion de parametros
try:
    
    if len(sys.argv) > 7:
        print("ERROR CANTIDAD INVALIDA DE PARAMETROS")
        exit()
    
    archivo=sys.argv[1]
    dni=sys.argv[2]
    salida=sys.argv[3]
    tipo_cheque=sys.argv[4]    
      
except IndexError:
    print("ERROR CANTIDAD INVALIDA DE PARAMETROS")
    exit()

estado_cheque= sys.argv[5] if len(sys.argv) > 5 else None
fecha=sys.argv[6] if len(sys.argv) > 6 else None

#validacion del archivo.csv
arc=os.path.isfile(archivo)

if arc != True:
    print("ERROR NO SE ENCUENTRA EL ARCHIVO .CSV")
    exit()
    
#validacion si el dni es un numero
try:
    dni= int(dni)

except ValueError:
    print("ERROR EL DNI NO ES UN NUMERO")
    exit()

#convierto el dni a str para usar el metodo len()
#ya que no funciona en datos tipo int
dni= str(dni)

if len(dni) != 8:
    print("ERROR CANTIDAD INCORRECTA DE CARACTERES EN EL DNI")
    exit()

#si salida no se encuentra en la lista exit
if salida not in ["pantalla","csv"]:
    print("ERROR PARAMETRO INCORRECTO EN SALIDA")
    exit()

#si tipo_cheque no se encuentra en la lista exit
if tipo_cheque not in ["EMITIDO","DEPOSITADO"]:
    print("ERROR PARAMETRO INCORRECTO EN TIPO DE CHEQUE")
    exit()

#si estado_cheque no se encuentra en la lista exit
if estado_cheque and estado_cheque not in ["PENDIENTE","APROBADO","RECHAZADO"]:
    print("ERROR PARAMETRO INCORRECTO EN ESTADO DE CHEQUE")
    exit()
    
#si fecha existe
#filtrado de fecha
if fecha:
    
    try:
        #divido decha en 2
        desde, hasta = fecha.split(":")
        
        if len(fecha.split(":")) != 2:
            print("ERROR FECHA COMPLETA INVALIDA")
            exit()

        #verifico que desde tenga 10 caracteres y tenga dos "-"
        if len(desde) != 10 or len(desde.split("-")) != 3:
            print("ERROR FECHA DESDE INVALIDA")
            exit()
            
        #verifico que hasta tenga 10 caracteres y tenga dos "-"
        if len(hasta) != 10 or len(hasta.split("-")) != 3:
            print("ERROR FECHA HASTA INVALIDA")
            exit()
            
    except ValueError:
        print("ERROR FECHA INCORRECTA")
        exit()

#conversion de fecha
    dd, dm, da = desde.split('-')
    hd, hm, ha = hasta.split('-')

    desde=datetime(int(da),int(dm),int(dd))
    hasta=datetime(int(ha),int(hm),int(hd))
    
#filtro
with open (archivo, 'r') as csvfile:
        reader=csv.reader(csvfile, delimiter=',')
        
        for i in reader:
            
            if i[6].isnumeric():
                
                emitido = int(i[6])
                depositado = int(i[7])
                emitido=datetime.fromtimestamp(emitido)
                depositado=datetime.fromtimestamp(depositado)
            
            if len(sys.argv) == 5:
                    
                if i[8] == dni and i[9] == tipo_cheque:
                    persona.append(i)
                    personacsv.append(str(emitido))
                    personacsv.append(str(depositado))
                    personacsv.append(i[5])
                    personacsv.append(i[3])
                    ccsv.append(personacsv)
                    personacsv=[]

                
            if len(sys.argv) == 6:
                    
                if i[8] == dni and i[9] == tipo_cheque and i[10] == estado_cheque:
                    persona.append(i)
                    personacsv.append(str(emitido))
                    personacsv.append(str(depositado))
                    personacsv.append(i[5])
                    personacsv.append(i[3])
                    ccsv.append(personacsv)
                    personacsv=[]
                
            if len(sys.argv) == 7: 
                
                if tipo_cheque == 'EMITIDO':
                        
                    if i[8] == dni and i[9] == tipo_cheque and i[10] == estado_cheque and emitido > desde and emitido < hasta:
                        persona.append(i)
                        personacsv.append(str(emitido))
                        personacsv.append(str(depositado))
                        personacsv.append(i[5])
                        personacsv.append(i[3])
                        ccsv.append(personacsv)
                        personacsv=[]       
                        
                if  tipo_cheque == 'DEPOSITADO':
                                    
                    if i[8] == dni and i[9] == tipo_cheque and i[10] == estado_cheque and depositado > desde and depositado < hasta:
                        persona.append(i)
                        personacsv.append(str(emitido))
                        personacsv.append(str(depositado))
                        personacsv.append(i[5])
                        personacsv.append(i[3])
                        ccsv.append(personacsv)
                        personacsv=[]

#verificacion del nro de cheque
for n in persona:
    for i in persona:
        if n[0] == i[0]:
            cont=cont+1
        if cont > 1:
            print("ERROR SE REPITE EL NRO DE CHEQUE",n[0])
            print(n)
            exit()
    cont=0

#salida de pantalla          
if salida == 'pantalla':
    print("los registros que coinciden son ")
    print("")
    for i in persona:
        print(i)

#salida csv
if salida == 'csv':
    fechaActual = datetime.now()
    fechaFile = datetime.strftime(fechaActual, "%b %d %Y")

    with open (f"{dni}-{fechaFile}.csv","w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerows(ccsv)
        print("archivo creado exitasamente")
