from stallworth_nqueens.common.logging.logger import format_unexpected_error


def test_format_unexpected_error_includes_type_and_message():
    assert (
        format_unexpected_error(RuntimeError("report generation failed"))
        == "Unexpected error (RuntimeError): report generation failed"
    )


def test_format_unexpected_error_preserves_key_error_without_extra_quotes():
    error = KeyError(
        "Unknown SVG image: report-watermark-sm. "
        "Available images: report-watermark"
    )

    assert format_unexpected_error(error) == (
        "Unexpected error (KeyError): "
        "Unknown SVG image: report-watermark-sm. "
        "Available images: report-watermark"
    )
