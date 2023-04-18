import io

import segno
import streamlit as st
from PIL import Image
from segno import helpers


def hr():
    st.markdown("---")


def inputForm() -> list[str, str | None, str | None, bool]:
    cols = st.columns(2)
    ssid = cols[0].text_input(
        "SSID", value="", max_chars=None, help="This is the name of your WiFi"
    )
    security = cols[0].selectbox(
        "Encryption",
        ("WEP", "WPA", None),
        index=1,
        format_func=lambda x: "No Password" if x is None else x,
        help="If you have a password and do not know about this, it is most likeliy WPA",
    )
    password = cols[1].text_input(
        "Passphrase",
        value=None,
        max_chars=None,
        help="This is the password for the WiFi",
        type="password",
        disabled=not bool(security),
    )
    hidden = st.checkbox(
        "Hidden WiFi", value=False, help="If the WiFi is hidden check this"
    )
    return ssid, password, security, hidden


@st.cache(suppress_st_warning=True)
def preview(image: io.BytesIO) -> None:
    preview_image = image
    image = Image.open(image)
    width, height = image.size
    st.markdown(f"Image size: {width}x{height}")
    st.image(preview_image, use_column_width=False)


def generate_qr_code(ssid, password, security, hidden, kind, scale):
    out = io.BytesIO()
    qrcode = helpers.make_wifi(
        ssid, password=password, security=security, hidden=hidden
    )
    qrcode.save(out, kind=kind, dark="#00000b", light=None, scale=scale)
    return out


def create_and_preview_qr(
    ssid: str,
    password: str | None = None,
    security: str | None = None,
    hidden: bool = False,
    kind: str = "png",
) -> None:
    scale = st.slider(
        "Scales image `x` times (expand image to view full size)",
        min_value=1,
        max_value=100,
        value=5,
        step=1,
        help="Scales the produced image",
    )
    out = generate_qr_code(ssid, password, security, hidden, kind, scale)
    image = preview(out)
    st.download_button(
        "Download QR code",
        out,
        file_name="wifi-qr-code.png",
        mime="image/png",
    )


def qr_explanation():
    return st.markdown(
        """A QR code (short for Quick Response code) is a two-dimensional barcode that can be scanned with a smartphone or other device to access information. In the context of logging into a WiFi network, a QR code can be used to quickly and easily connect to the WiFi network without having to manually enter the network name (SSID) and password!

Here's how it works:

1. Generate a QR code with the SSID (WiFi name) and password.
2. Anyone  who wants to connect to the WiFi network scans the QR code with a smartphone or other device equipped with a QR code reader.
3. The QR code reader decodes the QR code and automatically connects the user's device to the WiFi

This process eliminates the need for the user to manually enter the SSID and password, making it easier and faster to connect to the WiFi network. It also helps to ensure that the correct SSID and password are used without the hassle of typos. This allows you to have a strong password without the hassle of having to type it."""
    )


def main():
    security = "WPA"
    st.subheader("Parameters")
    st.markdown(
        """Fill in the boxed below to create a QR code for easy login on the specified wifi"""
    )

    ssid, password, security, hidden = inputForm()

    st.subheader("QR Code")
    create_and_preview_qr(ssid, password, security, hidden)

    st.subheader("About")

    with st.sidebar:
        st.title("WiFi QR Code Generator")
        qr_explanation()


if __name__ == "__main__":
    main()
