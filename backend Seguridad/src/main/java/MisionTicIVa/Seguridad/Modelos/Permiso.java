package MisionTicIVa.Seguridad.Modelos;

import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document()
public class Permiso {
    private String _id;
    private String url;
    private String metodo;

}
