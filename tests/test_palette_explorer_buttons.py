import pytest
from conxius_orbit_gui import ConxiusOrbitGUI
from textual.widgets import Button
from unittest.mock import MagicMock
from conxius_orbit_secrets import validate_stacks_address


@pytest.mark.asyncio
async def test_address_explorer_buttons_exist():
    """Verify that the new address explorer buttons exist and have correct tooltips."""
    app = ConxiusOrbitGUI()
    # Mock monitor to avoid API calls during app startup
    app.monitor = MagicMock()
    app.monitor.api_url = "https://api.testnet.hiro.so"
    app.monitor.check_api_status.return_value = {
        "status": "online",
        "block_height": 100,
    }
    app.monitor.get_account_info.return_value = {"balance": "0", "nonce": 0}
    app.monitor.get_deployed_contracts.return_value = []
    app.monitor.get_recent_transactions.return_value = []

    async with app.run_test() as pilot:
        # Check if buttons are present
        dashboard_explorer_btn = app.query_one("#view-dashboard-explorer-btn", Button)
        settings_explorer_btn = app.query_one("#view-address-explorer-btn", Button)

        assert dashboard_explorer_btn is not None
        assert settings_explorer_btn is not None

        # Check tooltips
        assert (
            dashboard_explorer_btn.tooltip == "View your address on Hiro Explorer [e]"
        )
        assert settings_explorer_btn.tooltip == "View address on Hiro Explorer [e]"


@pytest.mark.asyncio
async def test_address_explorer_initial_state():
    """Verify the initial state of address explorer buttons."""
    # Test with configured address
    app_with_addr = ConxiusOrbitGUI()
    app_with_addr.address = "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
    app_with_addr.monitor = MagicMock()

    async with app_with_addr.run_test() as pilot:
        # Refresh state manually since on_mount ran before address was set
        is_addr_configured = app_with_addr.address != "Not configured"
        app_with_addr.w_view_dashboard_explorer_btn.disabled = not is_addr_configured
        app_with_addr.w_view_address_explorer_btn.disabled = (
            not validate_stacks_address(app_with_addr.address, app_with_addr.network)
        )

        assert (
            app_with_addr.query_one("#view-dashboard-explorer-btn", Button).disabled
            is False
        )
        assert (
            app_with_addr.query_one("#view-address-explorer-btn", Button).disabled
            is False
        )

    # Test with "Not configured" address
    app_no_addr = ConxiusOrbitGUI()
    app_no_addr.address = "Not configured"
    app_no_addr.monitor = MagicMock()

    async with app_no_addr.run_test() as pilot:
        assert (
            app_no_addr.query_one("#view-dashboard-explorer-btn", Button).disabled
            is True
        )
        assert (
            app_no_addr.query_one("#view-address-explorer-btn", Button).disabled is True
        )
