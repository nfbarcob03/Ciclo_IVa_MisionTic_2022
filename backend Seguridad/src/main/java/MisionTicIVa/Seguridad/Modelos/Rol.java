package MisionTicIVa.Seguridad.Modelos;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document()
public class Rol {
    @Id
    private String _id;
    private String nombre;
    private String descripcion;
}
