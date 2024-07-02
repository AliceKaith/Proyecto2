from conn import c

def create_tables():
    c.execute("""
        CREATE TABLE Variables (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            valor DECIMAL(15, 2) NOT NULL,
            fecha DATE NOT NULL
        );
    """)

    c.execute("""
        CREATE TABLE Regimen (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ingresos DECIMAL(15, 2) NOT NULL,
            retencion_10 DECIMAL(15, 2) NOT NULL,
            deducciones DECIMAL(15, 2) NOT NULL,
            base DECIMAL(15, 2) NOT NULL,
            isr_o_favor DECIMAL(15, 2) NOT NULL,
            fecha DATE NOT NULL
        );
    """)

    c.execute("""
        CREATE TABLE CalculoISR (
            id INT AUTO_INCREMENT PRIMARY KEY,
            base DECIMAL(15, 2) NOT NULL,
            limite_inferior DECIMAL(15, 2) NOT NULL,
            excedente_lim_inferior DECIMAL(15, 2) NOT NULL,
            porcentaje_excedente DECIMAL(5, 2) NOT NULL,
            impuesto_marginal DECIMAL(15, 2) NOT NULL,
            cuota_fija DECIMAL(15, 2) NOT NULL,
            impuesto_determinado DECIMAL(15, 2) NOT NULL,
            subsidio_acreditab DECIMAL(15, 2) NOT NULL,
            impuesto_antes_cg DECIMAL(15, 2) NOT NULL,
            credito_general DECIMAL(15, 2) NOT NULL,
            impuesto_mensual DECIMAL(15, 2) NOT NULL,
            isr_retenido_10 DECIMAL(15, 2) NOT NULL,
            pagos_provisionales DECIMAL(15, 2) NOT NULL,
            isr_a_pagar DECIMAL(15, 2) NOT NULL,
            isr_retenido_exceso DECIMAL(15, 2) NOT NULL,
            fecha DATE NOT NULL
        );
    """)

    c.execute("""
        CREATE TABLE TarifaIntegral (
            id INT AUTO_INCREMENT PRIMARY KEY,
            mes VARCHAR(50) NOT NULL,
            limite_inferior DECIMAL(15, 2) NOT NULL,
            limite_superior DECIMAL(15, 2),
            cuota_fija DECIMAL(15, 2) NOT NULL,
            porcentaje DECIMAL(5, 2) NOT NULL
        );
    """)

    c.execute("""
        CREATE TABLE PagoProvisionalIVA (
            id INT AUTO_INCREMENT PRIMARY KEY,
            iva_venta DECIMAL(15, 2) NOT NULL,
            iva_retenido DECIMAL(15, 2) NOT NULL,
            iva_acreditable DECIMAL(15, 2) NOT NULL,
            diferencia DECIMAL(15, 2) NOT NULL,
            acreditamiento_iva DECIMAL(15, 2) NOT NULL,
            iva_pagar_o_favor DECIMAL(15, 2) NOT NULL,
            fecha DATE NOT NULL
        );
    """)

    c.execute("""
        CREATE TABLE ResumenPagoProvisional (
            id INT AUTO_INCREMENT PRIMARY KEY,
            isr DECIMAL(15, 2) NOT NULL,
            iva DECIMAL(15, 2) NOT NULL,
            otros DECIMAL(15, 2) NOT NULL,
            sub_empleo DECIMAL(15, 2) NOT NULL,
            fecha DATE NOT NULL
        );
    """)

    #Tablas

if __name__=="__main__":
    create_tables()