import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';

export default function VentaTerminal() {
    const [catalogo, setCatalogo] = useState([]);
    const [carrito, setCarrito] = useState([]);
    const [tipoDoc, setTipoDoc] = useState('BOLETA');
    const [datosFactura, setDatosFactura] = useState({
        rut: '',
        razon_social: '',
        giro: '',
        direccion: ''
    });
    const [mensaje, setMensaje] = useState('');
    const [error, setError] = useState('');
    const [modalPrevia, setModalPrevia] = useState(false);

    // Cargar productos desde Django al abrir la pantalla
    useEffect(() => {
        apiClient.get('productos/')
            .then(res => setCatalogo(res.data))
            .catch(() => setError('Error al cargar catálogo de productos. Verifique el backend.'));
    }, []);

    // Agregar producto al carrito
    const agregarAlCarrito = (producto) => {
        const existe = carrito.find(item => item.codigo === producto.codigo);
        if (existe) {
            setCarrito(carrito.map(item => 
                item.codigo === producto.codigo 
                ? { ...item, cantidad: item.cantidad + 1 } 
                : item
            ));
        } else {
            setCarrito([...carrito, { ...producto, cantidad: 1 }]);
        }
    };

    // Modificar cantidad o quitar
    const modificarCantidad = (codigo, delta) => {
        setCarrito(carrito.map(item => {
            if (item.codigo === codigo) {
                const nuevaCant = item.cantidad + delta;
                return nuevaCant > 0 ? { ...item, cantidad: nuevaCant } : null;
            }
            return item;
        }).filter(Boolean));
    };

    // Cálculos en tiempo real
    const subtotalNeto = carrito.reduce((acc, item) => acc + (parseFloat(item.precio_unitario) * item.cantidad), 0);
    const montoIva = subtotalNeto * 0.19;
    const totalGeneral = subtotalNeto + montoIva;

    // Enviar venta a la API
    const confirmarVenta = async () => {
        setError('');
        setMensaje('');
        try {
            const payload = {
                items: carrito.map(i => ({ codigo: i.codigo, cantidad: i.cantidad })),
                tipo_documento: tipoDoc,
                datos_factura: tipoDoc === 'FACTURA' ? datosFactura : null
            };

            const res = await apiClient.post('ventas/registrar/', payload);
            setMensaje(`¡Venta procesada con éxito! N° Comprobante: ${res.data.comprobante.numero_documento}`);
            setCarrito([]);
            setModalPrevia(false);
            if (tipoDoc === 'FACTURA') {
                setDatosFactura({ rut: '', razon_social: '', giro: '', direccion: '' });
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Error al emitir el comprobante');
            setModalPrevia(false);
        }
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'sans-serif', maxWidth: '1000px', margin: '0 auto' }}>
            <h1 style={{ borderBottom: '2px solid #2c3e50', paddingBottom: '10px' }}>Sistema Web de Ventas - Mostrador</h1>
            
            {mensaje && <div style={{ background: '#d4edda', color: '#155724', padding: '10px', marginBottom: '15px', borderRadius: '4px' }}>{mensaje}</div>}
            {error && <div style={{ background: '#f8d7da', color: '#721c24', padding: '10px', marginBottom: '15px', borderRadius: '4px' }}>{error}</div>}

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                {/* Catálogo de Productos */}
                <div style={{ border: '1px solid #ccc', borderRadius: '6px', padding: '15px' }}>
                    <h2>Productos Disponibles</h2>
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ background: '#eee', textAlign: 'left' }}>
                                <th style={{ padding: '8px' }}>Descripción</th>
                                <th style={{ padding: '8px' }}>Precio</th>
                                <th style={{ padding: '8px' }}>Acción</th>
                            </tr>
                        </thead>
                        <tbody>
                            {catalogo.map(p => (
                                <tr key={p.codigo} style={{ borderBottom: '1px solid #eee' }}>
                                    <td style={{ padding: '8px' }}>{p.descripcion}</td>
                                    <td style={{ padding: '8px' }}>${parseFloat(p.precio_unitario).toFixed(0)}</td>
                                    <td style={{ padding: '8px' }}>
                                        <button onClick={() => agregarAlCarrito(p)} style={{ background: '#28a745', color: 'white', border: 'none', padding: '5px 10px', cursor: 'pointer', borderRadius: '3px' }}>
                                            + Agregar
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* Carrito y Cobro */}
                <div style={{ border: '1px solid #ccc', borderRadius: '6px', padding: '15px' }}>
                    <h2>Detalle de Venta</h2>
                    {carrito.length === 0 ? (
                        <p style={{ color: '#777' }}>No hay artículos en la venta actual.</p>
                    ) : (
                        <div>
                            <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '15px' }}>
                                <tbody>
                                    {carrito.map(item => (
                                        <tr key={item.codigo} style={{ borderBottom: '1px solid #eee' }}>
                                            <td>{item.descripcion}</td>
                                            <td>
                                                <button onClick={() => modificarCantidad(item.codigo, -1)}>-</button>
                                                <span style={{ margin: '0 8px' }}>{item.cantidad}</span>
                                                <button onClick={() => modificarCantidad(item.codigo, 1)}>+</button>
                                            </td>
                                            <td style={{ textAlign: 'right' }}>${(item.precio_unitario * item.cantidad).toFixed(0)}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>

                            <div style={{ background: '#f8f9fa', padding: '10px', borderRadius: '4px', marginBottom: '15px' }}>
                                <p style={{ margin: '4px 0' }}>Subtotal Neto: <strong>${subtotalNeto.toFixed(0)}</strong></p>
                                <p style={{ margin: '4px 0' }}>IVA (19%): <strong>${montoIva.toFixed(0)}</strong></p>
                                <h3 style={{ margin: '6px 0', color: '#0056b3' }}>Total: ${totalGeneral.toFixed(0)}</h3>
                            </div>

                            <div style={{ marginBottom: '15px' }}>
                                <label style={{ marginRight: '15px' }}>
                                    <input type="radio" value="BOLETA" checked={tipoDoc === 'BOLETA'} onChange={() => setTipoDoc('BOLETA')} /> Boleta
                                </label>
                                <label>
                                    <input type="radio" value="FACTURA" checked={tipoDoc === 'FACTURA'} onChange={() => setTipoDoc('FACTURA')} /> Factura
                                </label>
                            </div>

                            {tipoDoc === 'FACTURA' && (
                                <div style={{ display: 'grid', gap: '8px', marginBottom: '15px', background: '#e9ecef', padding: '10px', borderRadius: '4px' }}>
                                    <input placeholder="RUT (ej: 76.123.456-7)" value={datosFactura.rut} onChange={e => setDatosFactura({...datosFactura, rut: e.target.value})} style={{ padding: '6px' }} />
                                    <input placeholder="Razón Social" value={datosFactura.razon_social} onChange={e => setDatosFactura({...datosFactura, razon_social: e.target.value})} style={{ padding: '6px' }} />
                                    <input placeholder="Giro Comercial" value={datosFactura.giro} onChange={e => setDatosFactura({...datosFactura, giro: e.target.value})} style={{ padding: '6px' }} />
                                    <input placeholder="Dirección" value={datosFactura.direccion} onChange={e => setDatosFactura({...datosFactura, direccion: e.target.value})} style={{ padding: '6px' }} />
                                </div>
                            )}

                            <button onClick={() => setModalPrevia(true)} style={{ width: '100%', background: '#007bff', color: 'white', border: 'none', padding: '10px', cursor: 'pointer', borderRadius: '4px', fontSize: '16px' }}>
                                Vista Previa y Emitir
                            </button>
                        </div>
                    )}
                </div>
            </div>

            {/* Modal de Previsualización */}
            {modalPrevia && (
                <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <div style={{ background: 'white', padding: '25px', borderRadius: '8px', maxWidth: '400px', width: '100%' }}>
                        <h2>Confirmación de Documento</h2>
                        <p><strong>Tipo:</strong> {tipoDoc}</p>
                        {tipoDoc === 'FACTURA' && (
                            <p style={{ fontSize: '13px', color: '#555' }}>
                                <strong>Receptor:</strong> {datosFactura.razon_social} ({datosFactura.rut})
                            </p>
                        )}
                        <hr />
                        <p>Subtotal Neto: ${subtotalNeto.toFixed(0)}</p>
                        <p>IVA (19%): ${montoIva.toFixed(0)}</p>
                        <h3>Total a Cobrar: ${totalGeneral.toFixed(0)}</h3>
                        <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
                            <button onClick={() => setModalPrevia(false)} style={{ flex: 1, padding: '8px', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Volver</button>
                            <button onClick={confirmarVenta} style={{ flex: 1, padding: '8px', background: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Confirmar y Guardar</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}