package com.example.pedido_service.model;

import jakarta.persistence.*;
import lombok.Data;
import java.util.Date;
import java.util.List;

@Data
@Entity
@Table(name = "tb_pedido")
public class Pedido {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idPedido;
    
    private Integer idRestaurante;
    private Integer idCliente;
    
    @Temporal(TemporalType.DATE)
    private Date dtPedido;
    
    private Double vlTotal;
    private String dsDescricao;

    @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "idPedido")
    private List<ItemPedido> itens;
}