# DXCU-CgroupsV2
---------------------------------------------------------------------------------
Limita el consumo de CPU y RAM por Usuario o Grupo de S.O , utilizando cgroupsV2
---------------------------------------------------------------------------------
--------------------------
El script se ejecuta con: bash dcxu.sh 
--------------------------
Recordar ejecutarlo como usuario root



----------------
Algunos Ejemplos
----------------
**Ejemplo 1: Configurar Limitaciones para uno o varios usuarios

1) bash dcxu.sh
2) presionamos "A" -> "Limitar Consumo"
3) escribimos el nombre del usuario a limitar
4) presionamos "1"
5) Escribimos el limite del CPU, ejemplo 5 para 5%, 50 para 50% etc, solo el numero en ese formato, en este caso "50"
6) Escribimos el limite de RAM, en este caso "1" (para 1 GB)


***Ejemplo 2: Configurar 1 GB de ram como uso maximo y 75% del uso del cpu para el grupo "pepito" (anteriormente tenemos que tener este grupo creado y sus usuarios en el, igualmente hay un apartado para hacer esto si te quedase mas practico desde el shell)

1) bash dcxu.sh
2) presionamos "A" -> "Limitar Consumo"
3) presionamos "X" -> nos va a mostrar un menu para elegir el usuario a limitar , pero en este caso, queremos limitar un grupo, por lo tanto presionamos X para "otras opciones"
4) presionamos "1" -> esto nos da 2 opciones : *Opcion 1 El consumo total del grupo no va a superar los limites establecidos No se puede establecer limites individuales, a miembros que pertenezcan a este grupo el limite es para todo el grupo
                                                *Opcion 2 Esta opcion genera limites para todos los usuarios de un grupo, pero lo hace de manera individual(no como grupo), es decir es como agregar todos los usuarios manualmente (pero para hacerlo mas rapido)
                                                Y a todos ponerles los mismos limites, los cuales podemos ir editando uno a uno de quererlo, no estas limitando un grupo por ejemplo al 75% , estas limitando a cada persona y
                                                diferente seria que el consumo total del grupo no supere el 75%

5) presionamos "1" nuevamente -> escribimos el nombre del grupo a limitar
6) Ingresar "75" (porcentaje de CPU maximo a asignar) ejemplo: 1 para 1%, 20 para 20%, 75 para 75%, en este caso ingreso 75, en ese formato solo el numero
7) ¿Desea limitar la RAM? (s/n): (aca si ponemos "n" no va a haber una limitacion sobre la memoria RAM, si ponemos  "s" entonces podemos poner "1" para 1 GB, "2" para 2GB, ETC, en ese formato solo el numero
8) Presionamos "A" (Pronto, una vez en el menu inicial del script (dcxu.sh) y ya con la configuracion generada, vamos a ir a "A" nuevamente
9) Presionamos "X"
10) Presionamos "5" y ahora se aplicara la configuracion que generamos para el grupo anteriormente

***Ejemplo 3: Restaurar la configuracion de LIMITACION un usuario en especifico
1) bash dcxu.sh
2) presionamos "A"
3) escribimos el nombre del usuario
4) presionamos "4"


***Ejemplo 4: Eliminar limitaciones a un usuario , (dejarlo normal)

1) bash dcxu.sh
2) presionamos "A"
3) escribimos el nombre del usuario
4) presionamos "2"


***Ejemplo 5: Restaurar/Aplicar Limites a todos los usuarios o grupos

1) bash dcxu.sh
2) presionamos "A"
3) presionamos "X"
4) presionamos "5"

***Ejemplo 6: Eliminar configuracion de Limites a todos los usuarios o grupos

1) bash dcxu.sh
2) presionamos "A"
3) presionamos "X"
4) presionamos "6"

------------------------------------
PRUEBAS DE ESTRES DE CPU EXPLICACION
------------------------------------
bash dcxu.sh (como root)

