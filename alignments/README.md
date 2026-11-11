# Alignment modules

One module per designation scheme. Each declares the scheme's **projection contract**: what kind of WESO thing each form of identifier names. See [docs/alignment.md](../docs/alignment.md#writing-an-alignment-module).

| Module | Scheme | Status |
|---|---|---|
| [`rds-wtg/`](rds-wtg) | RDS for WTG, VGB/BDEW guideline v2.0 (2024) | Draft — all four aspects |
| RDS-PP | IEC 81346 for power plants | Wanted |
| RDS-PS | IEC 81346 for power systems | Wanted |
| ISO 14224 | Granularity scale and equipment classes as reporting labels | Wanted |

Manufacturer and operator schemes usually live with the data that uses them (see the serial and parts schemes in [`examples/`](../examples)) rather than here, unless they are shared across organisations.

To start a new one, copy [`_template/`](_template).
