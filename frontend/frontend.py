import reflex as rx
import httpx
from typing import List

# Modelo de datos para criptomonedas
class Crypto(rx.Base):
    id: str
    name: str
    symbol: str
    price: str
    icon_url: str

# Estado global para las criptomonedas
class CryptoState(rx.State):
    crypto_data: List[Crypto] = []

    async def get_prices(self):
        """Obtiene datos de precios de criptomonedas desde el backend."""
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/crypto")
            raw_data = response.json()
            self.crypto_data = [
                Crypto(
                    id=item["id"],
                    name=item["name"],
                    symbol=item["symbol"],
                    price=f"${float(item['priceUsd']):.2f}",
                    icon_url=f"https://assets.coincap.io/assets/icons/{item['symbol'].lower()}@2x.png",
                )
                for item in raw_data
            ]

# Página Home
def home_page():
    return rx.container(
        rx.heading("Proyecto de WWW", font_size="2xl", margin_bottom="16px"),
        rx.text(
            "En este proyecto, vamos a utilizar FastAPI y Reflex para hacer una aplicación que nos ayude a ver los precios de las criptomonedas del momento a tiempo real.",
            font_size="lg",
            line_height="1.5",
        ),
        padding="20px",
        max_width="800px",
        margin="auto",
    )

# Página About
def about_page():
    team = [
        {"name": "Carlos Eduardo Guerrero Jaramillo", "email": "carlos.eduardo.guerrero@correounivalle.edu.co", "icon": "https://imgur.com/xfHzIOX.png"},
    ]
    return rx.container(
        rx.heading("Sobre mí", font_size="2xl", margin_bottom="16px"),
        rx.grid(
            rx.foreach(
                team,
                lambda member: rx.box(
                    rx.hstack(
                        rx.image(src=member["icon"], alt=member["name"], width="64px", height="64px"),
                        rx.vstack(
                            rx.text(member["name"], font_weight="bold"),
                            rx.text(member["email"], color="gray.500"),
                        ),
                        align_items="center",
                    ),
                    padding="2",
                    border="1px solid #eaeaea",
                    border_radius="md",
                    box_shadow="sm",
                ),
            ),
            template_columns="repeat(auto-fit, minmax(300px, 1fr))",
            gap="16px",
            width="100%",
        ),
        padding="20px",
        max_width="1000px",
        margin="auto",
    )

# Página API (Crypto)
# Cards de criptomonedas
def crypto_cards():
    return rx.grid(
        rx.foreach(
            CryptoState.crypto_data,
            lambda crypto: rx.box(
                rx.vstack(
                    rx.image(
                        src=crypto.icon_url, 
                        alt=crypto.name, 
                        width="80px", 
                        height="80px",
                        border_radius="full",
                        margin_bottom="8px",
                    ),
                    rx.text(
                        crypto.name, 
                        font_weight="bold", 
                        font_size="lg", 
                        color="blue.600",
                    ),
                    rx.text(f"({crypto.symbol})", color="gray.500"),
                    rx.text(
                        crypto.price, 
                        font_size="md", 
                        color="green.600", 
                        font_weight="bold",
                    ),
                ),
                padding="16px",
                border="1px solid #eaeaea",
                border_radius="lg",
                box_shadow="lg",
                text_align="center",
                transition="all 0.3s ease-in-out",
                _hover={"transform": "scale(1.05)", "box_shadow": "xl"},
            ),
        ),
        template_columns="repeat(auto-fit, minmax(250px, 1fr))",
        gap="24px",
        padding="16px",
        width="100%",  
    )


# Página de criptomonedas
def crypto_page():
    return rx.container(
        rx.heading(
            "Crypto Dashboard", 
            font_size="3xl", 
            color="gray.800", 
            margin_bottom="24px",
        ),
        rx.button(
            "Actualizar Precios", 
            on_click=CryptoState.get_prices,
            background_color="blue.500",
            color="white",
            _hover={"background_color": "blue.700"},
            padding="12px 24px",
            border_radius="md",
            margin_bottom="24px",
        ),
        crypto_cards(),
        padding="32px",
        max_width="1200px",
        margin="auto",
    )

# Barra de navegación 
def navbar():
    return rx.box(
        rx.hstack(
            # Título a la izquierda
            rx.text(
                "Crypto Dashboard",
                font_size="xl",
                font_weight="bold",
                color="blue.600",
                margin_right="auto",
            ),
            # Links de navegación a la derecha
            rx.link(
                "Inicio",
                href="/",
                padding="12px",
                font_size="md",
                _hover={"color": "blue.500", "text_decoration": "underline"},
            ),
            rx.link(
                "Sobre mí",
                href="/about",
                padding="12px",
                font_size="md",
                _hover={"color": "blue.500", "text_decoration": "underline"},
            ),
            rx.link(
                "Cryptos API",
                href="/crypto",
                padding="12px",
                font_size="md",
                _hover={"color": "blue.500", "text_decoration": "underline"},
            ),
            spacing="4",
            justify="between",
            align_items="center",
            padding="16px",
        ),
        width="100%",  # Ajusta el ancho al 100% de la pantalla
        background_color="white",
        box_shadow="lg",
        position="sticky",
        top="0",
        z_index="1000",
        border_bottom="1px solid #eaeaea",
    )


# Layout de la aplicación con diseño mejorado
def layout(page):
    return rx.vstack(
        navbar(),  # Navbar en la parte superior
        rx.box(
            page,  # Contenido de la página
            width="100%",
            max_width="1200px",
            margin="auto",
            padding="20px",
            background_color="gray.50",
            border_radius="md",
            box_shadow="lg",
            margin_top="16px",
        ),
    )



# Configuración de la aplicación
app = rx.App()
app.add_page(lambda: layout(home_page()), route="/", title="Inicio")
app.add_page(lambda: layout(about_page()), route="/about", title="Sobre mí")
app.add_page(lambda: layout(crypto_page()), route="/crypto", title="Cryptos API")
