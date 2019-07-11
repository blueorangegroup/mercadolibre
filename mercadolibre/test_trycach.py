

class unaExcepcion(Exception):
    pass


def funcion_con_try_cach(parametro):

    try:
        if parametro == 'loop':
            raise unaExcepcion
        elif parametro == 'jodido':
            raise Exception
    except unaExcepcion:
        print('EXCEPCION UNA EXCEPCION')
        return funcion_con_try_cach('')
    except Exception:
        print('eXCEPCION OTRA EXCEPCION')
    finally:
        print('COMMITIANDO')

    print('TERMINE')


def funcion_con_for(lista, parametro):

    for elemento in lista:
        print(elemento)
        try:
            if parametro == 'error':
                raise Exception
        except Exception:
            print('ROMPILOROMPI')
            elemento = elemento

funcion_con_for(['1', '2', '3'], 'error')
