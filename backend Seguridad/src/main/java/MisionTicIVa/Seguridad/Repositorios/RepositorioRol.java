package MisionTicIVa.Seguridad.Repositorios;

import MisionTicIVa.Seguridad.Modelos.Rol;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface RepositorioRol  extends
        MongoRepository<Rol,String> {
}
