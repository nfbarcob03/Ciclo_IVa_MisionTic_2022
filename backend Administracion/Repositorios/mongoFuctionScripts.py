def mongoGroup(id,fielName, aggregationFuction, fialdAgregation):
    return {
        '$group': {
            '_id': id,
            fielName: {
                aggregationFuction: fialdAgregation
            }
        }
    }

def mongoLookUp(fromColletion, localField, foreignField, alias):
    return {
        '$lookup': {
            'from': fromColletion,
            'localField': localField,
            'foreignField': foreignField,
            'as': alias
        }
    }

def mongoSet(fieldName, expresion):
    return {
        '$set': {
            fieldName: expresion
        }
    }

def mongoAddFields(fieldName, expresion):
    return {
        '$addFields': {
            fieldName: expresion
        }
    }
def mongoSort(fieldName, ascending = False):
    order = 1 if ascending else -1
    return {
        '$sort': {
            fieldName: order
        }
    }

def mongoMatch(fieldName, expresion):
    return {
        '$match': {
            fieldName: expresion
        }
    }