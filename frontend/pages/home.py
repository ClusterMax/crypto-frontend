import reflex as rx
import httpx
from reflex import cache

# Función para obtener datos de la API del backend
async def fetch_crypto_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/crypto")
        return response.json()

# Crear el modelo para los activos
class CryptoAsset(rx.Model):
    id: str
    name: str
    symbol: str
    priceUsd: float

# Crear la vista de la aplicación
def home():
    crypto_data = fetch_crypto_data()

    return rx.Column(
        [
            rx.Text("Cryptocurrency Prices", font_size="2xl", font_weight="bold"),
            rx.For(
                crypto_data,
                lambda asset: rx.Text(f"{asset['name']} ({asset['symbol']}): ${asset['priceUsd']}"),
            ),
        ]
    )
