package com.example.pedido_service.model;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "tbitem_pedido_produto")
public class ItemPedido {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idItem;

    private Integer idProduto;
    private Integer cdQuantidade;
    private Double vlSubTotal;
}