la OPCION "1" nos permite saturar 1 nucleo con el usuario especificado
la OPCION "2" nos permite saturar los nucleos que quieramos con el usuario especificado
la OPCION "T" nos permite saturar un nucleo con todos los usuarios al mismo tiempo

la OPCION "3" va a cancelar el estres del CPU de todos los usuarios que lo esten saturando
la OPCION "4" va a cancelar el estres del CPU de un usuario especificado, permitiendo que las pruebas de estres de otros usuarios permanezcan


------------------
Datos Adicionales
------------------

Opcion "5" y "6" nos permite ver las LIMITACIONES ACTIVAS tanto para grupos como para usuarios
la opcion "H" es simplemente un atajo a HTOP , la OPCION U, es mas basico ya que no usa htop y no necesitas instalarlo, pero esta centrado en un usuario especifico
la opcion "R" es una manera rapida de hacer un respaldo de la carpeta "./config" y la opcion "G"  es una manera mas rapida de ir al script de limitar grupos en lugar de tener que acceder desde el script de la opcion "A"

la opcion "0" es para salir", en el script se puede agregar arriba del todo "clear" en caso que les quede mas lindo visualmente, ya que el script se ejecuta en bucle hasta no utilizar salir.

--------------------------------------------------------------------------------------------------------
Version para sistemas con mayor restriccion a nivel kernel: https://github.com/Oscuro21/DXCU2-CgroupsV2-
--------------------------------------------------------------------------------------------------------

--------------------------------------------------------------------------
Script para saturar la memoria RAM: https://github.com/Oscuro21/SaturarRAM
se debe ejecutar con el usuario que desean probar sus limitaciones
--------------------------------------------------------------------------


-----------
Explicacion
-----------
Podemos aplicar por ejemplo un maximo de 75% de uso de CPU a uno o varios usuarios, o podemos aplicar el 75% entre todos los integrantes de un grupo, (75 o el valor deseado)
Cada Configuracion de limitacion de CPU y/o RAM se guarda en "./config"
Dentro de la misma se genera una carpeta con el nombre de cada usuario o nombre del grupo del sistema con un archivo .txt que tiene las limitaciones
una vez ya tenemos la configuracion en ./config , podemos aplicar la configuracion , o restaurarla , ya que al reiniciar el equipo esta se va, (se puede programar una tarea o crontab para que eso no ocurra)

cgroupsv2 se encarga de asignar los recursos a los procesos
ademas creamos una tarea en systemd que se ejecuta cada 2 seg, moviendo los procesos del grupo o usuario a la configuracion que creamos en cgroups para mantener los procesos limitados.
Los archivos en  /sys/fs/cgroup/$nombre_usuario o  /sys/fs/cgroup/$nombre_grupo , una vez reiniciado el servidor se restablecen por default, a diferencia de los de systemd que no se eliminan,
por eso el programa genera la carpeta .config para poder restaurar las configuraciones en /sys/fs/cgroup/, los archivos en .config tambien los utiliza el programa para en caso de querer borrar
las limitaciones , tambien identificar que archivos de systemd debe eliminar. 

En caso de necesitar que se aplique la limitacion automaticamente despues de cada reinicio, se puede simplemente poner la funcion de la opcion "5" en un script nuevo que contenga:


restaurar_configuracion() {
    local usuario=$1
    local config_file="$CONFIG_DIR/$usuario/config.txt"
    if [ -f "$config_file" ]; then
        source "$config_file"
        echo "Restaurando límites para $usuario: CPU=$CPU_MAX, RAM=$MEMORY_MAX"
        asignar_limites "$usuario" "$((CPU_MAX / 1000))" "$MEMORY_MAX"
    else
        echo "No hay configuración guardada para $usuario."
    fi
}


restaurar_todos() {
    for usuario in $(ls "$CONFIG_DIR"); do
        restaurar_configuracion "$usuario"
    done
}









