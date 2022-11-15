from Repositorios.InterfaceRepositorio import InterfaceRepositorio
from Modelos.Inscripcion import Inscripcion
from bson import ObjectId
import Repositorios.mongoFuctionScripts as mf
class RepositorioInscripcion(InterfaceRepositorio[Inscripcion]):
    def getListadoInscritosEnMateria(self, id_materia):
        theQuery = {"materia.$id": ObjectId(id_materia)}
        return self.query(theQuery)

    def getMayorNotaPorCurso(self):
        query1 = {
            "$group": {
                "_id": "$materia",
                "max": {
                    "$max": "$nota_final"
                },
                "doc": {
                    "$first": "$$ROOT"
                }
            }
        }
        pipeline = [query1]
        return self.queryAggregation(pipeline)

    def promedioNotasEnMateria(self, id_materia):
        query1 = {
            "$match": {"materia.$id": ObjectId(id_materia)}
        }
        query2 = {
            "$group": {
                "_id": "$materia",
                "promedio": {
                    "$avg": "$nota_final"
                }
            }
        }
        pipeline = [query1, query2]
        return self.queryAggregation(pipeline)

    def sumaNotasEnMateria(self, id_materia):
        query1 = {
            "$match": {"materia.$id": ObjectId(id_materia)}
        }
        query2 = {
            "$group": {
                "_id": "$materia",
                "promedio": {
                    "$sum": "$nota_final"
                }
            }
        }
        pipeline = [query1, query2]
        return self.queryAggregation(pipeline)

    def reporteTotalNotasPorMateriaCompleto(self,id_mesa = None):
        pipeline=[
            mf.mongoGroup('$materia','sumaNotasMateria', '$sum','$nota_final'),
            mf.mongoLookUp('materia', '_id.$id','_id',  'materia'),
            mf.mongoSet('materia', {'$first': '$materia'}),
            mf.mongoAddFields('depId', '$materia.departamento.$id'),
            mf.mongoLookUp('departamento','depId','_id','departamento'),
            mf.mongoSet('departamento', {'$first': '$departamento'}),
            mf.mongoSort('sumaNotasMateria', False)
            ]
        if id_mesa is not None:
            pipeline.insert(0,mf.mongoMatch( 'estudiante.$id',  ObjectId(id_mesa)))
        return self.queryAggregation(pipeline)

    def reporteTotalNotasPorMateriaQueryRaiz(self,id_mesa = None):
        pipeline = [
            mf.mongoGroup('$materia', 'sumaNotasMateria', '$sum', '$nota_final'),
        ]
        if id_mesa is not None:
            pipeline.insert(0, mf.mongoMatch('estudiante.$id', ObjectId(id_mesa)))
        return self.queryAggregation(pipeline)